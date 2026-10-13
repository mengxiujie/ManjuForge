# Changelog

All notable changes to ManjuForge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.10.1] - 2026-10-13

### Added

- **README 首屏「30 秒了解 + 证据区」**：面向陌生读者（招聘方 / 评审 / 潜在用户）的前 10 秒。新增三块——「是什么/解决什么」两句话说明 + 「可以直接验证的东西」对照表（想知道 X 就打开 Y，会看到什么）+ 「规模与状态」。原文的问题是要翻三千字才知道这项目到底能干什么、有没有真东西。

### Changed

- 版本收口 1.10.0 → 1.10.1（SKILL.md frontmatter / skill.json / README 徽章 / README_EN 徽章）

### Notes

- 本轮优化动因：项目需作为**过往作品证明**用于简历与赛事材料。缺口不在能力（能力深度第 9 档），在**对外可读性**——GitHub topics 为空、项目描述是英文的 "manju script"（外人不知 manju 为何物）、无可点开的成品入口。故本轮只做门面，不做能力升级。
- 仓库元数据同步更新（GitHub topics + description），见仓库设置。

## [1.10.0] - 2026-10-13

### Added

- **`scripts/selftest.py` 检查器自测**（借鉴 eternityspring/shuohao-skills 4.5k★ 的工程纪律：每个 skill 必须有 `selftest`，**不调模型、不耗额度**）：47 项断言——纯函数（norm_name/name_match/epnum/stage_level/pair_key/parse_tables/row_dict）+ 分镜解析 + **构造"每类故障各埋一处"的临时项目，断言 22 项检查全部触发** + 干净项目零 🔴 防误报 + 空目录/不存在路径优雅降级 + **自动扫描源码校验"22 项"与文档一致**。一秒跑完，无需 CI。
  - 首次运行即抓出夹具自身的一处记忆矛盾（某角色在角色档案里却从未在任何分集出场 → D3/P4 正确报红），反证了"防误报"断言有效。
- **SKILL.md 新增「发布纪律」节**：5 条缺一不可的改动后检查——版本收口五处 / selftest 全绿 / 两个检查器跑 demo 并复核 🔴 非误报 / **prompt.core 同步必须 grep 新能力关键词而不只改版本号** / 全部副本 pairwise `diff -r --strip-trailing-cr` 零差异。

### Changed

- **SKILL.md 无损瘦身 −59 行**（717 → 658）：定位节 37 行营销备忘录压到 8 行（详情指针到 references）；实测踩坑记录 24 行表重构为「12 条已机器化不必人工核对 + 12 条语义类必人工核对」；Hook/心理触发点两个清单合并压缩；剧情摘要模板改指针到 `templates/plot_summary.md`；推广策略压缩为指针，腾出的位置换成新增的「发布纪律」节。
- **description 从 840 字符压到 79 字符**——这是每次加载都常驻的上下文开销。
- **三个孤儿 reference 归位**：`shanhai_landscape_epic_mode.md`、`tianzuo_2026_runtime_patch.md`（均标注「项目专项·不进公开仓库」）、`vibefilming-evaluation.md`（补进竞品调研组）。
- **检查项数收口**：19 / 17 / 22 三处不一致 → 统一为 **22**（M6 · F5 · R4 · D3 · P4），并在 selftest 内加断言防再次漂移。

### Fixed

- 1.9.0 条目曾把 22 项检查写成「19 项」——本版更正。
- `prompt.core.txt` 从 v1.7.4 补齐到 v1.10.0（补 adapter 契约 + 跨文件检查 + 发布纪律），修复该坑的第四次复发（v1.2 修过 → v1.6 回归 → v1.7.3 再修 → 再次落后）。

## [1.9.0] - 2026-10-13

### Added

