#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManjuForge 一致性检查器 (consistency_check.py v1.0)
==================================================
跨文件引用完整性校验。补 quality_check.py 查不到的一类事故：
quality_check.py 只看**单个文件内部**的字段是否合规；
本工具只看**文件与文件之间**是否自相矛盾——记忆断裂、引用悬空、状态不同步。

22 项检查，分五组：
    M 记忆文件层   M1 文件齐备 / M2 最后更新集一致 / M3 伏笔清单双向一致
                   M4 伏笔状态同步 / M5 引用完整性(悬空F-ID) / M6 角色弧光覆盖
    F 伏笔表健康   F1 回收发酵期 / F2 回收状态矛盾 / F3 悬置 / F4 并发上限 / F5 ID唯一
    R 关系图       R1 矩阵对称 / R2 阶段不跳级 / R3 矩阵与时间线一致 / R4 关系型伏笔有落点
    D 人物状态     D1 快照角色有档案 / D2 出场角色有快照 / D3 最后出场准确
    P 分集层       P1 时间轴连续 / P2 碎片有风格锚点 / P3 角色有Character ID / P4 ID跨集复用

用法:
    python scripts/consistency_check.py [项目目录] [--json] [--quiet]

退出码:
    0 = 无 🔴      1 = 存在 🔴

自测:
    python scripts/selftest.py     # 两个检查器的确定性逻辑自测（不调模型，不耗额度）

项数收口:
    「22 项」必须与 SKILL.md「跨文件一致性检查」节、README 说明一致；
    selftest.py 的最后一项断言会扫描本文件校验这个数字，改代码请同步改两处文档。

设计原则（借用 drama-skills creator_markdown_check.py 的报错范式）:
    每条问题必须同时给出「哪两个文件在哪一点上矛盾」和「怎么修」，
    不做只报 "校验失败" 的哑巴检查器。
