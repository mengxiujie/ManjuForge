# ManjuForge｜漫剧铸造

**AI 漫剧连载创作引擎（Agent Skill：Hermes / Claude Code / Codex / Copilot 通用）**

> 别人做好看的单集，我们做活得久的 IP。

<p align="center">
  <a href="https://github.com/mengxiujie/ManjuForge">GitHub</a> |
  <a href="https://gitcode.com/gcw_LRlig9U4/manjuforge">GitCode（国内镜像）</a> |
  <a href="./README_EN.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-v1.8.0-brightgreen" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT--0-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Agent%20Skill-blue" alt="Platform">
  <img src="https://img.shields.io/badge/Standards-Agent%20Skills-8A2BE2" alt="Agent Skills">
  <img src="https://img.shields.io/badge/Episodes--Tested-11-orange" alt="Episodes">
  <img src="https://img.shields.io/badge/Foreshadow--Rate-100%25-orange" alt="Foreshadow">
</p>

---

## 📖 这是什么

ManjuForge 是一个 AI 漫剧**连载**创作工具，以标准 **Agent Skill**（SKILL.md）形态运行，可在 Hermes Agent、Claude Code、Codex、GitHub Copilot 及任何支持 Agent Skills 开放标准的运行环境中安装使用。

输入题材和人设，输出：**完整剧本 + 分镜（横屏16:9/竖屏9:16）+ 配音文案 + AI绘图提示词**。

核心解决一个问题：**连载30集以上，人设不崩、剧情不断、伏笔不丢。**

### 市场定位：画面一致 vs 叙事记忆

2026 年的 AI 短剧/漫剧工具大多在解决"**画面**一致"（角色/场景跨镜头不漂移），ManjuForge 解决的是"**故事**一致"：

| | 主流工作台（Jellyfish/ArcReel 等） | ManjuForge |
|---|---|---|
| 一致的对象 | 画面资产：角色/场景/道具/服装外观 | **叙事记忆**：人设/关系/伏笔/时间线/世界观 |
| 防的是 | 跨镜头漂移 | **跨集崩坏**（30集人设OOC/伏笔丢失/设定漂移/关系混乱） |
| 时间尺度 | 单镜→单集 | **单集→全剧**（跨集进化：视觉符号/信任曲线/关系阶段） |
| 载体 | 资产库+参考图 | 七记忆文件+三引擎（Story Bible/Character Graph/Foreshadow Engine） |

一句话：它们管画面不崩，我们管**故事不崩**。两者互补——ManjuForge 的提示词产出可直接喂给任何生成工作台。

---

## ✨ 实测验证

### Demo 一：《代码赘婿》6集完整创作（古风穿越爽剧）

| 集数 | 综合评分 | 第三方评分 |
|------|:--------:|:----------:|
| 1 | 7.8 | 88 |
| 2 | 7.8 | 92 |
| 3 | 8.3 | 95 |
| 4 | 8.2 | — |
| 5 | 8.1 | 97 |
| 6 | 8.3 | 96.5 |

验证结果：6集零崩坏｜伏笔回收率 100%（11根全回收/推进）｜第4集起双主线｜第6集从个人对抗升级阵营对抗。第三方评级（Character Memory / Relationship Graph / State Engine / Economic Logic / World Consistency / Narrative Engine 六项 A–A+，综合 A+）。

### Demo 二：《渊烬》第一单元 E1-5（从零跑通，非回顾性迁移）

- 质量曲线：E1 四处修复 → E2 一处 → E3-5 零修复（流程内化为习惯）
- 单集六维均值 **91.1/100**；单元七项评级 **6×A+ / 1×A**
- 三引擎实战：伏笔表 10 规划/5 激活、关系图 8 事件落地、信任曲线 0→15→20
- 实战新认知：**介质锚点**（跨集情绪差异大的剧，锚点只锁介质+完成度，光照为场景变量）

---

## 🔗 核心能力

### 连载记忆机制（七文件 + 三引擎）

| 记忆文件 | 解决 | 更新时机 |
|----------|------|----------|
| 角色档案 | 人设崩坏（身份不变量锁死/状态变量逐集更新） | 每集 |
| 世界观 | 设定漂移 | 首次+扩展时 |
| 场景布局 | 空间跳位（含光照状态字段，防跨时段崩） | 变更时 |
| 剧情摘要 | 剧情断层 | 每集 |
| 伏笔表 | 伏笔丢失（Foreshadow Engine：埋设→发酵→推进→回收） | 每集 |
| 故事圣经 | 记不住设定（Story Bible：四段式总纲，每5集刷新） | 每5集 |
| 角色关系图 | 记不住关系（Character Graph：矩阵+事件时间线，信任曲线） | 关系变化时 |

### 竖屏分镜（9:16 AI执行版）
- 碎片化时间轴（3-7秒/碎片）；横屏番剧（优酷天作类）另有 landscape 标准
- 声音四层标注（🎵音乐+🔊环境+💓生理+🫧细节）+ 跨时段声音匹配检查
- 风格锚点只锁介质（防内容词污染闪回/穿越）+ Character ID / Scene ID 跨集锁定
- Direct it 提示词范式（情绪靠可见动作承载，不堆形容词）