- **跨文件一致性检查器 `scripts/consistency_check.py`**（借鉴 zenstory-ai/drama-skills 2.8k★ 的 `creator_markdown_check.py`）：**22 项检查分五组**——M 记忆文件层（七文件齐备 / 各文件"最后更新"集数一致 / 伏笔清单双向一致 / 伏笔状态同步 / 悬空 F-ID 引用 / 角色弧光覆盖档案）、F 伏笔表健康（回收发酵期≥2集 / 回收状态与字段不矛盾 / 悬置>8集 / S级≤3·A级≤5 并发 / ID 唯一）、R 关系图（矩阵对称 / 阶段不跳级 / 矩阵末态=时间线末态 / 关系型伏笔有落点）、D 人物状态（快照角色有档案 · 群像豁免 / **出场角色必须有快照** / "最后出场"必须真实）、P 分集层（**时间轴首尾相接** / 每碎片风格锚点 / 角色 Character ID / 项目级覆盖）。
  - **补的是 quality_check.py 查不到的一类事故**：前者只看单文件内部字段合不合规，查不出文件与文件互相矛盾——而那是记忆断裂的真实形态。
  - **报错范式**（照 drama-skills 抄）：每条问题同时给出「哪两个文件在哪一点上矛盾」+「怎么修」，不做只报"校验失败"的哑巴检查器。
  - **实测（6 集 Demo）当场抓出人工复核漏掉的三类事故**：`场景布局.md` 缺失；关系图 E6 记了林老太君在行会的戏、剧情摘要人物快照里却没这个人（出场了不登记=下集把她当没出现过）；7 处碎片时间轴空档 2-8 秒（成片黑场）。合计 18 项：🔴8 · 🟡7 · 🟢3。
  - 支持 `--json` 机读、`--quiet` 只显问题；空目录/不存在路径均优雅降级。
- **`references/competitive_landscape_2026-10.md` 开源市场全景调研**：三层格局实证（全栈平台 Toonflow 17.4k / huobao 16.1k / waoowaoo 14.5k / HKUDS-ViMax 12.6k；Skill 套件 shuohao 4.4k / drama-skills 2.8k / manju-laoli 1.2k）；三个直接竞品机制深拆；能力对照评分表；18 条分级吸收点（🔴4 / 🟡10 / 🟢4）。**下次迭代先读这个。**

### Changed

- SKILL.md 新增「跨文件一致性检查（v1.9.0 新增·必跑）」小节，明确 Step 4 同步完成后、进入下一集前必须跑一次
- 版本收口 1.8.0 → 1.9.0（SKILL.md frontmatter / skill.json / README 徽章 / README_EN 徽章）；references 计数 29 → 30

### Notes

- **战略验证**：三家头部 Skill 套件（shuohao 6 skill / drama-skills 12 skill / manju-laoli 41 模块）**全部不做长篇连载记忆**——Story Bible / Character Graph / Foreshadow Engine 仍是市场空白，护城河成立。
- **但**"机检门禁 + 参考图生成"已是行业标配，ManjuForge 在这两个维度落后一个身位；本版补上机检，参考图生成门列为下一优先级。

## [1.8.0] - 2026-09-07

### Added

- **Agent Skills 标准兼容层**（市场调研驱动：2026 技能分发已进入开放标准时代，agentskills.io 规范 + Claude Code/Codex/Copilot 全支持）：SKILL.md frontmatter 补 `license: MIT-0` + `metadata`（version/author），与 agentskills.io 规范字段对齐；确认 Hermes 解析兼容（name 与目录名 manjuforge 匹配）
- **README 多平台分发改造**：从"Hermes Skill"单一平台定位升级为"Agent Skill（Hermes / Claude Code / Codex / Copilot 通用）"；新增四平台一键安装指引 + GitCode 国内镜像；补"画面一致 vs 叙事记忆"市场定位对照表；badges 更新（v1.8.0 / Agent Skill / Agent Skills 标准）
- **README_EN.md 英文版**：面向海外短剧/动漫创作者的分发入口（此前纯中文，海外不可达）
- **生产执行纪律 + Adapter Contract**（借鉴 zenstory-ai/drama-skills 1632★ 真实产线实践）：SKILL.md 新增「生产执行纪律（供应商解耦 + 确认前置）」小节 + `references/adapter-contract.md` 完整契约——创作文件永不写死供应商、执行经 adapter profile 映射、四步确认闸门（建边界 job → prepare 预览 → 明确确认 → run，失败重试须重新确认，防失控成本）

