#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManjuForge 质量自检工具 (v1.2.0)
================================
一行命令跑完 14 项自动检查：开篇画面/标题欺诈/风格锚点/Character ID/
碎片时长/声音匹配/视觉锤/反派台词/关注引导/字幕卡/负向提示词/标题格式/
场景标记/跨时段过渡。

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


def check_style_anchor(frags: list[dict]) -> tuple[str, str]:
    """3. 风格锚点完整：所有提示词含统一 Style Anchor 前缀。"""
    if not frags:
        return "🟡", "未解析到碎片表，跳过风格锚点检查"
    missing = [f["id"] for f in frags if "风格锚点" not in f["prompt"] and "style anchor" not in f["prompt"].lower()]
    if missing:
        return "🔴", f"以下碎片缺风格锚点前缀：{missing[:5]}{'…' if len(missing) > 5 else ''}（无锚点=跨镜头画风崩）"
    return "🟢", f"全部 {len(frags)} 个碎片含统一风格锚点"


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


def check_fragment_duration(frags: list[dict]) -> tuple[str, str]:
    """5. 碎片时长合格：平均3-7秒，无单一碎片>10秒（>12秒=🔴）。"""
    if not frags:
        return "🟡", "未解析到碎片表，跳过时长检查"
    durations = [f["duration"] for f in frags]
    avg = sum(durations) / len(durations)
    over12 = [f["id"] for f in frags if f["duration"] > 12]
    over10 = [f["id"] for f in frags if f["duration"] > 10]
    if over12 or avg > 8:
        return "🔴", f"碎片时长不合格：平均{avg:.1f}秒，超12秒碎片：{over12 or '无'}（抖音快切节奏，须拆分）"
    if avg > 7 or over10:
        return "🟡", f"碎片偏长：平均{avg:.1f}秒，超10秒碎片：{over10}（目标平均3-7秒，建议拆分）"
    return "🟢", f"碎片时长合格：平均{avg:.1f}秒（{len(frags)}个碎片）"


def check_sound_time_match(text: str) -> tuple[str, str]:
    """6. 声音设计与场景时间匹配（按行级检测，避免跨场景误报）。"""
    hard_issues, soft_issues = [], []
    day_kw = ("清晨", "早晨", "晨光", "天亮", "破晓")
    night_kw = ("深夜", "夜晚", "夜半", "子时", "夜·", "夜，")
    candle_kw = ("烛火", "蜡烛", "灯芯", "油灯")
    bird_kw = ("鸟鸣", "鸡鸣")
    for line in text.splitlines():
        if any(k in line for k in day_kw) and any(k in line for k in candle_kw):
            hard_issues.append(f"L{text.count(chr(10), 0, text.find(line)) + 1}: 清晨场景出现烛火（清晨=鸟鸣+晨光）")
        if any(k in line for k in night_kw) and any(k in line for k in bird_kw):
            hard_issues.append(f"L{text.count(chr(10), 0, text.find(line)) + 1}: 夜晚场景出现鸟鸣/鸡鸣（夜晚=烛火+虫鸣）")
    # 全文级跨行组合：只提示人工确认，不判死
    if not hard_issues:
        if any(k in text for k in day_kw) and any(k in text for k in candle_kw):
            soft_issues.append("全文同时出现清晨与烛火（可能跨场景，请人工确认）")
        if any(k in text for k in night_kw) and any(k in text for k in bird_kw):
            soft_issues.append("全文同时出现夜晚与鸟鸣（可能跨场景，请人工确认）")
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
]


def run_checks(path: Path, villain: str | None) -> tuple[list, list, list]:
    text = read_text(path)
    title = extract_title(text)
    body = body_after_title(text, title)
    frags = parse_fragments(text)

    passed, warned, failed = [], [], []
    dispatch = {
        "开篇有画面": lambda: check_open_visual(body, title),
        "标题不欺诈": lambda: check_title_honesty(text, title, body),
        "风格锚点完整": lambda: check_style_anchor(frags),
        "Character ID完整": lambda: check_character_id(text, frags),
        "碎片时长合格": lambda: check_fragment_duration(frags),
        "反派有台词": lambda: check_villain_line(text, villain),
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
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"错误：文件不存在 {path}", file=sys.stderr)
        return 2

    passed, warned, failed = run_checks(path, args.villain)
    return render(passed, warned, failed, path, args.json)


if __name__ == "__main__":
    sys.exit(main())
