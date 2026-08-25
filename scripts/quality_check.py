#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManjuForge 质量自检工具 (v1.6.0)
================================
一行命令跑完 18 项自动检查：开篇画面/标题欺诈/风格锚点/Character ID/
碎片时长/声音匹配/视觉锤/反派台词/关注引导/字幕卡/负向提示词/标题格式/
场景标记/跨时段过渡/参考图绑定/伏笔表健康/故事圣经健康/角色关系图健康。

用法:
    python scripts/quality_check.py <第X集_完整版.md> [--villain 反派名] [--json]

输出:
    🔴 未通过项（必须修复后才能进入下一集）   → 退出码 1
    🟡 待优化项                                → 退出码 0
    🟢 通过项

示例:
    python scripts/quality_check.py demo/第1集_完整版.md --villain 赵天赐
"""

import argparse
import json
import re
import sys
from pathlib import Path


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


def parse_fragments(text: str) -> list[dict]:
    """解析竖屏碎片时间轴表。识别包含 '→' 时间轴的表格行。"""
    frags = []
    for line in text.splitlines():
        if "→" not in line or not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        t = cells[2]  # 时间轴列
        m = re.match(r"(\d{1,2}):(\d{2})[→-]{1,2}(\d{1,2}):(\d{2})", t)
        if not m:
            continue
        start_s = int(m.group(1)) * 60 + int(m.group(2))
        end_s = int(m.group(3)) * 60 + int(m.group(4))
        frags.append({
            "id": cells[0],
            "time": t,
            "duration": end_s - start_s,
            "camera": cells[3],
            "visual": cells[4],
            "sound": cells[5],
            "prompt": cells[6],
        })
    return frags


def extract_title(text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def body_after_title(text: str, title: str) -> str:
    """去掉标题行和头部元信息（> 引用块）后的正文。"""
    body = text.replace(title, "", 1)
    body = re.sub(r"^>\s*[^\n]*\n", "", body, flags=re.MULTILINE)
    return body


def cjk_words(s: str) -> list[str]:
    """提取 CJK 连续片段中的 2-4 字关键词（滑窗去重），用于标题正文比对。"""
    runs = re.findall(r"[\u4e00-\u9fff]{2,}", s)
    out = set()
    for run in runs:
        if len(run) <= 4:
            out.add(run)
        for i in range(len(run) - 1):
            out.add(run[i:i + 2])      # 2字
            if i + 2 < len(run):
                out.add(run[i:i + 3])  # 3字
    # 过滤常见虚词，避免误报
    stop = {"一个", "这个", "那个", "什么", "怎么", "不是", "就是", "还是", "没有",
            "自己", "他们", "我们", "你们", "真的", "可以", "知道", "觉得", "因为"}
    return [w for w in out if w not in stop][:8]


# ---------------------------------------------------------------- 检查项

def check_open_visual(body: str, title: str) -> tuple[str, str]:
    """1. 开篇有画面：第一帧必须是具体画面，禁止黑屏开头。"""
    # 找开篇钩子段落
    m = re.search(r"【开篇钩子[^】]*】\s*\n+(.*?)(?=\n###|\n##|\n【[A-ZＡ-Ｚ])", body, re.DOTALL)
    segment = m.group(1) if m else body[:400]
    if "黑屏" in segment and not re.search(r"ECU|CU\b|特写|画面|镜头|场景", segment):
        return "🔴", "开篇黑屏：开篇钩子段落只有'黑屏'描述，无具体画面。第一帧必须是场景/角色/动作"
    if not re.search(r"ECU|CU\b|特写|画面|镜头|场景|MS\b|WS\b|正面|侧脸", segment[:200]):
        return "🟡", "开篇钩子段落未检测到明确的画面描述（ECU/特写/场景等），请确认第一帧有画面"
    return "🟢", "开篇第一帧有具体画面"


def check_title_honesty(text: str, title: str, body: str) -> tuple[str, str]:
    """2. 标题不欺诈：标题引用的台词/事件必须在本集中出现。"""
    quoted = re.findall(r"[“\"]([^”\"]{2,})[”\"]", title)
    if quoted:
        missing = [q for q in quoted if q not in text]
        if missing:
            return "🔴", f"标题引用台词未在正文出现：{missing}（标题欺诈=划走+取关）"
        return "🟢", "标题引用的台词已在正文兑现"
    # 无引号：取标题主体关键词做覆盖度粗检
    head = title.split("：", 1)[-1] if "：" in title else title
    words = cjk_words(head)
    if not words:
        return "🟢", "标题无可比对关键词"
    hit = sum(1 for w in words if w in body)
    ratio = hit / len(words)
    if ratio < 0.3:
        return "🟡", f"标题关键词在正文出现率仅 {ratio:.0%}（{hit}/{len(words)}），确认不是标题夸大"
    return "🟢", f"标题关键词覆盖度 {ratio:.0%}"


def parse_style_anchor(text: str) -> str:
    """解析分镜表上方的统一风格锚点声明（`风格锚点（所有提示词统一前缀）：` 后代码块）。"""
    m = re.search(r"风格锚点（所有提示词统一前缀）：\s*\n\s*>\s*`([^`]+)`", text)
    return m.group(1).strip() if m else ""


# Style Anchor 禁词：锚点只允许渲染介质+视觉完成度，内容词会污染所有镜头
# （covert content injection，见 knowledge_base/ai_execution_fields.md 4.4）
STYLE_ANCHOR_BANNED = [
    "drama", "romance", "melodrama", "thriller", "fantasy", "mythology",
    "historical", "ancient", "period", "dynasty", "campus", "palace",
    "hanfu", "school uniform", "modern elements",
    "古装", "民国", "校园", "宫廷", "玄幻", "古风", "甜宠", "虐恋", "悬疑",
]


def check_style_anchor(frags: list[dict], text: str = "") -> tuple[str, str]:
    """3. 风格锚点完整：所有提示词含统一 Style Anchor 前缀；锚点声明须 medium/grade-only。"""
    if not frags:
        return "🟡", "未解析到碎片表，跳过风格锚点检查"
    missing = [f["id"] for f in frags if "风格锚点" not in f["prompt"] and "style anchor" not in f["prompt"].lower()]
    if missing:
        return "🔴", f"以下碎片缺风格锚点前缀：{missing[:5]}{'…' if len(missing) > 5 else ''}（无锚点=跨镜头画风崩）"
    if not text:
        return "🟢", f"全部 {len(frags)} 个碎片含统一风格锚点标记"
    anchor = parse_style_anchor(text)
    if not anchor:
        return "🟡", "碎片含[风格锚点]标记但未找到统一前缀声明（建议在分镜表上方声明：> 风格锚点（所有提示词统一前缀）：> `...`）"
    banned_hits = []
    for w in STYLE_ANCHOR_BANNED:
        if re.search(r"[a-zA-Z]", w):
            if re.search(rf"\b{re.escape(w)}\b", anchor, re.IGNORECASE):
                banned_hits.append(w)
        elif w in anchor:
            banned_hits.append(w)
    if banned_hits:
        return "🔴", f"锚点含内容词：{banned_hits}。Style Anchor 必须只描述渲染介质+完成度，题材/时代/地点/服装/情绪词会注入每个碎片污染内容（如闪回现代被压制）。改为 medium-only 锚点，见 knowledge_base/ai_execution_fields.md 4.4"
    return "🟢", f"全部 {len(frags)} 个碎片含统一风格锚点，锚点内容符合 medium/grade-only"


def check_character_id(text: str, frags: list[dict]) -> tuple[str, str]:
    """4. Character ID 完整：角色出场碎片含 Character ID。"""
    ids = set(re.findall(r"Character ID:\s*([A-Z_]+)", text))
    if not ids:
        # 无任何 ID 但碎片里出现角色名（中文名字片段）→ 判定缺 ID
        name_hits = re.findall(r"[\u4e00-\u9fff]{2,3}(?:·[\u4e00-\u9fff]{2,4})?(?=：|（)", text)
        if frags and len(frags) >= 3:
            return "🔴", "全文件无任何 Character ID 锚定（角色跨集必变脸）"
        return "🟢", "无角色出场（或单集无角色），跳过"
    return "🟢", f"检测到 {len(ids)} 个 Character ID：{sorted(ids)}"


_FMT_PARAMS = {
    # 抖音竖屏短剧（默认）：平均3-7秒，>10秒🟡，>12秒🔴
    "vertical": {"avg_min": 3, "avg_max": 7, "warn": 10, "fail": 12, "label": "抖音快切节奏"},
    # 横屏AI番剧（优酷天作10分钟/集）：平均10-20秒，>30秒🟡，>45秒🔴
    "landscape": {"avg_min": 10, "avg_max": 20, "warn": 30, "fail": 45, "label": "横屏番剧节奏"},
}


def check_fragment_duration(frags: list[dict], fmt: str = "vertical") -> tuple[str, str]:
    """5. 碎片时长合格。vertical：平均3-7秒，>10秒🟡，>12秒🔴；landscape：平均10-20秒，>30秒🟡，>45秒🔴。"""
    if not frags:
        return "🟡", "未解析到碎片表，跳过时长检查"
    p = _FMT_PARAMS.get(fmt, _FMT_PARAMS["vertical"])
    durations = [f["duration"] for f in frags]
    avg = sum(durations) / len(durations)
    over_fail = [f["id"] for f in frags if f["duration"] > p["fail"]]
    over_warn = [f["id"] for f in frags if f["duration"] > p["warn"]]
    if over_fail or avg > p["avg_max"] * 1.15:
        return "🔴", f"碎片时长不合格：平均{avg:.1f}秒，超{p['fail']}秒碎片：{over_fail or '无'}（{p['label']}，须拆分）"
    if avg > p["avg_max"] or over_warn:
        return "🟡", f"碎片偏长：平均{avg:.1f}秒，超{p['warn']}秒碎片：{over_warn}（目标平均{p['avg_min']}-{p['avg_max']}秒，建议拆分）"
    if avg < p["avg_min"]:
        return "🟡", f"碎片偏短：平均{avg:.1f}秒（{p['label']}目标{p['avg_min']}-{p['avg_max']}秒，碎片过碎=节奏被快切带偏，建议合并）"
    return "🟢", f"碎片时长合格：平均{avg:.1f}秒（{len(frags)}个碎片，{p['label']}）"


def _script_zone(text: str) -> str:
    """提取剧本部分（## 剧本 与 ## 竖屏 之间）。分镜表的声音字段（🎵🔊💓🫧）不参与昼夜检测。"""
    if "## 剧本" in text:
        tail = text.split("## 剧本", 1)[-1]
    elif "## 竖屏" in text:
        return text.split("## 竖屏", 1)[0]  # 无剧本标记但有序幕区
    else:
        return text
    if "## 竖屏" in tail:
        return tail.split("## 竖屏", 1)[0]
    return tail