### Fixed

- skill.json author 笔误 `mengxiuj` → `mengxiujie`；version 同步 1.8.0

### Notes

- 分支 `feat/skill-standard` 基于远端 v1.7.4（b7520e1）开发；本地桌面 main 旧 v1.3-v1.6 提交已备份至 `backup-local-v16`
- README references 计数改为 29（以目录实际为准防漂移）
- 市场调研结论存档：竞品量化（waoowaoo 14k★/inkos 9.6k★/Jellyfish 6.3k★/seedance-2.0 7.2k★/zenstory drama-skills 1.6k★ 等）——ManjuForge 差异化确认在"叙事记忆"（竞品全在做画面资产一致）

## [1.7.4] - 2026-08-29

### Fixed

- **四方副本残留文件清理**（例行维护）：安装副本 / 运行态 / 生产快照三处残留 v1.2.0 dedupe 时已从主副本删除的遗留文件——`references/pitfalls_log.md`（早期 13 条踩坑，已被 SKILL.md「实测踩坑记录」24 条表完全覆盖）、`references/storyboard-skill.md`（anime-storyboard-artist 完整复制，知识库已内化至 knowledge_base/ 且未被 SKILL.md 引用）。三方已清除，四方重新对齐
- **README references 计数校准**：30→28（保留「以目录实际为准」防漂移表述）

## [1.7.3] - 2026-08-25

### Fixed

- **prompt.core.txt 内外版本分裂修复**（P0，v1.2 识别的最严重问题复发）：核心引擎从 v1.6.0 同步至 v1.7.2 全能力——三平台参数化（抖音竖屏/优酷横屏 landscape/红果）、横屏 AI 执行版、场景布局光照状态字段（TIME-OF-DAY）、剧情摘要主线推进字段、Direct it 语序范式（4.3）、介质锚 vs 情绪锚决策（4.4.1）、自检表碎片时长双标准、知识库引用补山海专项
- **README references 计数修正**（P1）：26→30 个专题文件，表述改为"以目录实际为准"防再次漂移；拉片库口径修正为 13 个案例文件

### Added

- **模型适配建议**（P2，补齐评估缺口）：SKILL.md 新增强/中/弱模型分工表（强模型跑创作判断/弱模型做批量转换）、创作类更新必须强模型复核、成本策略

## [1.7.2] - 2026-08-25

### Added

- **场景布局"光照状态"字段**（DramaClaw TIME-OF-DAY 规则落地，存档项解冻）：每个场景记录 `time-of-day`（晨/日/暮/夜）、主光源方向与色温、特殊光照（烛火/冥火/天光）；锚点图固定光照只许局部调节，跨时段场景逐时段登记光照行，防 AI 生成"跨时段场景崩"
- **ai-sample-pipeline 存档项解冻**（属生产工作台，不在本仓库版本内）：`prompt-adaptation.md` 新增第六节 I2V 运动描述规则（首帧契约/单向运动链/禁静态镜头词/禁情绪标签/字数按时长缩放/失败回退，DramaClaw §3.5 存档解冻）；`qa-rework.md` 返工纪律新增"每次重拍只改一个变量"（Seedance five-verdict 纪律）

## [1.7.1] - 2026-08-25

### Added

