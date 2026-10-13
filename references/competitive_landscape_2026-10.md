# 竞品调研存档：2026-10 开源 AI 短剧/漫剧市场全景

> 调研日期：2026-10-13 ｜ 方法：GitHub API（`gh api`）实证元数据 + README/tree 深读，非二手转述
> **结论先行**：市场在最近 3 个月完成形态换代——**我们的护城河（长篇连载记忆）依然无人做，但"机检门禁"和"参考图生成"已变成行业标配，我们落后一个身位。**
> 上一次调研（DramaClaw 3.3k）到本次（6.9k），三个头部 skill 套件从 0 涨到 4.4k/2.8k/1.2k——**skill 形态的窗口在关闭，必须补工程完成度。**

---

## 一、项目概况（事实核查表）

三层层级已清晰分化。**同一层内才是直接竞争关系。**

### L1 全栈平台层（不是我们的战场，但决定评委的认知基线）

| 项目 | ★ | 创建 | 最后推送 | License | 形态关键点 |
|---|---|---|---|---|---|
| HBAI-Ltd/Toonflow-app | 17,387 | 2026-01-29 | 2026-10-12 | MIT | 无限画布 + AI Agent + MCP + 插件体系；桌面/移动/服务端三端；21 种界面语言 |
| chatfire-AI/huobao-drama | 16,109 | 2026-01-05 | 2026-10-05 | **CC BY-NC-SA 4.0** | Mastra 4 Agent（script_rewriter/extractor/storyboard_breaker/prompt_generator）；`workspace/skills/` 可在 UI 内编辑 |
| waooAI/waoowaoo | 14,538 | — | 2026-09-21 | — | "好莱坞式工作流"，卖点是过程可控而非抽卡 |
| HKUDS/ViMax | 12,640 | 2025-03-30 | 2026-09-30 | MIT | **港大数据智能实验室**，有 arXiv 论文；直击"角色漂移/只有画面没有叙事结构" |
| dramaclaw/dramaclaw | 6,862 | 2026-03-27 | 2026-10-12 | Elastic 2.0 | 已调研过（上次 3.3k → 翻倍）；要求 UI 角落保留 "Powered by DramaClaw" |
| Forget-C/Jellyfish | 6,709 | 2026-03-06 | 2026-07-30 | Apache-2.0 | 剧本→结构化分镜→一致性管理→镜头准备→出片→导出 |
| ArcReel/ArcReel | 5,453 | 2026-02-07 | 2026-10-12 | AGPL-3.0 | 卖点三条：角色一致 / 过程可控 / **成本可追踪**；**导出剪映草稿**；有覆盖率徽章 + Docker |

### L2 Skill 套件层（正面战场）

| 项目 | ★ | 创建 | 推送 | License | 形态 |
|---|---|---|---|---|---|
| eternityspring/shuohao-skills | **4,456** | 2026-08-06 | 2026-10-08 | Apache-2.0 | 6 skill；有商业工作室 studio.reelbenchai.com；**14 道脚本校验门禁** |
| zenstory-ai/drama-skills | **2,789** | 2026-07-16 | 2026-10-03 | MIT | **12 skill**；有公司 zenstory.ai；含剪辑 + 生产确认闸门；已上 ClawHub |
| lixiaoxiao9888-create/manju-laoli-skill | 1,158 | 2026-08-15 | 2026-10-12 | MIT | 单 Skill **41 个规则模块** 49 文件，V6.9.8；机检 C1~C20 / H1~H12 |
| smixs/visual-skills | 505 | 2026-04-26 | 2026-09-16 | CC-BY-4.0 | 2 skill：导演戏剧学（Murch/走位/蒙太奇）+ **反 AI 味禁用词表** |
| VanGong1999/screen-creative-skills | 452 | 2026-01-10 | 2026-10-12 | MIT | **31 个评估类 skill**（剧本/大纲/IP/小说评分），v2.2.0 |
| suihe1/short-drama-production | 182 | 2026-08-30 | — | — | 短剧生产总控，默认 16:9 |
| phileiny/h3-storyboard-skill | 176 | 2026-08-26 | — | — | MiniMax H3 镜头拆分 + 角色表演 |
| machina-exm/film-studio-skills | 148 | 2026-08-14 | 2026-08-14 | **无 License** | 7 skill；**README 明确写了 Hermes 安装方式** |
| ADC1920/AI-short-play-video-creation | 1 | 2026-10-02 | 2026-10-12 | MIT | 小但机制锐利（见三·D） |