def _scene_segments(script: str) -> list[str]:
    """按场景标记切分剧本：'**场景：...**' 或 '### 【段标题' 为段边界。"""
    parts = re.split(r"\n(?=\*\*场景：|\n### 【)", script)
    return [p for p in parts if p.strip()]


def check_sound_time_match(text: str) -> tuple[str, str]:
    """6. 声音设计与场景时间匹配（仅剧本区·按场景段检测，避免跨场景误报）。"""
    hard_issues, soft_issues = [], []
    day_kw = ("清晨", "早晨", "晨光", "天亮", "破晓")
    night_kw = ("深夜", "夜晚", "夜半", "子时", "夜·", "夜，")
    candle_kw = ("烛火", "蜡烛", "灯芯", "油灯")
    bird_kw = ("鸟鸣", "鸡鸣")
    script = _script_zone(text)
    # 行级检测（硬冲突）：同一行内昼夜矛盾
    for line in script.splitlines():
        if any(k in line for k in day_kw) and any(k in line for k in candle_kw):
            hard_issues.append(f"L{text.count(chr(10), 0, text.find(line)) + 1}: 清晨场景出现烛火（清晨=鸟鸣+晨光）")
        if any(k in line for k in night_kw) and any(k in line for k in bird_kw):
            hard_issues.append(f"L{text.count(chr(10), 0, text.find(line)) + 1}: 夜晚场景出现鸟鸣/鸡鸣（夜晚=烛火+虫鸣）")
    # 场景段级检测（软提示）：同一场景段内昼夜关键词并存（跨场景段共存不算冲突）
    if not hard_issues:
        for i, seg in enumerate(_scene_segments(script)):
            seg_day = any(k in seg for k in day_kw)
            seg_candle = any(k in seg for k in candle_kw)
            seg_night = any(k in seg for k in night_kw)
            seg_bird = any(k in seg for k in bird_kw)
            if seg_day and seg_candle:
                soft_issues.append(f"场景段{i + 1}内同时出现清晨与烛火（确认是否同场景跨时段）")
            if seg_night and seg_bird:
                soft_issues.append(f"场景段{i + 1}内同时出现夜晚与鸟鸣（确认是否同场景跨时段）")
    if hard_issues:
        return "🔴", "；".join(hard_issues)
    if soft_issues:
        return "🟡", "；".join(soft_issues)
    return "🟢", "声音设计与场景时间匹配"