"""

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

# ---------------------------------------------------------------- 常量

MEMORY_FILES = [
    "角色档案.md",
    "世界观.md",
    "场景布局.md",
    "剧情摘要.md",
    "伏笔表.md",
    "故事圣经.md",
    "角色关系图.md",
]

# 伏笔状态词表 → 语义
TABLE_STATUS = {
    "已埋": "active",
    "活跃": "active",
    "悬置": "active",
    "已回收": "closed",
    "已废弃": "dropped",
}
SUMMARY_STATUS = {
    "🟡进行中": "active",
    "🟢已回收": "closed",
    "🔴已废弃": "dropped",
}

# 关系阶段阶梯（正向）。同义词并入同层，用于「不跳级」判定。
STAGE_LADDER = [
    ("冷漠", "无视", "陌生"),
    ("观察", "好奇", "试探"),
    ("认可", "认同", "正眼"),
    ("并肩", "维护", "并肩作战"),
    ("托付", "信任", "依赖"),
]
ANTAGONIST_STAGES = ("敌对", "冲突", "公开敌对", "背叛")

# 名字匹配阈值（归一化后相似度）
NAME_MATCH_RATIO = 0.72


# ---------------------------------------------------------------- 工具函数

def read_text(path: Path) -> str:
    """按 UTF-8 读取，兼容 BOM 和 CRLF。"""
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def norm_name(s: str) -> str:
    """归一化名字：去括号内容、去引号标点空格。"""
    s = re.sub(r"[（(][^）)]*[）)]", "", s)
    s = re.sub(r"[\"'“”‘’·、，,。.\s/\\|—\-_]", "", s)
    return s.strip()


def name_match(a: str, b: str) -> bool:
    """两个条目名是否指同一件事（归一化后包含或高相似）。"""
    na, nb = norm_name(a), norm_name(b)
    if not na or not nb:
        return False
    if na in nb or nb in na:
        return True
    return SequenceMatcher(None, na, nb).ratio() >= NAME_MATCH_RATIO


def epnum(s: str):
    """'E1' / '第5集' / 'E20+' / '长期' / '—' → int 或 None。"""
    if s is None:
        return None
    s = str(s).strip()
    if not s or s in {"—", "-", "--", "长线", "长期", "无"}:
        return None
    m = re.search(r"\d+", s)
    return int(m.group()) if m else None


def stage_level(cell: str):
    """从一段文字里解析出关系阶段层级，返回 (level, token) 或 None。"""
    for token in ANTAGONIST_STAGES:
        if token in cell:
            return None, token
    for lvl, group in enumerate(STAGE_LADDER):
        for token in group:
            if token in cell:
                return lvl, token
    return None, ""


def pair_key(s: str):
    """关系对归一化：'林霜·沈舟' 与 '沈舟-林霜' 视为同一对（顺序无关）。"""
    parts = [norm_name(p) for p in re.split(r"[-·、/＋+]", s or "") if norm_name(p)]
    return frozenset(parts)


def parse_tables(text: str):
    """解析全部 markdown 表格，返回 [(header:list, rows:list[list])]。"""
    out, block = [], []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            block.append(s)
        else:
            if len(block) >= 2:
                out.append(block)
            block = []
    if len(block) >= 2:
        out.append(block)

    tables = []
    for blk in out:
        cells = lambda ln: [c.strip() for c in ln.strip().strip("|").split("|")]
        header = cells(blk[0])
        # 第二行必须是分隔行
        if not re.fullmatch(r"[|:\-\s]+", blk[1]):
            continue
        rows = [cells(ln) for ln in blk[2:] if ln.strip().strip("|").strip()]
        tables.append((header, rows))
    return tables


def find_table(text: str, *keywords):
    """找表头同时包含全部关键词的第一张表。"""
    for header, rows in parse_tables(text):
        joined = "".join(header)
        if all(k in joined for k in keywords):
            return header, rows
    return None, None


def row_dict(header, row):
    """按表头对齐成 dict（列数不齐时缺位补空）。"""
    cells = row + [""] * (len(header) - len(row))
    return {header[i]: cells[i] for i in range(len(header))}


def get(d: dict, *cands, default=""):
    """按候选列名模糊取值。"""
    for k, v in d.items():
        for c in cands:
            if c in k:
                return v
    return default


class Finding:
    __slots__ = ("level", "code", "where", "problem", "fix")

    def __init__(self, level, code, where, problem, fix):
        self.level, self.code, self.where = level, code, where
        self.problem, self.fix = problem, fix

    def to_dict(self):
        return {"level": self.level, "code": self.code, "where": self.where,
                "problem": self.problem, "fix": self.fix}


# ---------------------------------------------------------------- 解析

def parse_max_episode(text: str):
    """从「最后更新」字段解析集数。"""
    m = re.search(r"最后更新[^\n]*?第?\s*(\d+)\s*集", text)
    return int(m.group(1)) if m else None


def parse_foreshadow_table(text: str):
    header, rows = find_table(text, "伏笔ID", "状态")
    if not header:
        return []
    out = []
    for r in rows:
        d = row_dict(header, r)
        out.append({
            "id": d.get("伏笔ID", "").strip(),
            "name": d.get("内容", "").strip(),
            "type": d.get("类型", "").strip(),
            "plant_ep": epnum(d.get("埋设集", "")),
            "priority": d.get("重要度", "").strip(),
            "status_raw": d.get("状态", "").strip(),
            "plan_ep": d.get("计划回收集", ""),
            "pay_ep": epnum(d.get("实际回收集", "")),
            "last_ep": epnum(d.get("最近推进集", "")),
            "links": d.get("关联", "").strip(),
            "note": d.get("备注", "").strip(),
        })
    return out


def parse_summary(text: str):
    """剧情摘要 → 伏笔清单 / 人物快照。"""
    fs, ch = [], []
    header, rows = find_table(text, "伏笔", "埋入集数", "状态")
    if header:
        for r in rows:
            d = row_dict(header, r)
            fs.append({
                "name": d.get("伏笔", "").strip(),
                "plant_ep": epnum(d.get("埋入集数", "")),
                "status_raw": d.get("状态", "").strip(),
                "note": d.get("备注", "").strip(),
            })
    header, rows = find_table(text, "当前状态", "最后出场")
    if header:
        for r in rows:
            d = row_dict(header, r)
            ch.append({
                "name": d.get("角色", "").strip(),
                "state": d.get("当前状态", "").strip(),
                "last_seen": d.get("最后出场", "").strip(),
                "change": d.get("关键变化", "").strip(),
            })
    return fs, ch


def parse_profiles(text: str):
    """角色档案 → 角色名列表。"""
    names = re.findall(r"^###\s*角色\d+[:：]\s*([^（(]+)", text, re.MULTILINE)
    if not names:
        names = re.findall(r"^#{2,4}\s*([^#\n（(]{1,12})（[^）]*）", text, re.MULTILINE)
    return [n.strip() for n in names if n.strip()]


def parse_relations(text: str):
    """角色关系图 → (矩阵, 时间线, 角色列表)。"""
    matrix, actors = {}, []
    timeline = []
    for header, rows in parse_tables(text):
        joined = "".join(header)
        if "角色" in joined and len(header) >= 3 and not matrix:
            cols = header[1:]
            for r in rows:
                if not r:
                    continue
                rowname = r[0]
                actors.append(rowname)
                for i, c in enumerate(cols):
                    val = r[i + 1] if i + 1 < len(r) else ""
                    matrix[(rowname, c)] = val
            continue
        if "关系对" in joined and "变化" in joined:
            for r in rows:
                d = row_dict(header, r)
                timeline.append({
                    "ep": epnum(d.get("集数", "")),
                    "pair": d.get("关系对", "").strip(),
                    "event": d.get("事件", "").strip(),
                    "change": d.get("变化", "").strip(),
                    "kind": d.get("类型", "").strip(),
                })
    return matrix, [a for a in actors if a and a != "—"], timeline


def parse_bible(text: str):
    """故事圣经 → 角色弧光角色列表 + 视觉母题。"""
    roster, motifs = [], []
    header, rows = find_table(text, "身份不变量", "弧线终点")
    if header:
        for r in rows:
            roster.append(row_dict(header, r).get("角色", "").strip())
    header, rows = find_table(text, "符号", "首现集")
    if header:
        for r in rows:
            d = row_dict(header, r)
            motifs.append({"symbol": d.get("符号", "").strip(),
                           "owner": d.get("关联角色", "").strip()})
    return [r for r in roster if r], motifs


def parse_fragments(text: str):
    """分集文件 → 竖屏碎片列表（含时间轴秒数）。"""
    frags = []
    for line in text.splitlines():
        if "→" not in line or not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 7 or re.fullmatch(r"[|:\-\s]+", line.strip()):
            continue
        m = re.match(r"(\d{1,2}):(\d{2})[→\-]{1,2}(\d{1,2}):(\d{2})", cells[2])
        if not m:
            continue
        frags.append({
            "id": cells[0],
            "start": int(m.group(1)) * 60 + int(m.group(2)),
            "end": int(m.group(3)) * 60 + int(m.group(4)),
            "visual": cells[4],
            "prompt": cells[6],
        })
    return frags


def episode_files(project: Path):
    """按集数排序的分集文件。"""
    fs = []
    for p in project.glob("第*集_完整版.md"):
        m = re.search(r"第(\d+)集", p.name)
        if m:
            fs.append((int(m.group(1)), p))
    return sorted(fs)


# ---------------------------------------------------------------- 检查

def check_memory(txt, findings):
    latest = 0
    missing = [f for f in MEMORY_FILES if f not in txt]
    if missing:
        findings.append(Finding(
            "🔴", "M1", "项目目录",
            f"记忆文件缺失：{'、'.join(missing)}——按连载记忆机制每部剧必须七文件齐备",
            "补齐缺失文件后重跑；场景布局.md 可用 templates/ 下的模板初始化（缺它=跨集空间一致性无锚点）"))

    # M2 最后更新集一致
    stamps = {}
    for f in MEMORY_FILES:
        t = txt.get(f, "")
        if not t:
            continue
        n = parse_max_episode(t)
        if n:
            stamps[f] = n
    for f in MEMORY_FILES:
        if f in stamps or f not in txt:
            continue
        m = re.search(r"最后更新[^\n]*?第\s*(\d+)\s*集", txt[f])
        if m:
            stamps[f] = int(m.group(1))
    if stamps:
        latest = max(stamps.values())
        lag = {f: n for f, n in stamps.items() if n != latest}
        if lag:
            detail = "、".join(f"{f}→E{n}" for f, n in sorted(lag.items()))
            findings.append(Finding(
                "🔴", "M2", "各记忆文件「最后更新」",
                f"记忆文件更新进度不一致（最新应为 E{latest}）：{detail}",
                "记忆断裂的典型征兆——说明某次创作后漏同步了部分文件；"
                "逐文件补到 E" + str(latest) + " 再继续下一集"))
        else:
            findings.append(Finding("🟢", "M2", "各记忆文件「最后更新」",
                                    f"全部同步至 E{latest}", ""))

    # M3/M4 伏笔清单双向一致 + 状态同步
    fh = parse_foreshadow_table(txt.get("伏笔表.md", ""))
    sf, _ = parse_summary(txt.get("剧情摘要.md", ""))
    for row in fh:
        if not row["id"]:
            continue
        hit = next((s for s in sf if name_match(row["name"], s["name"])), None)
        if not hit:
            findings.append(Finding(
                "🔴", "M3", f"伏笔表.md ↔ 剧情摘要.md",
                f"{row['id']}「{row['name']}」登记在伏笔表，但剧情摘要的「关键伏笔追踪」里没有对应行",
                f"在剧情摘要「关键伏笔追踪」补一行：{row['name']} | 第{row['plant_ep']}集 | "
                f"{row['status_raw']} | 否则下集创作时读不到这根线=遗忘"))
            continue
        a = TABLE_STATUS.get(row["status_raw"])
        b = SUMMARY_STATUS.get(hit["status_raw"])
        if a and b and a != b:
            findings.append(Finding(
                "🔴", "M4", f"伏笔表.md ↔ 剧情摘要.md",
                f"{row['id']}「{row['name']}」状态不同步：伏笔表={row['status_raw']}，摘要={hit['status_raw']}",
                f"以伏笔表为准改写摘要该行状态为「{row['status_raw']}」（回收完成必须两处同时改）"))
    for s in sf:
        if not any(name_match(r["name"], s["name"]) for r in fh):
            findings.append(Finding(
                "🔴", "M3", f"剧情摘要.md ↔ 伏笔表.md",
                f"摘要伏笔「{s['name']}」在伏笔表中没有登记行",
                "在伏笔表补登记（含ID/类型/埋设集/重要度），否则该伏笔无生命周期追踪"))

    # M5 引用完整性：别的文件引用的 F-ID 是否存在
    for f in ("故事圣经.md", "角色关系图.md", "剧情摘要.md"):
        ids = set(re.findall(r"\bF\d{3}\b", txt.get(f, "")))
        ids |= set(re.findall(r"\bF\d{2,3}\b", txt.get(f, "")))
        ids = {i for i in ids if i.startswith("F")}
        known = {r["id"] for r in fh if r["id"]}
        dangling = sorted(i for i in ids if i not in known)
        if dangling:
            findings.append(Finding(
                "🔴", "M5", f"{f} ↔ 伏笔表.md",
                f"引用了不存在的伏笔ID：{'、'.join(dangling)}",
                "要么在伏笔表补登记这些ID，要么把引用改成正确的ID——悬空引用会让下集误判伏笔状态"))

    # M6 故事圣经角色弧光覆盖角色档案
    profiles = parse_profiles(txt.get("角色档案.md", ""))
    roster, _ = parse_bible(txt.get("故事圣经.md", ""))
    for role in roster:
        if profiles and not any(name_match(role, p) for p in profiles):
            findings.append(Finding(
                "🔴", "M6", "故事圣经.md ↔ 角色档案.md",
                f"故事圣经「角色弧光」登记了「{role}」，但角色档案里没有这个角色",
                "在角色档案补该角色的身份不变量/状态变量/禁止变化，或从弧光表移除"))
    return profiles, latest


def check_foreshadow(fh, latest, findings):
    seen = {}
    for row in fh:
        rid = row["id"]
        if rid in seen:
            findings.append(Finding("🔴", "F5", "伏笔表.md",
                                    f"伏笔ID重复：{rid}",
                                    "ID 是跨文件引用的主键，重复会导致回收指向错误；改为唯一ID"))
        seen[rid] = row

        if row["status_raw"] == "已回收":
            if row["pay_ep"] is None:
                findings.append(Finding(
                    "🔴", "F2", "伏笔表.md",
                    f"{rid}「{row['name']}」状态为已回收，但「实际回收集」为空",
                    "补填实际回收集，或把状态改回活跃——状态与字段自相矛盾会污染健康统计"))
            elif row["plant_ep"] is not None:
                gap = row["pay_ep"] - row["plant_ep"]
                if gap < 2:
                    findings.append(Finding(
                        "🟡", "F1", "伏笔表.md",
                        f"{rid}「{row['name']}」埋于E{row['plant_ep']}、收于E{row['pay_ep']}，"
                        f"仅发酵 {gap} 集（规则要求 ≥2 集）",
                        "本集已过审可保留，但登记备注「发酵期不足·标记参考」；"
                        "下集起同类伏笔至少隔一集再回收"))

        if latest and row["status_raw"] == "活跃" and row["last_ep"]:
            idle = latest - row["last_ep"]
            if idle > 8:
                findings.append(Finding(
                    "🔴", "F3", "伏笔表.md",
                    f"{rid}「{row['name']}」最近推进于E{row['last_ep']}，距最新E{latest}已悬置 {idle} 集",
                    "插入一次推进（提及/升级/回收）或人工决策标记「已废弃」——"
                    "悬置>8集观众已忘记这根线"))

    active = [r for r in fh if r["status_raw"] in ("活跃", "已埋", "悬置")]
    for grade, cap in (("S", 3), ("A", 5)):
        n = len([r for r in active if r["priority"] == grade])
        if n > cap:
            names = "、".join(r["id"] for r in active if r["priority"] == grade)
            findings.append(Finding(
                "🟡", "F4", "伏笔表.md",
                f"{grade}级活跃伏笔 {n} 条，超出上限 {cap}（{names}）",
                f"优先回收/降级其中 {n - cap} 条——并发S级过多会让每集都像在收网，反而没有重点"))


def check_relations(txt, fh, findings):
    matrix, actors, timeline = parse_relations(txt.get("角色关系图.md", ""))
    if not matrix:
        return
    # R1 对称
    for a in actors:
        for b in actors:
            if a == b:
                continue
            ab, ba = matrix.get((a, b), ""), matrix.get((b, a), "")
            if ab and ba:
                na = re.sub(r"[\d·\s]", "", ab)
                nb = re.sub(r"[\d·\s]", "", ba)
                if na != nb:
                    findings.append(Finding(
                        "🟡", "R1", "角色关系图.md 关系矩阵",
                        f"矩阵不对称：{a}→{b}=「{ab}」，但 {b}→{a}=「{nb}」",
                        "两侧描述同一段关系必须同义；不对称会让下游按「谁看谁」取值时读到两套事实"))

    # R2 阶段不跳级
    pairs = {}
    for t in timeline:
        if not t["pair"] or t["ep"] is None:
            continue
        lvl, token = stage_level(t["change"])
        if lvl is None:
            continue
        pairs.setdefault(t["pair"], []).append((t["ep"], lvl, token))
    for pair, seq in pairs.items():
        seq.sort()
        for (e1, l1, t1), (e2, l2, t2) in zip(seq, seq[1:]):
            if l2 - l1 > 1:
                findings.append(Finding(
                    "🔴", "R2", "角色关系图.md 关系事件时间线",
                    f"{pair} 关系阶段跳级：E{e1}「{t1}」→ E{e2}「{t2}」（跨 {l2 - l1} 级）",
                    "阶段不能跳级（观察→托付=跳级）。在中间集补一次过渡事件，"
                    "如「行为否定+心理认可」式的小推进"))

    # R3 矩阵末态与时间线一致
    for pair, seq in pairs.items():
        parts = [p.strip() for p in re.split(r"[-·]", pair) if p.strip()]
        if len(parts) < 2:
            continue
        a, b = parts[0], parts[1]
        cell = matrix.get((a, b), "") or matrix.get((b, a), "")
        if not cell:
            continue
        mlvl, mtoken = stage_level(cell)
        last = max(seq, key=lambda x: x[0])
        llvl, ltoken = last[1], last[2]
        if mlvl is not None and llvl is not None and mlvl != llvl:
            findings.append(Finding(
                "🟡", "R3", "角色关系图.md 矩阵 ↔ 时间线",
                f"{pair} 矩阵写「{mtoken}」（第{mlvl}级），但时间线末态是「{ltoken}」（第{llvl}级）",
                "矩阵是「当前快照」，必须等于时间线最后一条；改矩阵或补一条更晚的时间线事件"))

    # R4 关系型伏笔在关系图有落点
    tl_keys = {pair_key(t["pair"]) for t in timeline if t["pair"]}
    for row in fh:
        if row["type"] != "关系型" or not row["id"]:
            continue
        key = pair_key(row["links"])
        if not key or key not in tl_keys:
            findings.append(Finding(
                "🟡", "R4", "伏笔表.md ↔ 角色关系图.md",
                f"关系型伏笔 {row['id']}「{row['name']}」关联「{row['links']}」，"
                f"但关系事件时间线里找不到该关系对的事件",
                "在该关系对下补事件行（哪怕只是「状态未变但被提及」），"
                "否则关系型伏笔的进展没有关系图支撑"))


def check_characters(txt, profiles, latest, findings):
    _, snapshot = parse_summary(txt.get("剧情摘要.md", ""))
    _, _, timeline = parse_relations(txt.get("角色关系图.md", ""))
    if not snapshot:
        return

    # D1 快照角色必须在角色档案里有档案（群像角色明确标注可豁免，但仍单独可见）
    CROWD = {"小商户", "群像", "众人", "群众", "商户们", "围观者"}
    for c in snapshot:
        if c["name"] in CROWD:
            findings.append(Finding(
                "🟢", "D1", "剧情摘要.md",
                f"群像角色「{c['name']}」按群像处理，未建个人档案（豁免）",
                ""))
            continue
        if profiles and not any(name_match(c["name"], p) for p in profiles):
            findings.append(Finding(
                "🟡", "D1", "剧情摘要.md ↔ 角色档案.md",
                f"剧情摘要人物快照有「{c['name']}」，角色档案里没有对应档案",
                "有台词/关系的角色必须建档（否则下集可能换性格）；确属群像就标准化命名为「小商户」并在档案注明"))

    # D2 本集在关系图有事件的角色，必须进快照（否则状态漂移无人察觉）
    for t in timeline:
        if t["ep"] != latest or not t["pair"]:
            continue
        for side in re.split(r"[-·]", t["pair"]):
            side = side.strip()
            if not side or side in {"众人", "群像"}:
                continue
            if not any(name_match(side, c["name"]) for c in snapshot):
                findings.append(Finding(
                    "🔴", "D2", "剧情摘要.md ↔ 角色关系图.md",
                    f"E{latest} 关系事件「{t['event'][:24]}」涉及「{side}」，"
                    f"但剧情摘要人物状态快照里没有该角色",
                    f"在人物状态快照补一行「{side}」并写清本集状态变化——"
                    "出场了却不登记=下集把ta当没出现过，状态变量会照抄上一集"))

    # D3 最后出场必须真实（该集文件里确实出现该角色名）
    eps = episode_files(Path(txt["__dir__"])) if "__dir__" in txt else []
    epmap = dict(eps)
    for c in snapshot:
        n = epnum(c["last_seen"])
        if n is None or n not in epmap:
            continue
        body = read_text(epmap[n])
        if c["name"] and c["name"] not in body:
            findings.append(Finding(
                "🔴", "D3", "剧情摘要.md ↔ 分集文件",
                f"快照称「{c['name']}」最后出场于第{n}集，但第{n}集正文中找不到该角色",
                "核对是「仅被提及」还是真出场：真没出场就把「最后出场」改回上一次实际出场集数"))


def check_episodes(project: Path, profiles, findings):
    """分集层：时间轴连续性 + 风格锚点 + Character ID 覆盖（按集聚合，不逐碎片刷屏）。"""
    eps = episode_files(project)
    if not eps:
        return
    id_chars = {}          # Character ID → 用到的角色名集合
    char_hits = {}         # 角色名 → 出现过的碎片数（有锚定/无锚定分开计）
    for n, path in eps:
        frags = parse_fragments(read_text(path))
        if not frags:
            continue

        # P1 时间轴连续（逐条报，因为每条都是独立事故）
        for prev, cur in zip(frags, frags[1:]):
            if cur["start"] > prev["end"]:
                findings.append(Finding(
                    "🔴", "P1", f"第{n}集_完整版.md",
                    f"时间轴空档：{prev['id']} 结束于 {prev['end']}s，{cur['id']} 从 {cur['start']}s 开始，"
                    f"缺口 {cur['start'] - prev['end']}s 无碎片覆盖",
                    "补一个空镜/过渡碎片填满缺口（日影移动、烛火点燃类），或把后一碎片起点前移——"
                    "成片会出现黑场或跳帧"))
            elif cur["start"] < prev["end"]:
                findings.append(Finding(
                    "🟡", "P1", f"第{n}集_完整版.md",
                    f"时间轴重叠：{prev['id']} 到 {prev['end']}s，{cur['id']} 从 {cur['start']}s 开始",
                    "碎片必须首尾相接；重叠会让剪辑时对不齐口型"))

        no_anchor, no_id = [], {}
        for fr in frags:
            if "风格锚点" not in fr["prompt"]:
                no_anchor.append(fr["id"])
            named = [p for p in profiles if p and p in fr["visual"]]
            if named and "Character ID" not in fr["prompt"]:
                for p in named:
                    no_id[p] = no_id.get(p, 0) + 1
            for m in re.finditer(r"Character ID[:：]\s*([A-Za-z_]+)", fr["prompt"]):
                id_chars.setdefault(m.group(1), set()).update(named)
                for p in named:
                    char_hits.setdefault(p, {"anchored": 0, "bare": 0})["anchored"] += 1
            for p in named:
                char_hits.setdefault(p, {"anchored": 0, "bare": 0})
                if "Character ID" not in fr["prompt"]:
                    char_hits[p]["bare"] += 1

        # P2 风格锚点缺失（按集聚合）
        if no_anchor:
            findings.append(Finding(
                "🔴", "P2", f"第{n}集_完整版.md",
                f"{len(no_anchor)}/{len(frags)} 个碎片的 AI 提示词缺少风格锚点前缀：{'、'.join(no_anchor[:8])}"
                + ("…" if len(no_anchor) > 8 else ""),
                "补统一 Style Anchor（只写渲染介质+完成度，禁写题材/时代/服装内容词）——无锚点=跨镜头画风崩"))

        # P3 角色未锚定（按集聚合 + 给出缺哪个角色几次）
        if no_id:
            detail = "、".join(f"{k}×{v}" for k, v in sorted(no_id.items(), key=lambda x: -x[1]))
            findings.append(Finding(
                "🟡", "P3", f"第{n}集_完整版.md",
                f"{sum(no_id.values())} 个碎片画面出现角色但提示词无 Character ID 锚定（{detail}）",
                "为这些碎片补 `Character ID: <拼音大写>`，同一角色跨集复用同一ID——"
                "纯文字描述的角色在跨集生成时必然漂移"))

    # P4 项目级：哪些角色从头到尾一次都没拿到 Character ID
    never = [p for p in profiles if char_hits.get(p, {}).get("anchored", 0) == 0]
    if never:
        findings.append(Finding(
            "🔴", "P4", "分集文件（全项目）",
            f"角色「{'、'.join(never)}」在全部剧集中从未出现 Character ID 锚定",
            "这些角色下集起必须补 ID 并写入角色档案的「身份不变量」区，"
            "否则它们是最早崩的一批"))
    if id_chars:
        findings.append(Finding(
            "🟢", "P4", "分集文件（全项目）",
            f"在用 Character ID {len(id_chars)} 个：{'、'.join(sorted(id_chars))}",
            ""))


# ---------------------------------------------------------------- 主流程

def run(project: Path):
    findings = []
    if not project.is_dir():
        return [Finding("🔴", "X0", str(project), "项目目录不存在", "检查路径")]

    txt = {}
    for p in sorted(project.glob("*.md")):
        txt[p.name] = read_text(p)
    txt["__dir__"] = str(project)

    profiles, latest = check_memory(txt, findings)
    fh = parse_foreshadow_table(txt.get("伏笔表.md", ""))
    check_foreshadow(fh, latest, findings)
    check_relations(txt, fh, findings)
    check_characters(txt, profiles, latest, findings)
    check_episodes(project, profiles, findings)
    return findings


def main():
    ap = argparse.ArgumentParser(description="ManjuForge 跨文件一致性检查器")
    ap.add_argument("project", nargs="?", default=str(Path(__file__).resolve().parent.parent / "demo"))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="只显示 🔴🟡")
    args = ap.parse_args()

    project = Path(args.project)
    findings = run(project)

    red = [f for f in findings if f.level == "🔴"]
    yellow = [f for f in findings if f.level == "🟡"]
    green = [f for f in findings if f.level == "🟢"]

    if args.json:
        print(json.dumps({"project": str(project),
                          "red": len(red), "yellow": len(yellow), "green": len(green),
                          "findings": [f.to_dict() for f in findings]},
                         ensure_ascii=False, indent=2))
        return 1 if red else 0

    print(f"ManjuForge 一致性检查 · {project}")
    print("=" * 68)
    for label, group in (("🔴 必须修复（跨文件矛盾）", red),
                         ("🟡 建议修复", yellow),
                         ("🟢 通过", green)):
        if not group:
            continue
        if args.quiet and label.startswith("🟢"):
            continue
        print(f"\n{label}  ({len(group)})")
        for f in group:
            print(f"  [{f.code}] {f.where}")
            print(f"       问题：{f.problem}")
            if f.fix:
                print(f"       修法：{f.fix}")
    print("\n" + "-" * 68)
    print(f"合计 {len(findings)} 项：🔴 {len(red)} · 🟡 {len(yellow)} · 🟢 {len(green)}")
    if red:
        print("存在 🔴 跨文件矛盾 → 未通过，修复后再进入下一集。")
    return 1 if red else 0


if __name__ == "__main__":
    sys.exit(main())