### L3 索引/知识库

- `zhaotoday/awesome-ai-video`（25★，2026-09-15）：按 Star 降序收录短剧/漫剧产线、Agent 框架与 Skills、云厂商智剪 API。**做行业背景资料时这是最快的入口。**

---

## 二、能力拆解：市场做对了什么

### 1. 全链路已经标准化为同一套阶段划分

所有人的管线都是：`原著/点子 → 大纲 → 角色与场景资产 → 剧本 → 分镜 → 图片提示词 → 视频提示词 → 生产 → 剪辑成片 → 审查`

差别只在**切几个 skill**、**每个阶段的产物是什么格式**、**门禁卡在哪一站**。

### 2. "先预览、确认、再生产"已成为行业共识

- drama-skills：`任何图片、视频、配音或音乐任务，都先在文件里看到这一批准确的内容和参数，明确确认后才调用外部接口花钱`
- ManjuForge v1.8.0 的 adapter 四步确认闸门（建 job → prepare 预览 → 明确确认 → run）

**两边独立收敛到同一设计 = 这个方向是对的，不是我们想多了。**

### 3. 自包含 + 可单独安装的 skill 目录约定

shuohao 的仓库约定（可直接照抄）：

```
skills/<skill-name>/
├── SKILL.md          the workflow the agent reads (required)
├── README.md         the docs a human reads
├── scripts/
│   ├── <name>.mjs    deterministic helpers, zero dependencies
│   └── selftest.mjs  self-test, never calls a model (required)
├── references/       detailed instructions, loaded on demand
├── examples/         bundled samples that double as test fixtures
└── assets/           screenshots
```

**硬性两条**：每个 skill 必须有 `SKILL.md`；每个 skill 必须有 `scripts/selftest`，**不调模型、不耗额度**，覆盖全部确定性逻辑。无 CI——因为自测 1 秒跑完。

---

## 三、核心机制深度拆解（最有价值的发现放最前）

### A. `drama-skills` —— 最直接对标，工程完成度最高

**A1 跨文档引用完整性机检（我们最大的差距）**

`creator_markdown_check.py` 核对五份文档之间的引用，**报的是原因和修法，不是"校验失败"**。原文报错示例：

```
ERROR: SHOT-EP001-002: 冻结关键帧提示词写到人物「周薄森」，视觉依据没有覆盖；
       本镜确实看不见时在视觉依据末尾加「；画外：人物「周薄森」」，正文里这个名字不可靠时
       在《视觉设定.md》写「画面代称：无」
ERROR: SHOT-EP001-003: 分镜时长 2 秒与视频提示词 3 秒不一致；视频提示词只能原样照抄已接受的镜头时长
```

**A2 连续性锁 `LOCK-*`**：跨镜保持项写成"能原样贴进提示词的短语"，锁面就是锁定内容本身：

```
- 连续性锁：LOCK-JIANGCHEN-DRESS《江晨松枝绿常服》
  （镜头：SHOT-EP001-002、SHOT-EP001-003…；图片提示词项：IMG-JIANGCHEN-SHEET）
  · 锁面：pine-green lapel service jacket
```

每镜必须声明依据了哪些锁；漏了机检报错。**比"Character ID"强的地方：ID 只是索引，锁面是可执行内容。**

**A3 三态令牌 `IMG-` / `PLAN-` / `REF-`**：区分"我自己的图 / 计划中但未提供 / 已实际核对过"。防幻觉硬机制。

**A4 五份 Markdown = 创作事实**：`剧本.md` / `视觉设定.md` / `分镜.md` / `图片提示词.md` / `视频提示词.md` + `剪辑单.md`。没有并行数据库，改哪份文件就是改哪一层决定。

**A5 冻结关键帧**：分镜只冻结**起点那一格**，视频提示词只写起点→终点之间的动作。

**A6 剪辑技能逐段写入出点理由**，字幕逐字取自剧本，统一响度后渲染。

**工程实践**：`.agents/notes/` 存 ADR（架构决策记录）；`evaluations/content-quality-cases/` 8 个失败案例；`docs/real-outputs.md` 放真实产出节选；`.clawhub/publish.json` + CI 发布 ClawHub。

### B. `shuohao-skills` —— 最像我们，且更工程化