- **横屏剧情型短剧适配正式并入产品**（此前在《山海》05_生产Skill 工作台独立存在，本轮三方合并）：
  - `references/platform_adaptation.md` — 平台适配层：抖音竖屏/优酷横屏番剧/红果三档参数化（画幅/单集时长/碎片时长/分发逻辑/标题/结尾/开篇钩子/声音设计/质量校验），创作前先锁定 `platform` 参数
  - `references/shanhai_landscape_epic_mode.md` — 《山海》横屏神话史诗专项模式（模式标识 `shanhai_landscape_epic`）：回应权主题北极星、禁互动引导、EP+集名标题、单集≥10分钟/全季≥150分钟
  - `references/tianzuo_2026_runtime_patch.md` — 优酷动漫"天作"计划2026运行时补丁：官方最低门槛（横屏/单集≥10min/≥10集/总≥150min/样片≥5min/投稿邮箱）、解释纪律（下限非固定值）、《山海》14集/152:00平台版锁定参数
  - `scripts/quality_check.py` — 新增 `--format landscape` 参数：碎片时长横屏标准（平均10-20秒，>30秒🟡，>45秒🔴）
  - `SKILL.md` — 竖屏碎片时长规范修正（10-15秒→平均3-7秒抖音标准+landscape 双标准，修复 v1.2 遗留矛盾）；质量自检引用加 `--format landscape`；知识库清单登记 platform_adaptation 与横屏史诗拉片案例
- **三方副本合并**：主副本（Git）/ 安装副本（Hermes 加载）/ 05_生产Skill 统一到 v1.7.1，demo 13文件、storyboard-skill.md、README 修正、LICENSE MIT-0 完整版三方对齐

## [1.7.0] - 2026-08-25

### Added

- **剧情摘要"主线推进"字段**（第三方评估遗留项落地）：
  - `templates/plot_summary.md` 全剧主线脉络升级为双主线表（主线A=外部冲突线 / 主线B=内心关系线，各带当前进度% + 下一节点）
  - 每集块新增"主线推进"记录字段（主线A/B 各自推进了什么、进度%变化）
  - `SKILL.md` 剧情摘要更新模板同步加字段；记忆连贯性自检清单新增 🔴 规则"第4集起必须激活主线B"（单主线到第8集会疲劳）
- **优化日志 v1.7.0 节**（`references/optimization-log-v1.2.md`）：三条候选点核查结论存档——主线B字段已落地 / 10集压力测试已由《渊烬》E1-10 真实完成（第二单元 7×A+，无记忆衰减）/ Hell-Grind 三点已全部落地；并登记横屏剧情型短剧适配为 v1.7 主菜（待方向确认）

## [1.6.0] - 2026-08-07

### Added

- **4.3 AI提示词模板 → Direct it 范式** in `ai_execution_fields.md` — absorbed from Seedance 2.0 Skill OS (Emily2040/seedance-2.0, MIT, 6.2k★, surveyed 2026-08-07, see `references/competitive_seedance_survey.md`):
  - **语序原则**: subject + one visible action beat opens the prompt (the model locks "who is doing what" first), then camera/light/sound follow, then technical specs.
  - **情绪承载原则**: emotion is carried by one visible action ("the realization lands in the stilled hands, not a word"); adjectives demoted to auxiliary.
  - Template now `[Style anchor], [Subject]+[action beat], [Camera: shot type+movement], [Light: source+quality], [Sound], [Color/mood via action], [Tech specs]` with decorative-vs-direct contrast examples (incl. wuxia-flavored example).

## [1.5.0] - 2026-08-07

### Added

- **《渊烬》实战验证（第一单元 E1-5）** — 用完整 7 文件流程从零跑通一部新剧（改编自同名小说第一卷），非 demo 回顾性迁移:
  - Quality curve: E1 4 fixes → E2 1 fix → E3-5 zero fixes (workflow internalized).
  - Per-episode six-dimension mean **91.1/100**; unit seven-dimension rating **6×A+ / 1×A**.
  - Engines battle-tested: foreshadow table 10 planned / 5 activated, character graph 8 events landed, trust curve 0→15→20.
  - 18 checks caught 4 real defect classes (fragment duration, title coverage, visual hammer, engagement guide).