def check_visual_hammer(text: str) -> tuple[str, str]:
    """7. 有视觉锤：至少1个让观众截图的高光镜头。"""
    markers = ["视觉锤", "定格", "高光", "特写定格", "截图"]
    if any(m in text for m in markers):
        return "🟢", "存在视觉锤镜头标记"
    return "🟡", "未检测到视觉锤镜头（每集至少1个让观众截图的高光瞬间）"


def check_villain_line(text: str, villain: str | None) -> tuple[str, str]:
    """8. 反派有台词：反派出场时有台词（冷笑/狠话/沉默也行）。"""
    # 反派名字：优先用户指定，否则找配音文案中标记
    if not villain:
        m = re.search(r"反派[:：]\s*([\u4e00-\u9fff]{2,4})", text)
        villain = m.group(1) if m else None
    if not villain:
        return "🟢", "未指定反派，跳过（可加 --villain 参数检查）"
    no_line = re.search(
        rf"{re.escape(villain)}[^。\n]*?(本集无台词|无台词|没有台词|未出场)", text)
    if no_line:
        return "🟡", f"反派「{villain}」被标记为无台词/未出场（反派离场前必须有台词，一句冷笑/狠话即可）"
    if villain in text and not re.search(
            rf"{re.escape(villain)}[^\n]*[:：]", text):
        return "🟡", f"反派「{villain}」未检测到台词行"
    return "🟢", f"反派「{villain}」存在台词"