**B1 `character-refs` 是真生成参考图**（我们只有"槽位声明"）：一句描述 → 拆字段 → 补缺并确认 → **先生成正面全身锚点图** → 其他视图（头像/90°侧面/背面/细节）**只参考锚点** → 按需分级 → 每张单独可重生成 + **staleness 追踪**。后端可选：自建 ComfyUI(Qwen Image) / codex 生图 / GPT Image 2 API / 自定义命令。

**B2 `novel-art` 美术圣经**：场景 + 叙事道具的**一致性锚点、光照与状态变体、比例参考**。

**B3 `novel-outline` 14 道质量门禁全是脚本校验**，且带 checkup 模式复核已有大纲。

**B4 输出语言中文优先**，validator **主动拒绝英文字段**。

### C. `manju-laoli-skill` —— 规则深度最接近我们（41 模块）

值得我们没有的模块：`facs-au-dictionary` / `facs-emotion-recipes`（面部动作编码 → 表情可控化）、`lighting-and-antifake`、`platform-safety-compliance-guide`、`action-previs-15grid`、`dialogue-doctor-7d`、`asset-spatial-ledger`、`production-ledger-handbook`、`combat-direction-engine`、`screenplay-gate-engine`。

### D. 两个小而锐的发现

- **`ADC1920/AI-short-play-video-creation`**：**人脸审核规避五法**（墨镜遮挡/网格遮挡/无五官三视图/服装+头部组合/风格转绘）；**人物锚点法 + ref 数量红线 + 候选图选择制 + 首帧重构图规范**；**宫格分镜直生 4/6/9/25**；`validate_storyboard.py`（词数/字符上限/**必含排除词**/禁用句式/编号重复）+ `make_grid.py` 本地拼宫格 + `check_refs.py` 断链引用核对。
- **`smixs/visual-skills`**：**禁用词表**（`cinematic` `epic` `stunning` `masterpiece` 一律禁）；`dramaturgy.md` 把 Murch 剪辑理论压成 5-30 秒可执行规则；`de-slop.md`；各模型精确语法（Seedance 2.5 / Kling 3.0 Turbo+Omni / Veo / Sora / Runway / Pika / Luma / Nanobanana）。
- **`machina-exm/film-studio-skills`**（无 License，只借思路）：**资产护照**——"一个资产一本护照，逐字复制进每一个提示词"；四定律 "Lock assets first · one asset, one passport · surgical one-line edits · log everything"；`stress-test` 是拒绝放行不一致产物的门禁 skill。
- **`shuyu-labs/BigBanana-AI-Director`**（CC BY-NC-SA）：**Script-to-Asset-to-Keyframe** 工作流，明确反对"抽卡式生成"——先把角色和场景资产锁死，再用首尾关键帧控制镜头；镜头九宫格。
- **`woanderingboy/novel-video-pipeline`**（MIT，低星但概念对齐）：五站式 + **IP 防火墙**（negative-ip 令牌强制覆盖）+ **站间门禁** `validate_pipeline.py --strict --child`；默认横屏 16:9 漫剧产线。

---

## 四、与自家产品能力对照表（诚实打分 1-10）

| 维度 | ManjuForge v1.8.0 | 头部竞品 | 判定 |
|---|---|---|---|
| 长篇连载记忆（圣经/关系图/伏笔） | **9** | 0-2（三家全部缺失） | 🔵 护城河成立 |
| 跨集节奏方法论（信任曲线/势力升级） | 8 | 3 | 🔵 领先 |
| 钩子 / 心理触发点库 | 8 | 4 | 🔵 领先 |
| 风格模板 + 分镜规范 | 8 | 8 | ⚪ 持平 |
| **跨文件引用完整性机检** | **3** → 已升级 | 9 | 🔴 落后（本次补） |
| **参考图生成（锚点→多视图→可重生）** | **2** | 9 | 🔴 落后 |
| 资产护照 / 连续性锁 | 4 | 9 | 🔴 落后 |
| 剪辑 / 成片层 | 1 | 7 | 🔴 缺失 |
| 反 AI 味词表 | 3 | 8 | 🟡 落后 |
| 模型实测档案（FACS/审核/参数） | 2 | 8 | 🟡 落后 |
| 分发（ClawHub / skills.sh） | 1 | 7 | 🟡 落后 |

