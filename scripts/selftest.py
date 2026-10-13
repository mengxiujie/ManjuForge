#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManjuForge 检查器自测 (selftest.py)
===================================
两个检查器的确定性逻辑自测。**不调模型、不耗额度、不写 ~/.hermes**，
一秒内跑完，任何断言失败即退出码 1。

覆盖：
  纯函数   read_text / norm_name / name_match / epnum / stage_level / pair_key
           parse_tables / find_table / row_dict / get / parse_fragments
  一致性   构造一个"每类故障各一处"的临时项目，断言 22 项检查中可构造的部分全部触发；
           再断言一个干净项目不产生 🔴（防误报）
  质量     用构造的分镜片段断言 quality_check 的碎片解析与时长判定

用法:
    python scripts/selftest.py          # 全部自测
    python scripts/selftest.py -v       # 显示每项断言
"""

import argparse
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CC = _load("consistency_check")
QC = _load("quality_check")

PASS, FAIL = [], []


def check(label, cond, detail=""):
    (PASS if cond else FAIL).append(label)
    if VERBOSE:
        print(f"  {'✅' if cond else '❌'} {label}" + (f"  → {detail}" if detail and not cond else ""))


def codes(findings, level=None):
    return {f.code for f in findings if level is None or f.level == level}


# ---------------------------------------------------------------- 纯函数

def test_helpers():
    print("[纯函数]")
    check("norm_name 去括号与标点", CC.norm_name("林霜的家主令牌（掌权象征）") == "林霜的家主令牌")
    check("norm_name 去引号", CC.norm_name('沈舟"bug"口头禅') == "沈舟bug口头禅")
    check("name_match 同义名", CC.name_match("林霜对沈舟的态度变化（信任曲线）", "林霜对沈舟态度变化"))
    check("name_match 拒绝无关", not CC.name_match("沈舟的真实来历", "赵家买断蚕丝"))
    check("epnum 解析 E1/第5集/E20+", [CC.epnum(x) for x in ("E1", "第5集", "E20+")] == [1, 5, 20])
    check("epnum 空值返回 None", CC.epnum("—") is None and CC.epnum("长期") is None)

    lv = CC.stage_level("信任 45→60")
    check("stage_level 同义词归层(信任→托付层)", lv[0] == 4, str(lv))
    check("stage_level 无视→冷漠层", CC.stage_level("无视 0→0")[0] == 0)
    check("stage_level 敌对不算正向阶梯", CC.stage_level("公开敌对")[0] is None)
    check("stage_level 无匹配返回 (None,'')", CC.stage_level("疏远↓") == (None, ""))

    check("pair_key 顺序无关", CC.pair_key("林霜·沈舟") == CC.pair_key("沈舟-林霜"))
    check("pair_key 不同关系对不相等", CC.pair_key("沈舟-林霜") != CC.pair_key("沈舟-赵天赐"))

    t = "| 甲 | 乙 |\n|---|---|\n| 1 | 2 |\n\n| 丙 | 丁 |\n|---|---|\n| 3 | 4 |\n"
    tables = CC.parse_tables(t)
    check("parse_tables 解析两表", len(tables) == 2, str(len(tables)))
    h, r = CC.find_table(t, "丙", "丁")
    check("find_table 按关键词命中", h == ["丙", "丁"] and r == [["3", "4"]])
    check("row_dict 列不齐补空", CC.row_dict(["a", "b"], ["1"]) == {"a": "1", "b": ""})
    check("get 模糊取列", CC.get({"伏笔ID": "F1"}, "伏笔ID") == "F1")


def test_fragments():
    print("[分镜解析]")
    ep = (
        "| 号 | 段 | 时间轴 | 景别/运镜 | 画面描述 | 声音设计 | AI提示词/优先级 |\n"
        "|---|---|--------|-----------|----------|----------|----------------|\n"
        "| A1 | A | 00:00→00:04 | ECU·固定 | 甲拍桌 | 🔊声 | **P0** [风格锚点] shot, Character ID: JIA |\n"
        "| A2 | A | 00:06→00:10 | WS·固定 | 空镜 | 🔊声 | **P0** no anchor here |\n"
    )
    frags = CC.parse_fragments(ep)
    check("parse_fragments 解析两条", len(frags) == 2, str(len(frags)))
    check("parse_fragments 时间轴转秒", frags[0]["start"] == 0 and frags[0]["end"] == 4)
    check("parse_fragments 带 srt 头行被跳过", all(f["id"].startswith("A") for f in frags))

    qfrags = QC.parse_fragments(ep)
    check("quality_check 同样解析出两条", len(qfrags) == 2)
    check("quality_check 算出时长", qfrags[0]["duration"] == 4, str(qfrags[0].get("duration")))


# ---------------------------------------------------------------- 夹具

CLEAN = {
    "角色档案.md": """# 角色档案