### 专业知识库
29 个专业参考文件 + 13 个拉片案例 + 6 大风格模板 + Hook 公式库（6型开篇+4型截断）+ 心理触发点体系：
- 拉片案例：盗梦空间/黑客帝国/千与千寻/你的名字/鬼灭之刃/进击的巨人/万神殿/中国奇谭/哪吒2/镖人/雾山五行/深海/灵笼/大鱼海棠
- 竖屏运镜字典、声音设计分层、AI 执行字段、平台适配（抖音竖屏/优酷横屏/红果）

### 自动质量自检
```bash
python scripts/quality_check.py demo/第1集_完整版.md --villain 赵天赐 --foreshadow demo/伏笔表.md --bible demo/故事圣经.md --graph demo/角色关系图.md
```
18 项检查（开篇画面/标题欺诈/风格锚点/Character ID/碎片时长/声音匹配/视觉锤/反派台词/互动引导/字幕卡/负向提示词/跨时段过渡/参考图绑定/伏笔表健康/故事圣经健康/角色关系图健康等），🔴 项自动拦截进入下一集，已在 11 集实战（6 Demo + 5 渊烬）验证。

### 生产执行纪律（v1.8.0）
提示词产出与生成后端**供应商解耦**：任何跑图/跑视频动作经 adapter 层执行，遵守四步确认闸门（建边界 job → prepare 预览 → 明确确认 → run，重试需重新确认，防失控成本）。详见 `references/adapter-contract.md`。

---

## 🚀 安装

> 安装目录名必须是小写 `manjuforge`（Agent Skills 规范要求 SKILL.md 的 `name` 与父目录名一致）。

### Hermes Agent
```bash
git clone https://github.com/mengxiujie/ManjuForge.git ~/.hermes/skills/creative/manjuforge
```
在 Hermes 对话中说"我想用 ManjuForge 创作一部漫剧"，然后告诉它题材、平台、画幅、集数、核心卖点。

### Claude Code
```bash
git clone https://github.com/mengxiujie/ManjuForge.git && cd ManjuForge
mkdir -p ~/.claude/skills && ln -s "$PWD" ~/.claude/skills/manjuforge
```
或在 Claude Code 对话中直接说：`安装这些技能 https://github.com/mengxiujie/ManjuForge`

### Codex（OpenAI）
```bash
git clone https://github.com/mengxiujie/ManjuForge.git && cd ManjuForge
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills" && ln -s "$PWD" "${CODEX_HOME:-$HOME/.codex}/skills/manjuforge"
```

### GitHub Copilot CLI / 跨客户端
```bash
# 项目级：把 SKILL.md 放入 .github/skills/manjuforge/ 或 .copilot/skills/manjuforge/
# 个人级：ln -s 到 ~/.copilot/skills/manjuforge
# 通用：复制到 ~/.agents/skills/manjuforge（跨客户端标准发现路径）
```

### 国内用户
GitHub 访问困难时用镜像：`git clone https://gitcode.com/gcw_LRlig9U4/manjuforge.git <同上目标目录>`

---

## 📁 项目结构

```
ManjuForge/                        # skill 目录（目录名=skill name）
├── SKILL.md                       # 核心定义（frontmatter: name/description/license/metadata）
├── skill.json                     # 元数据（版本/标签/模式）
├── prompt.core.txt                # 核心引擎规则（开源稳定版）
├── LICENSE                        # MIT-0
├── scripts/
│   └── quality_check.py           # 18项自动质量自检
├── templates/                     # 6个记忆模板
├── references/                    # 29个专业参考文件
│   ├── adapter-contract.md        # ★v1.8.0 供应商解耦+确认前置契约
│   ├── evaluation_framework.md    # 六维度评估体系
│   ├── hook_formula_library.md    # 六型Hook公式库
│   ├── knowledge_base/            # 拉片案例+AI执行规范
│   └── ...                        # 竞品调研/立项设计/优化日志
├── demo/                          # 6集《代码赘婿》完整Demo
└── docs/                          # 文档
```

---

## 📜 开源协议

MIT-0 License — 免费商用、无需署名、可闭源改造。

---

## 🤝 参与贡献

欢迎 Star、Fork、提 Issue。

有问题或建议 → [GitHub Issues](https://github.com/mengxiujie/ManjuForge/issues)

---

## 🧭 路线图信号（我们只回应真实需求）

ManjuForge 采用"开源 Skill 验证 → 观察信号 → 决定是否做企业版"的策略：
- ✅ 现在：持续迭代开源 Skill（叙事记忆方法论 + 拉片知识库是真正壁垒）
- ⏳ 观望：Star / Issue / 私信询盘信号足够后，再启动可视化工作台或企业版
- ❌ 不做：不追单集画质（那是视频模型层的事）、不做 Web 美化壳

你的 Star 和 Issue 就是路线图投票。