**判断**：我们用"记忆"赢前三个维度，用"工程完成度"输掉后五个。评委看 Demo 时，"不崩人设"是讲故事，**"机检能当场报出跨文件矛盾"是能演示的技术动作。**

---

## 五、可吸收改进点（按优先级）

### 🔴 直接落地

| # | 借鉴什么 | 来源 | 落到哪 | 状态 |
|---|---|---|---|---|
| 1 | **跨文件引用完整性检查器** - 伏笔清单双向一致 / 伏笔状态同步 / 悬空 F-ID / 关系型伏笔有落点 / 出场角色有快照 / 时间轴连续 | drama-skills `creator_markdown_check.py` | `scripts/consistency_check.py` | ✅ v1.9.0 已落地 |
| 2 | **参考图生成门** - 锚点图优先 → 其他视图只参考锚点 → 按需分级 → 单张可重生成 + staleness 追踪 | shuohao `character-refs` | 新 reference + 接入 adapter 契约 | 待做 |
| 3 | **资产护照** - 一资产一护照，逐字进提示词 | film-studio-skills | `角色档案.md` 模板 + Character ID 规范 | 待做 |
| 4 | **连续性锁 `LOCK-*` + 三态令牌 IMG/PLAN/REF** | drama-skills | `ai_execution_fields.md` 4.3/4.5 | 待做 |

### 🟡 规划期

5. 首尾关键帧字段（BigBanana Script-to-Asset-to-Keyframe）
6. 反 AI 味禁用词表（visual-skills）
7. 剪辑理论层文档：Murch 眨眼理论 / 走位 / 蒙太奇（visual-skills `dramaturgy.md`）
8. FACS AU 字典 + 情绪配方（manju-laoli）
9. 宫格分镜直生 4/6/9/25（ADC1920 + BigBanana 九宫格）
10. 平台审核合规专章（ADC1920 人脸审核规避五法 + manju-laoli `platform-safety-compliance-guide`）
11. 剪辑单 + 成片层（drama-skills `short-drama-edit`）
12. `scripts/selftest` 无模型自测纪律（shuohao 硬要求）
13. 失败案例库 `evaluations/content-quality-cases/`（drama-skills）
14. 模型实测档案（ADC1920 即梦 Seedance 2.5 CLI 实查 / drama-skills 模型行为探针）

### 🟢 存档备用

15. IP 防火墙 negative-ip 令牌（novel-video-pipeline）
16. 剪映草稿导出 + 费用追踪（ArcReel）
17. ClawHub + skills.sh 分发（drama-skills 已上 ClawHub）
18. `.agents/notes/` ADR 决策记录（drama-skills）

---

## 六、威胁评估 + 不做什么

### 威胁

| 项目 | 威胁度 | 它缺什么（我们的机会） |
|---|---|---|
| shuohao-skills 4.4k Apache-2.0 + 商业工作室 | **高** | 长篇连载记忆、Hook 公式库、心理触发点体系、抖音平台规则 |
| drama-skills 2.8k MIT + 公司 | **高** | 长篇连载记忆、Hook/心理/风格库 |
| manju-laoli-skill 1.2k MIT 41 模块 | **中高** | 长篇连载记忆（同样缺）、跨文件引用机检 |
| 全栈平台层（Toonflow/huobao/waoowaoo） | 低 | 形态完全不同，不抢同一批用户 |

**三家头部 skill 套件全部不做跨集记忆——护城河成立。但"记忆"单独撑不起一次迭代：必须补上机检与参考图两块标配，否则在"完成度"维度被反复压制。**

### 明确不做

- ❌ **不做全栈平台**（Toonflow / huobao 形态）——与定位冲突，也不是黑客松的赢法
- ❌ **不搬 CC BY-NC-SA 项目结构进商用产品**（huobao-drama、BigBanana）——非商用许可
- ❌ **不搬 Elastic 2.0 进 SaaS**（dramaclaw）——只借设计
- ❌ **不借无 License 项目的结构**（film-studio-skills）——只借概念
- ❌ **不抄 drama-skills 的"五份文档"结构**——那会丢掉七文件记忆这个唯一护城河
- ❌ **不做 SaaS / Web 美化 / 画布 / ComfyUI 集成**（与 6 个月聚焦策略一致）

---

## 一句话总结

**市场用三个月把"机检门禁 + 参考图生成"做成了标配，却始终没人做长篇连载记忆——我们的护城河是真的，但必须补上工程完成度才能守住它。**