def check_follow_guide(text: str) -> tuple[str, str]:
    """9. 结尾有互动+关注引导。"""
    has_interact = bool(re.search(r"【结尾互动】|评论区|如果是你|你怎么", text))
    has_follow = bool(re.search(r"【关注引导】|关注[看播]?第?\d*集|关注看下集|下集", text))
    if has_interact and has_follow:
        return "🟢", "结尾含互动引导+关注引导"
    if has_follow:
        return "🟡", "有关注引导但缺互动引导（评论区开放式问题）"
    return "🟡", "结尾缺互动/关注引导（'评论区告诉我…'+'关注看下一集…'）"


def check_subtitle_card(text: str) -> tuple[str, str]:
    """10. 重要角色首次出场有字幕卡。"""
    if "字幕卡" in text:
        return "🟢", "存在角色字幕卡"
    return "🟡", "未检测到字幕卡（重要角色首次出场须标注姓名+身份）"


def check_negative_prompt(text: str) -> tuple[str, str]:
    """11. AI提示词含负向提示词。"""
    if re.search(r"NO text|NO watermark|no text|no watermark", text):
        return "🟢", "提示词含负向提示词（NO text / NO watermark）"
    return "🔴", "提示词缺负向提示词（须包含 NO text, NO watermark, NO modern elements）"