## 基本信息

- **最后更新**：第2集创作后

## 核心角色

### 角色1：甲（男主）
- 文本
### 角色2：乙（女主）
- 文本
""",
    "世界观.md": """# 世界观

## 基本信息

- **最后更新**：第2集
""",
    "场景布局.md": """# 场景布局

## 基本信息

- **最后更新**：第2集
""",
    "剧情摘要.md": """# 剧情摘要

## 基本信息

- **最后更新**：第2集

## 关键伏笔追踪

| 伏笔 | 埋入集数 | 状态 | 备注 |
|------|----------|------|------|
| 甲的真实来历 | 第1集 | 🟡进行中 | |

## 人物状态快照

| 角色 | 当前状态 | 最后出场 | 关键变化 |
|------|----------|----------|----------|
| 甲 | 起 | 第1集 | 无 |
| 乙 | 起 | 第1集 | 无 |
""",
    "伏笔表.md": """# 伏笔表

## 基本信息

- **最后更新**：第2集创作后

## 伏笔总表

| 伏笔ID | 内容 | 类型 | 埋设集 | 重要度 | 状态 | 计划回收集 | 实际回收集 | 最近推进集 | 关联 | 备注 |
|--------|------|------|--------|:------:|------|:----------:|:----------:|:----------:|------|------|
| F001 | 甲的真实来历 | 人物型 | E1 | S | 活跃 | E20+ | — | E2 | 甲 | |
""",
    "故事圣经.md": """# 故事圣经

## 角色弧光（摘要，详情见 角色档案.md）

| 角色 | 身份不变量（3词） | 当前状态（变量） | 弧线终点 | 状态 |
|------|------------------|------------------|----------|------|
| 甲 | a/b/c | 起 | 成 | 活跃 |
| 乙 | a/b/c | 起 | 成 | 活跃 |

## 视觉母题（全剧符号系统）

| 符号 | 类型 | 首现集 | 当前进化态 | 关联角色 | 备注 |
|------|------|:------:|------------|----------|------|
| 令牌 | 道具 | E1 | 无 | 乙 | 见 F001 |
""",
    "角色关系图.md": """# 角色关系图

## 关系矩阵（当前状态快照）

| 角色 | 甲 | 乙 |
|------|------|------|
| 甲 | — | 夫妻·观察 |
| 乙 | 夫妻·观察 | — |

## 关系事件时间线

| 集数 | 关系对 | 事件 | 变化 | 类型 |
|------|--------|------|------|------|
| E1 | 甲-乙 | 初遇 | 冷漠 0→0 | 初始 |
| E2 | 甲-乙 | 相助 | 观察 0→15 | 推进↑ |
""",
    "第1集_完整版.md": """# 第1集：甲站起来