- **4.4.1 锚点粒度决策（介质锚 vs 情绪锚）** in `ai_execution_fields.md` — from 《渊烬》practice: shows with strongly varying per-episode mood (war field → village → plague city) must use a media-only anchor (no lighting words); fixed lighting anchors would force every scene's mood (covert content injection, second form). Decision rule: single-tone mood curve → emotional anchor; multi-tone → media anchor.

### Changed

- **`quality_check.py` sound-time check → scene-segment granularity**: detection now runs on the script zone only (storyboard sound fields 🎵🔊 excluded) and warns only when day/night keywords coexist within the same `**场景：` segment — cross-scene morning/evening coexistence no longer false-positives (E5 real-world regression).
- **README / skill.json / prompt.core / CHANGELOG → v1.5.0**; README gained a "实战验证（《渊烬》E1-5）" section.

## [1.4.0] - 2026-08-07

### Added

- **Story Bible (v1.0)** — strategic pillar #1, "记不住设定":
  - `references/story_bible.md` — design doc: single source of truth overview (world rules summary / character arc table / visual-motif table / forbidden-changes digest + mainline tracker), refreshed every 5 episodes; visual motif table is the full-series symbol panorama complementing the foreshadow table's per-symbol lifecycle.
  - `templates/story_bible_template.md` + `demo/故事圣经.md` (4 roles, 3 motifs, world+character bans, A/B mainlines migrated from the 6-episode demo).
- **Character Graph (v1.0)** — strategic pillar #2, "记不住关系":
  - `references/character_graph.md` — design doc: relation matrix (current snapshot, symmetric, stage-tagged) + event timeline (change log), trust-curve pacing (E1-6 +10~15/ep, E7+ plateau), no stage skipping.
  - `templates/character_graph_template.md` + `demo/角色关系图.md` (4×4 matrix + 11 events; 沈舟-林霜 0→15→30→45→60→65 trust curve exactly on spec).
- **`quality_check.py` 16 → 18 checks**: "故事圣经健康" (`--bible`: 4-section completeness 🔴, empty motif table 🔴, incomplete motif fields 🟡, empty bans 🟡) and "角色关系图健康" (`--graph`: matrix asymmetry 🔴, trust jump >20 in one episode 🔴, missing timeline/events 🟡).

### Changed

- **SKILL.md**: memory system is now 7 files in two tiers (per-episode: character dossier/plot summary/foreshadow table/scene layout; overview: worldbuilding/story bible/character graph); initialization flow gained steps 6-7; self-check gained 3 items (bible refresh every 5 eps, graph update on relationship episodes, no stage skipping).
- **`prompt.core.txt` synced to v1.4.0**: 7-file memory table with tier split.
- **README / skill.json**: v1.4.0, 18 checks, Story Bible + Character Graph feature sections, 7-file memory claim.
- **All 3 strategic pillars now landed**: Foreshadow Engine (v1.3.0) + Story Bible + Character Graph (v1.4.0) — the 6-month focus is complete at the design-and-landing level.

## [1.3.0] - 2026-08-07

### Added

- **Foreshadow Engine (v1.0)** — the 3rd strategic pillar (Story Bible / Character Graph / Foreshadow Engine) is now formally designed and landed:
  - `references/foreshadow_engine.md` — design doc: foreshadow lifecycle state machine (planted → active → collected / abandoned / suspended), 7 foreshadow types (prop / line / character / event / setting / relationship / **symbol** — the symbol type emerged from demo evidence: the token / desk-tapping / "bug" catchphrase cross-episode evolution), fermentation window (collect ≥2 eps after planting), collection consistency (🔴 upgrade allowed, downgrade banned), density rules (1-2 planted + ≥1 advanced per episode), concurrency caps (S≤3 / A≤5).
  - `templates/foreshadow_template.md` — the 4th memory file template.
  - `demo/伏笔表.md` — all 12 real demo foreshadows migrated to full lifecycle tracking (F001-F012), including an honest fast-collect case (F008, E5→E6) that the checker flags as a 🟡 fermentation-window warning — checker and manual judgment agree.