def check_title_format(title: str) -> tuple[str, str]:
    """12. 标题格式：悬念句/冲突句，禁止'第X集：XXX'。"""
    if re.match(r"^第\d+集[:：]", title):
        return "🟡", f"标题使用'第X集：'格式——规范要求悬念句/冲突句（如'赘婿被当众扇耳光，他忍了…'）"
    return "🟢", "标题为悬念句/冲突句格式"


def check_scene_markers(text: str) -> tuple[str, str]:
    """13. 剧本有场景标记。"""
    markers = re.findall(r"\*\*场景[:：][^*]*\*\*", text)
    if markers:
        return "🟢", f"场景标记完整（{len(markers)}处）"
    if re.search(r"场景[:：]|【[A-ZＡ-Ｚ]段", text):
        return "🟡", "场景标记不规范（建议 **场景：地点 时段 内/外**）"
    return "🟡", "未检测到场景标记"


def check_time_transition(text: str) -> tuple[str, str]:
    """14. 跨时段有过渡碎片。"""
    times = []
    for kw in ("清晨", "早晨", "晨光", "午后", "黄昏", "傍晚", "夜晚", "深夜", "夜半"):
        if kw in text:
            times.append(kw)
    if len(set(times)) >= 2 and not re.search(r"空镜|过渡|转场|日影移动|烛火点燃|时间流逝", text):
        return "🟡", f"检测到多个时段（{'/'.join(times)}）但无过渡碎片（空镜/日影移动/烛火点燃）"
    return "🟢", "时段单一或有过渡处理"


def check_reference_binding(text: str, frags: list[dict]) -> tuple[str, str]:
    """15. 参考图绑定提醒：角色出场碎片建议绑定角色参考图（🟡 不强制）。"""
    if not frags:
        return "🟡", "未解析到碎片表，跳过参考图检查"
    has_char = any("Character ID" in f["prompt"] for f in frags)
    if not has_char:
        return "🟢", "本集无角色出场（或未用Character ID），跳过"
    if re.search(r"角色参考图|参考图[:：]|Image\s*\d+", text):
        return "🟢", "已绑定角色参考图（槽位声明或提示词内引用，参考图=最高一致性保障）"
    return "🟡", "有角色出场但未绑定角色参考图。纯文字 Character ID 一致性天花板低，建议在分镜表上方声明：> 角色参考图：Image 1=角色名（正脸设定图）。见 knowledge_base/ai_execution_fields.md 4.5（暂无参考图可暂用文字锚定）"


def _episode_num(s: str) -> int:
    """从 'E3' / '第3集' / '3' 提取集数。"""
    if not s:
        return 0
    m = re.search(r"E(\d+)|第(\d+)集|^(\d+)$", s)
    return int(m.group(1) or m.group(2) or m.group(3)) if m else 0