| 号 | 段 | 时间轴 | 景别/运镜 | 画面描述 | 声音设计 | AI提示词/优先级 |
|---|---|--------|-----------|----------|----------|----------------|
| A1 | A | 00:00→00:05 | ECU·固定 | 甲拍桌 | 🔊拍桌 | **P0** [风格锚点] shot, Character ID: JIA |
| A2 | A | 00:05→00:10 | MS·固定 | 乙回头 | 🔊风声 | **P0** [风格锚点] shot, Character ID: YI |
""",
}


def broken():
    """在干净夹具上，每类故障各埋一处。"""
    d = dict(CLEAN)
    del d["场景布局.md"]                                   # M1
    d["世界观.md"] = d["世界观.md"].replace("第2集", "第1集")   # M2
    d["剧情摘要.md"] = d["剧情摘要.md"].replace("第2集", "第10集")
    d["伏笔表.md"] = d["伏笔表.md"].replace("第2集创作后", "第10集创作后")
    d["故事圣经.md"] = d["故事圣经.md"].replace("第2集", "第10集")
    d["角色关系图.md"] = d["角色关系图.md"].replace("第2集", "第10集")

    d["剧情摘要.md"] = d["剧情摘要.md"].replace(
        "| 甲的真实来历 | 第1集 | 🟡进行中 | |",
        "| 甲的真实来历 | 第1集 | 🟡进行中 | |\n"
        "| 摘要独有的伏笔 | 第1集 | 🟡进行中 | |\n"                                  # M3
        "| 状态不符的伏笔 | 第1集 | 🟢已回收 | |")                                   # M4
    d["伏笔表.md"] = d["伏笔表.md"].replace(
        "| F001 | 甲的真实来历 | 人物型 | E1 | S | 活跃 | E20+ | — | E2 | 甲 | |",
        "| F001 | 甲的真实来历 | 人物型 | E1 | S | 活跃 | E20+ | — | E1 | 甲 | |\n"
        "| F001 | 重复ID | 人物型 | E1 | S | 活跃 | — | — | E1 | 甲 | |\n"          # F5
        "| F002 | 表独有伏笔 | 事件型 | E1 | S | 已回收 | — | — | E1 | 甲 | |\n"      # F2
        "| F003 | 快回收 | 事件型 | E1 | A | 已回收 | — | E2 | E2 | 甲 | |\n"          # F1
        "| F004 | 长期悬置 | 事件型 | E1 | A | 活跃 | — | — | E1 | 甲 | |\n"          # F3
        "| F005 | S级4 | 事件型 | E1 | S | 活跃 | — | — | E1 | 甲 | |\n"              # F4
        "| F006 | S级5 | 事件型 | E1 | S | 活跃 | — | — | E1 | 甲 | |\n"              # F4
        "| F007 | 关系型悬挂 | 关系型 | E1 | A | 活跃 | — | — | E1 | 甲·戊 | |\n"     # R4
        "| F008 | 状态不符的伏笔 | 事件型 | E1 | A | 活跃 | — | — | E1 | 甲 | |")      # M4
    d["故事圣经.md"] = d["故事圣经.md"].replace("见 F001", "见 F999")  # M5
    d["故事圣经.md"] = d["故事圣经.md"].replace(
        "| 乙 | a/b/c | 起 | 成 | 活跃 |",
        "| 乙 | a/b/c | 起 | 成 | 活跃 |\n| 丁 | a/b/c | 起 | 成 | 活跃 |")  # M6
    d["剧情摘要.md"] = d["剧情摘要.md"].replace(
        "| 乙 | 起 | 第1集 | 无 |",
        "| 乙 | 起 | 第1集 | 无 |\n| 戊 | 起 | 第1集 | 无 |")  # D1
    d["角色关系图.md"] = d["角色关系图.md"].replace(
        "| 乙 | 夫妻·观察 | — |", "| 乙 | 单方面·观察 | — |")  # R1
    d["角色关系图.md"] = d["角色关系图.md"].replace(
        "| E2 | 甲-乙 | 相助 | 观察 0→15 | 推进↑ |",
        "| E2 | 甲-乙 | 相助 | 观察 0→15 | 推进↑ |\n"
        "| E10 | 甲-乙 | 决裂再托付 | 托付 15→65 | 推进↑ |")   # R2 (跨级)
    d["角色关系图.md"] = d["角色关系图.md"].replace(
        "| E10 | 甲-乙 | 决裂再托付 | 托付 15→65 | 推进↑ |",
        "| E10 | 甲-乙 | 决裂再托付 | 托付 15→65 | 推进↑ |\n"
        "| E10 | 甲-丙 | 丙出场 | 敌对 | 转折↺ |")            # D2 (丙不在快照)
    d["剧情摘要.md"] = d["剧情摘要.md"].replace(
        "| 甲 | 起 | 第1集 | 无 |", "| 甲 | 起 | 第1集 | 无 |")  # 保持：甲在 ep1 里出现 ✓
    d["剧情摘要.md"] = d["剧情摘要.md"].replace(
        "| 乙 | 起 | 第1集 | 无 |", "| 乙 | 起 | 第3集 | 无 |")  # D3（第3集文件不存在→跳过）
    d["第1集_完整版.md"] = (
        "# 第1集：甲站起来\n\n"
        "| 号 | 段 | 时间轴 | 景别/运镜 | 画面描述 | 声音设计 | AI提示词/优先级 |\n"
        "|---|---|--------|-----------|----------|----------|----------------|\n"
        "| A1 | A | 00:00→00:05 | ECU·固定 | 甲拍桌 | 🔊拍桌 | **P0** [风格锚点] shot, Character ID: JIA |\n"
        "| A2 | A | 00:08→00:12 | WS·固定 | 甲走远 | 🔊脚步 | **P0** no anchor, no id |\n"
    )
    return d


def write_project(files):
    d = Path(tempfile.mkdtemp(prefix="mf-selftest-"))
    for name, body in files.items():
        (d / name).write_text(body, encoding="utf-8")
    return d


def test_consistency():
    print("[一致性检查器]")
    f = CC.run(write_project(broken()))
    got = codes(f, "🔴")
    got_all = codes(f)

    for c in ("M1", "M2", "M3", "M5", "M6", "D2", "R2", "P1", "P2"):
        check(f"{c} 触发", c in got_all, f"got={sorted(got_all)}")
    for c in ("M4", "M5", "F1", "F2", "F3", "F4", "F5", "R1", "R4", "D1"):
        check(f"{c} 触发", c in got_all, f"got={sorted(got_all)}")
    check("P3 触发（角色出现但无 Character ID）", "P3" in got_all)
    check("P4 触发（角色从未锚定）", "P4" in got_all, f"got={sorted(got_all)}")

    clean = CC.run(write_project(CLEAN))
    clean_red = codes(clean, "🔴")
    check("干净项目零 🔴（防误报）", not clean_red, f"误报={sorted(clean_red)}")
    check("干净项目仍报 🟢 项", any(x.level == "🟢" for x in clean))

    empty = CC.run(Path(tempfile.mkdtemp(prefix="mf-empty-")))
    check("空目录只报 M1", codes(empty) == {"M1"}, f"got={sorted(codes(empty))}")
    missing = CC.run(Path("C:/no/such/dir-mf-selftest"))
    check("不存在路径只报 X0", codes(missing) == {"X0"})


def test_counts():
    print("[项数收口自检]")
    src = (SCRIPTS / "consistency_check.py").read_text(encoding="utf-8")
    import re as _re
    found = set(_re.findall(r'"([MFRDP]\d)"', src))
    check("检查项数 = 22，与 SKILL.md/README 声称一致", len(found) == 22, f"实际 {len(found)}: {sorted(found)}")


def main():
    global VERBOSE
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    VERBOSE = a.verbose

    print("ManjuForge 检查器自测（不调模型，不耗额度）")
    print("=" * 60)
    for fn in (test_helpers, test_fragments, test_consistency, test_counts):
        fn()
        print()

    total = len(PASS) + len(FAIL)
    print("=" * 60)
    print(f"合计 {total} 项断言：通过 {len(PASS)} · 失败 {len(FAIL)}")
    if FAIL:
        print("\n失败项：")
        for x in FAIL:
            print(f"  ❌ {x}")
        return 1
    print("全部通过 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