- **`quality_check.py` 15 → 16 checks**: new "伏笔表健康" check (`--foreshadow <伏笔表.md>`): duplicate IDs 🔴, illegal status 🔴, collected-before-planted 🔴, collected-without-date 🔴, fermentation window <2 eps 🟡, discarded-without-reason 🟡. Verified live against the demo foreshadow table.

### Changed

- **SKILL.md**: memory mechanism is now 4 files (added 伏笔表.md); hard rules extended (foreshadow registration + collection consistency); per-episode workflow Step 4 now includes foreshadow-table sync; self-check checklist gained 3 foreshadow items.
- **`prompt.core.txt` synced to v1.3.0**: 4 memory files + foreshadow hard rules.
- **README / skill.json**: version v1.3.0, 16 checks, Foreshadow Engine feature section, 4-file memory claim.

## [1.2.1] - 2026-08-07

### Added

- **Style anchor pollution prevention** (`references/knowledge_base/ai_execution_fields.md` §4.4): anchors must be medium/grade-only — banned content words (historical/ancient/romance/hanfu/古装/民国/校园 etc.) that would covertly override legitimate content on every panel. Absorbed from DramaClaw (58-episode production pipeline). `quality_check.py` now parses the anchor declaration and flags banned words as 🔴.
- **Reference-image slot binding** (`ai_execution_fields.md` §4.5): Image N slot declaration + in-prompt references, three binding modes (composite / portrait / prompt_only). Absorbed from DramaClaw identity-lock mechanism. `quality_check.py` gained a 15th check (reference-binding 🟡 reminder, non-blocking).
- **Character dossier invariant/variant split** (`templates/character_template.md` rewrite + `demo/角色档案.md` migrated): identity invariants (locked: appearance anchors / personality core / dialogue style) vs state variables (per-episode: emotion / costume / injury / relationship stage) + "forbidden changes" negative checklist. Absorbed from Hell-Grind AIGC Skill (asset-state-matrix / story-bible design). `templates/worldbuilding_template.md` gained a "forbidden changes" section.
- **Competitor surveys archived**: `references/competitive_dramaclaw_survey.md` (open-source AIGC video engine, Elastic 2.0, 5 absorbable points) and `references/competitive_hellgrind_survey.md` (Higgsfield 90-min AI film skill extraction, MIT, 3 absorbable points).

### Changed

- **`scripts/quality_check.py` 14 → 15 checks**: style-anchor content validation (banned-word detection, 🔴) + new reference-binding reminder (🟡). Ad-hoc verified (17 assertions, both rounds green) plus full 6-episode demo pass without regressions.
- **`prompt.core.txt` synced to v1.2.1**: style-anchor pollution rules, reference-image slot guidance, negative-prompt correction (dropped `NO modern elements` content ban), updated self-check table. Fixes the internal/external rule drift first noted in v1.2.0.
- **`references/style_guide.md`**: all six style anchors rewritten medium/grade-only (content words removed).
- **`SKILL.md`**: anchor rules + self-check checklist + 15-check wording updated; memory-mechanism table documents the invariant/variant split.

## [1.2.0] - 2026-07-31

### Added

- **Automatic Quality Check Tool** (`scripts/quality_check.py`): One-command 14-item auto inspection (opening frame / title honesty / style anchor / Character ID / fragment duration / sound-time match / visual hammer / villain lines / follow-up guide / subtitle card / negative prompt / title format / scene marker / time transition). Parses real episode files, outputs 🔴🟡🟢 verdict, exits 1 when 🔴 items exist. Verified against all 6 demo episodes — automatically caught the real issue documented in pitfalls (Ep4-6 fragment duration creeping up to 7.6-7.8s).
- **prompt.core.txt upgraded to v1.2**: Added serial memory mechanism (character dossier / worldbuilding / plot summary constraints injection + summary update template), Hook formula library (6 opening types + 4 ending cliffhangers), psychological rhythm design, style anchor / Character ID / negative prompt rules, unified fragment duration (3-7s average, matching SKILL.md), title spec, subtitle card, ending guide rules, and 8 long-series pacing rules. Fixed the fragment duration contradiction between prompt.core (10-15s) and SKILL.md (3-7s).