def parse_foreshadow_table(text: str) -> list[dict]:
    """解析伏笔表（Markdown 表格，伏笔ID格式 F0xx）。"""
    rows = []
    for line in text.splitlines():
        if not line.strip().startswith("|") or not re.search(r"\|\s*F\d+", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        rows.append({
            "id": cells[0],
            "content": cells[1],
            "type": cells[2],
            "plant": cells[3],
            "importance": cells[4],
            "status": cells[5],
            "plan": cells[6] if len(cells) > 6 else "",
            "collect": cells[7] if len(cells) > 7 else "",
            "recent": cells[8] if len(cells) > 8 else "",
            "notes": cells[10] if len(cells) > 10 else "",
        })
    return rows


def check_foreshadow_table(text: str) -> tuple[str, str]:
    """16. 伏笔表健康检查（Foreshadow Engine）：ID唯一/状态合法/回收一致/发酵窗口。"""
    rows = parse_foreshadow_table(text)
    if not rows:
        return "🟡", "未解析到伏笔表条目（需 --foreshadow 指定伏笔表路径，ID格式 F0xx）"
    reds, yellows = [], []
    ids = [r["id"] for r in rows]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        reds.append(f"重复ID {dup}")
    for r in rows:
        st = r["status"]
        if st not in ("已埋", "活跃", "已回收", "已废弃"):
            reds.append(f"{r['id']} 状态非法:{st}")
            continue
        plant, collect = _episode_num(r["plant"]), _episode_num(r["collect"])
        if st == "已回收":
            if not r["collect"]:
                reds.append(f"{r['id']} 已回收但缺实际回收集")
            elif collect <= plant:
                reds.append(f"{r['id']} 回收集({r['collect']})≤埋设集({r['plant']})")
            elif collect - plant < 2:
                yellows.append(f"{r['id']} 发酵窗口不足(仅隔{collect-plant}集,应≥2)")
        elif st == "已废弃" and not r["notes"]:
            yellows.append(f"{r['id']} 已废弃但无备注理由")
    if reds:
        return "🔴", "伏笔表：" + "；".join(reds[:4])
    if yellows:
        return "🟡", "伏笔表：" + "；".join(yellows[:4])
    return "🟢", f"伏笔表健康（{len(rows)}条：ID唯一/状态合法/回收一致）"


def check_story_bible(text: str) -> tuple[str, str]:
    """17. 故事圣经健康（Story Bible）：四段齐全/视觉母题完整/禁止变化非空。"""
    if not text.strip():
        return "🟡", "未提供故事圣经（需 --bible 指定路径）"
    sections = ["世界规则", "角色弧光", "视觉母题", "禁止变化"]
    missing = [s for s in sections if f"## {s}" not in text and f"## 一、{s}" not in text]
    if missing:
        return "🔴", f"故事圣经缺段落：{missing}（四段式：世界规则/角色弧光/视觉母题/禁止变化）"
    reds, yellows = [], []
    def _zone(t: str, header: str) -> str:
        """提取某 ## 段内容，到下一个行首 ##（非 ###）段落为止。"""
        if header not in t:
            return ""
        return re.split(r"\n## (?!#)", t.split(header, 1)[-1], maxsplit=1)[0]
    # 视觉母题：只在 ## 视觉母题 段内找符号行
    motif_zone = _zone(text, "## 视觉母题")
    if "| 符号 |" in motif_zone and "| 类型 |" in motif_zone:
        motif_rows = [l for l in motif_zone.splitlines() if l.strip().startswith("|") and re.search(r"\|\s*E\d+", l)]
        if not motif_rows and "无符号" not in motif_zone:
            reds.append("视觉母题表为空（无符号登记；若本剧无符号系统请注明'本剧无符号'）")
        else:
            incomplete = [l.split("|")[1].strip() for l in motif_rows if len([c for c in l.strip().strip("|").split("|")]) < 6]
            if incomplete:
                yellows.append(f"母题字段不完整：{incomplete[:3]}")
    elif "视觉母题" in text:
        yellows.append("无视觉母题表（建议建立全剧符号系统）")
    # 禁止变化非空
    forbid_zone = _zone(text, "## 禁止变化")
    if forbid_zone.strip() and not any(l.strip().startswith("- ") for l in forbid_zone.splitlines()):
        yellows.append("禁止变化段为空（世界级+角色级至少各1条）")
    # 主线脉络：表头含"当前进度" 且 主线A/B 行第3列非空
    main_zone = _zone(text, "## 主线脉络")
    if "| 主线 |" in main_zone:
        if "当前进度" not in main_zone.split("---", 1)[0]:
            yellows.append("主线脉络缺'当前进度'列")
        else:
            empty_progress = [l.split("|")[1].strip() for l in main_zone.splitlines()
                              if l.strip().startswith("|") and re.search(r"主线[A-Z]", l)
                              and len([c for c in l.strip().strip("|").split("|")]) > 2
                              and not [c for c in l.strip().strip("|").split("|")][2].strip()]
            if empty_progress:
                yellows.append(f"主线缺当前进度：{empty_progress[:3]}")
    if reds:
        return "🔴", "故事圣经：" + "；".join(reds[:3])
    if yellows:
        return "🟡", "故事圣经：" + "；".join(yellows[:3])
    return "🟢", "故事圣经健康（四段齐全+母题完整+禁令已填）"


def parse_relation_matrix(text: str) -> tuple[list[str], list[list[str]]]:
    """解析关系矩阵：返回 (角色列表, 单元格二维表)。只在 ## 关系矩阵 段内解析，跳过表头/分隔行。"""
    if "## 关系矩阵" in text:
        text = re.split(r"\n## (?!#)", text.split("## 关系矩阵", 1)[-1], maxsplit=1)[0]
    header, rows = [], []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # 跳过 markdown 分隔行（|---|）
        if cells and all(re.fullmatch(r"-{2,}", c or "-") for c in cells):
            continue
        if cells and cells[0] == "角色":
            header = cells[1:]
            continue
        if header and len(cells) == len(header) + 1 and cells[0] not in ("—", "-"):
            rows.append(cells)
    return header, rows


def check_character_graph(text: str) -> tuple[str, str]:
    """18. 角色关系图健康（Character Graph）：矩阵对称/事件完整/信任无突变。"""
    if not text.strip():
        return "🟡", "未提供角色关系图（需 --graph 指定路径）"
    reds, yellows = [], []
    header, rows = parse_relation_matrix(text)
    if len(header) < 2:
        yellows.append("关系矩阵角色数<2（单角色矩阵无意义）")
    else:
        names = [r[0] for r in rows]
        for i, name_i in enumerate(names):
            for j, name_j in enumerate(names):
                if i == j:
                    continue
                a = rows[i][j + 1] if len(rows[i]) > j + 1 else ""
                b = rows[j][i + 1] if len(rows[j]) > i + 1 else ""
                if bool(a) != bool(b):
                    reds.append(f"矩阵不对称：{name_i}→{name_j} 有/无 与反向不一致")
                    break
            if reds:
                break
    if "关系事件时间线" not in text:
        yellows.append("无关系事件时间线（关系变化必须有事件记录）")
    else:
        events = [l for l in text.splitlines() if l.strip().startswith("|") and re.search(r"\|\s*E\d+", l)]
        if not events:
            yellows.append("事件时间线为空（每集至少1对关系推进）")
        else:
            for l in events:
                m = re.search(r"(\d+)→(\d+)", l)
                if m and int(m.group(2)) - int(m.group(1)) > 20:
                    reds.append(f"单集信任突变>20：{l.split('|')[1].strip()}")
                    break
    if reds:
        return "🔴", "关系图：" + "；".join(reds[:3])
    if yellows:
        return "🟡", "关系图：" + "；".join(yellows[:3])
    return "🟢", f"关系图健康（{len(header)}角色矩阵对称+事件完整）"


# ---------------------------------------------------------------- 主流程

CHECKS = [
    ("开篇有画面", check_open_visual, 0),
    ("标题不欺诈", check_title_honesty, 0),
    ("风格锚点完整", check_style_anchor, 0),
    ("Character ID完整", check_character_id, 0),
    ("碎片时长合格", check_fragment_duration, 0),
    ("声音设计匹配", check_sound_time_match, 0),
    ("有视觉锤", check_visual_hammer, 0),
    ("反派有台词", check_villain_line, 0),
    ("互动+关注引导", check_follow_guide, 0),
    ("有角色字幕卡", check_subtitle_card, 0),
    ("负向提示词", check_negative_prompt, 0),
    ("标题格式", check_title_format, 0),
    ("场景标记", check_scene_markers, 0),
    ("跨时段过渡", check_time_transition, 0),
    ("参考图绑定", check_reference_binding, 0),
    ("伏笔表健康", check_foreshadow_table, 0),
    ("故事圣经健康", check_story_bible, 0),
    ("角色关系图健康", check_character_graph, 0),
]


def run_checks(path: Path, villain: str | None, foreshadow_path: str | None = None,
               bible_path: str | None = None, graph_path: str | None = None,
               fmt: str = "vertical") -> tuple[list, list, list]:
    text = read_text(path)
    title = extract_title(text)
    body = body_after_title(text, title)
    frags = parse_fragments(text)

    def _read_if(p: str | None) -> str:
        if p:
            fp = Path(p)
            if fp.exists():
                return read_text(fp)
        return ""

    foreshadow_text = _read_if(foreshadow_path)
    bible_text = _read_if(bible_path)
    graph_text = _read_if(graph_path)

    passed, warned, failed = [], [], []
    dispatch = {
        "开篇有画面": lambda: check_open_visual(body, title),
        "标题不欺诈": lambda: check_title_honesty(text, title, body),
        "风格锚点完整": lambda: check_style_anchor(frags, text),
        "Character ID完整": lambda: check_character_id(text, frags),
        "碎片时长合格": lambda: check_fragment_duration(frags, fmt),
        "反派有台词": lambda: check_villain_line(text, villain),
        "参考图绑定": lambda: check_reference_binding(text, frags),
        "伏笔表健康": lambda: check_foreshadow_table(foreshadow_text),
        "故事圣经健康": lambda: check_story_bible(bible_text),
        "角色关系图健康": lambda: check_character_graph(graph_text),
    }
    for name, fn, _ in CHECKS:
        try:
            if name in dispatch:
                level, msg = dispatch[name]()
            else:
                level, msg = fn(text)
        except Exception as e:  # 单项异常不阻塞整体
            level, msg = "🟡", f"检查异常：{e}"
        if level == "🔴":
            failed.append((name, msg))
        elif level == "🟡":
            warned.append((name, msg))
        else:
            passed.append((name, msg))
    return passed, warned, failed


def render(passed, warned, failed, path: Path, json_out: bool) -> int:
    if json_out:
        print(json.dumps({
            "file": str(path),
            "passed": [{"item": n, "detail": m} for n, m in passed],
            "warned": [{"item": n, "detail": m} for n, m in warned],
            "failed": [{"item": n, "detail": m} for n, m in failed],
            "verdict": "FAIL" if failed else "PASS",
        }, ensure_ascii=False, indent=2))
        return 1 if failed else 0

    print(f"## {path.stem} 自检结果")
    if passed:
        print("🟢 通过项：")
        for n, m in passed:
            print(f"   ✓ {n} — {m}")
    if warned:
        print("🟡 待优化：")
        for n, m in warned:
            print(f"   △ {n} — {m}")
    if failed:
        print("🔴 未通过：")
        for n, m in failed:
            print(f"   ✗ {n} — {m}")
    verdict = "❌ 未通过（须修复所有🔴项才能进入下一集）" if failed else \
              ("⚠️ 通过（有🟡项建议优化）" if warned else "✅ 全部通过")
    print(f"\n判定：{verdict}")
    return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser(description="ManjuForge 质量自检工具")
    ap.add_argument("file", help="第X集_完整版.md 路径")
    ap.add_argument("--villain", default=None, help="反派角色名（检查其是否有台词）")
    ap.add_argument("--foreshadow", default=None, help="伏笔表.md 路径（Foreshadow Engine 健康检查）")
    ap.add_argument("--bible", default=None, help="故事圣经.md 路径（Story Bible 健康检查）")
    ap.add_argument("--graph", default=None, help="角色关系图.md 路径（Character Graph 健康检查）")
    ap.add_argument("--format", default="vertical", choices=["vertical", "landscape"],
                    help="碎片时长标准：vertical=抖音竖屏(平均3-7秒) landscape=横屏番剧(平均10-20秒，优酷天作10分钟/集)")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"错误：文件不存在 {path}", file=sys.stderr)
        return 2

    passed, warned, failed = run_checks(path, args.villain, args.foreshadow, args.bible, args.graph, args.format)
    return render(passed, warned, failed, path, args.json)


if __name__ == "__main__":
    sys.exit(main())