### Changed

- **SKILL.md restructured**: 804 lines → 586 lines (-27%). Removed duplicated sections (batch mode ×2, pitfall records ×3, knowledge base index ×2, demo iteration workflow ×2, production workflow overlap ×3). Chapter numbering normalized (一~八, no jumps/duplicates). All pitfall records merged into one 24-item verified pitfall table.
- **References deduplicated**: removed `storyboard-skill.md` (stale anime-storyboard-artist copy, already internalized into knowledge_base/) and `pitfalls_log.md` (content merged into SKILL.md pitfall table). 18 → 16 reference files.
- **Iteration documentation**: added `references/optimization-log-v1.2.md` (reusable refactoring methodology + script development patterns + git merge lessons for future versions) and `references/competitive_shanyin_survey.md` (competitor survey archive: Shanyin Screenwriter 2.0 on SekoAI — closed-source, platform-exclusive, limited reference value). 16 → 18 reference files.

## [1.1.0] - 2026-07-02

### Added

- **Hook Formula Library** (`references/hook_formula_library.md`): 6 opening hook types (Conflict, Suspense, Emotional, Visual Hammer, Question, World-Building) + 4 ending cliffhanger types + platform-specific adaptation guide + practical checklists. Each hook type includes formulas, templates, examples, and high-frequency pitfalls.

- **Psychological Triggers System** (`references/psychological_triggers.md`): Information gap theory, emotional resonance mechanisms, cognitive load management, and addiction loop design for short-form drama retention. Includes per-episode psychological rhythm templates (Ep1-3/4-6/7-10/11-15 with different strategies).

- **Quality Checklist Integration**: Hook type verification and psychological trigger checks now integrated into the per-episode quality self-check workflow.

- **Competitive Analysis Notes** (`references/competitive_analysis_notes.md`): Comparative study against similar AI script generation tools, with actionable improvement directions.

### Changed

- **SKILL.md**: Creation workflow now requires explicit Hook type selection and psychological trigger design before generation.
- **README.md**: Updated to highlight new Hook Formula and Psychological Trigger capabilities.

## [1.0.0] - 2026-06-10

### Added

- **Core Skill (SKILL.md)**: Complete manju generation engine with cross-episode memory mechanism
- **Character Dossier Template**: Locks character design, relationships, and dialogue style across episodes
- **Worldbuilding Template**: Locks era, rules, factions, and spatial geography
- **Plot Summary Template**: Auto-updated log of key events, foreshadowing threads, and timeline
- **Vertical Storyboard System**: 9:16 format with fragmented timeline (3-7 seconds per fragment)
- **Four-Layer Sound Annotation**: Music, Environment, Physiological, and Detail sound layers
- **Quality Self-Check System**: Six-dimensional assessment (Script, Storyboard, Voiceover, AI Prompts, Memory Mechanism, TikTok Adaptation)
- **Style Guide**: 6 cinematic style templates (Inception, Your Name, Attack on Titan, and more)
- **Knowledge Base**: 13 film analysis case studies for reference
- **Vertical Cinematography Dictionary**: Camera angles, transitions, and framing specs for mobile-first content
- **Demo**: Complete 6-episode demo series "The Code Son-in-Law" with full output

### Verified Performance (6-Episode Demo)

| Metric | Result |
|--------|--------|
| Cross-episode Memory | Zero inconsistencies |
| Character Consistency | Main character retains defined traits |
| Foreshadowing Recovery | 100% (11 plot threads recovered/advanced) |
| Relationship Evolution | Progress shown through actions/spatial changes |
| Parallel Mainlines | Second mainline successfully introduced in Ep.4 |
| Faction Conflict Escalation | Escalates from personal to factional conflict |

### Technical Details

- Platform: Hermes Agent
- License: MIT-0 (No Attribution Required)
- Third-party evaluation: A+ across all dimensions
