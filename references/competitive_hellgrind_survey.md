# 竞品调研存档：Hell-Grind-AIGC-Skill（Higgsfield HELL GRIND 社区剥离版）

> 调研日期：2026-08-07。结论先行：**它是"生产管理方法"，DramaClaw 是"生产工具"，我们是"创作方法论"。它最有价值的是模板工程化——特别是"身份不变量 vs 状态变量"二分，直接影响我们的 Character Graph 战略。**

---

## 一、项目概况（事实核查）

| 项 | 数据 |
|----|------|
| 原版 | higgsfield.ai/@higgsfield.studio/projects/hell-grind — 90分钟AI电影《HELL GRIND》，按场次公开全部提示词/角色资产/场景图/生成视频，免费无需注册 |
| 剥离版 | github.com/renmu2017/Hell-Grind-AIGC-Skill（2026-08-05创建，19 stars，MIT License） |
| 形态 | Codex 生态 Skill（agents/openai.yaml）+ 10阶段项目模板 + 3个Python脚本（init/validate/audit）+ 4个测试 |
| 定位 | 模型无关的 AIGC 视频生产工作流：项目搭建、资产与镜头管理、提示词生成与润色、生成记录、连续性检查、交付验收 |
| 规模 | 22个references专门指南 + 10阶段模板（00_brief→09_delivery）+ CSV表头体系 |

**LICENSE：MIT** —— 模板和思路可放心借鉴（注意：原版 HELL GRIND 的角色/资产/长提示词有版权，剥离版 SKILL.md 明确禁止复制到新项目）。

---

## 二、10 阶段项目模板结构

```
00_brief    brief.md + project.yaml          立项
01_story    story-bible.md                   故事圣经（4段式）
02_assets   assets.csv + asset-state-matrix.csv + reference-scope.csv   资产+状态+参考范围
03_scenes   scenes.csv + spatial-map.csv     场景+空间地图
04_shots    shots.csv + beat-sheet.csv + audio-cues.csv   镜头+节拍+音频提示
05_prompts  prompt-index.csv + prompt-template.md        提示词索引+模板
06_generations generation-log.csv + iteration-log.csv    生成记录+迭代记录
07_review   continuity-matrix.csv + qa-checklist.md + selection-log.csv + waivers.csv   连续性+QA+选择+豁免
08_edit     edit-notes.md                    剪辑
09_delivery delivery-checklist.md            交付验收
```

---

## 三、最有价值的模板设计（核心收获）

### 3.1 asset-state-matrix：身份不变量 vs 状态变量分离（🔴 最高价值）

```
asset_version_id, asset_id, version, state_name,
identity_invariants,    ← 锁死的：骨相/发型/体型/肤色（跨版本不变）
state_variables,        ← 可变的：情绪/姿势/服装状态/伤势
costume_or_surface, damage_or_weathering, carried_props,
reference_ids, approval_status, notes
```

**洞见**：角色资产必须显式区分"身份不变量"（永远锁死）和"状态变量"（逐镜头可变）。我们的角色档案是全文本描述，没有这个二分——这是 Character Graph 的胚胎设计。

### 3.2 story-bible.md：四段式故事圣经（🟡 直接对标战略）

```
# 故事圣经
## 世界规则    待填写
## 角色弧光    待填写
## 视觉母题    待填写
## 禁止变化    待填写    ← 妙：连续性的负面定义（什么绝不能变）
```

**洞见**："禁止变化"段落 = 连续性的负面定义。我们只有正向约束（角色档案说"必须这样"），没有负面清单（"绝不能那样"）。

### 3.3 reference-scope：参考图 8 维继承控制（🟢 4.5 的未来扩展）

```
reference_id, asset_id, source_path_or_url, rights_status,
inherit_identity, inherit_state, inherit_material, inherit_space,
inherit_composition, inherit_camera, inherit_lighting, inherit_color,
exclude, approval_status, notes
```

**洞见**：参考图继承细到 8 个维度（身份/状态/材质/空间/构图/机位/光照/色彩），每个维度独立开关 + exclude 排除列表。我们刚做的 4.5 参考图槽位只有 3 种粗模式（composite/portrait/prompt_only）——8 维是未来 Story Bible 视觉层的进阶。

### 3.4 continuity-matrix：逐镜头连续性追踪（🟢 参考）

```
shot_id, asset_version_ids, screen_direction, spatial_state,
costume_state, injury_state, prop_state, environment_state,
action_in, action_out, audio_state, open_issues, notes
```

13 列逐镜头追踪——我们是集级追踪（剧情摘要），镜头级对短剧过重，但"screen_direction/action_in/action_out"概念可借鉴。

### 3.5 spatial-map：空间分区+深度层（🟡 与我们的 Blocking 同构）

```
scene_id, zone_id, zone_name, screen_relation, depth_layer,
entry_exit, anchor_objects, allowed_assets, lighting_source, continuity_notes
```

与我们的 Blocking 文本俯视图同构，多了 depth_layer（深度层）和 allowed_assets（允许出现的资产）——前者对 2.5D/3D 场景有用。

---

## 四、与 ManjuForge / DramaClaw 对照

| 维度 | ManjuForge | DramaClaw | Hell-Grind |
|------|-----------|-----------|------------|
| 形态 | 创作方法论 Skill | 生产工具（引擎） | 生产管理方法 Skill |
| 叙事方法论 | ✅ 深度内置 | ❌ | ❌ |
| 提示词工程细节 | 🟡 已吸收DramaClaw 5点 | ✅ 58集验证 | ✅ 90分钟电影验证 |
| 项目管理模板 | ❌ markdown自由格式 | 🟡 | ✅ 10阶段CSV体系 |
| 资产版本管理 | ❌ | ✅ 资产库 | ✅ 版本矩阵+审批 |
| 连续性追踪 | 🟡 集级（剧情摘要） | 🟡 镜头级prompt | ✅ 镜头级矩阵 |
| 交付验收 | ❌（战略暂停） | ✅ | ✅ |
| 授权 | 开源 | Elastic 2.0（禁SaaS） | MIT |

---

## 五、可吸收的 3 个改进点（按优先级）

1. **🔴 角色档案增加"身份不变量/状态变量"二分**：升级 templates/character_template.md——锁死的（骨相/发型/体型/台词风格/性格核心）与可变的（情绪/状态/服装/关系阶段）显式分开。直接为 Character Graph 铺路。
2. **🟡 Story Bible 模板增加"禁止变化"段**：世界观/角色档案补负面清单（什么绝不能变/绝不能出现），与正向约束互补。Story Bible 战略落地时用四段式结构（世界规则/角色弧光/视觉母题/禁止变化）。
3. **🟢 存档 8 维继承与镜头级矩阵概念**：Story Bible 视觉层（参考图）落地时，4.5 的三种模式可扩展为继承维度控制。

**不做的**：不引入 10 阶段 CSV 体系（短剧项目过重）、不做镜头级追踪（集级足够）、不集成它作为依赖（19 stars 两天项目，抄概念不抄依赖）。

---

## 六、威胁评估

- 无直接威胁：Hell-Grind 面向"已有剧本的视频制作"，ManjuForge 面向"从零创作的内容创意"——上游关系，不是竞争
- 但注意：它是 Codex 生态（agents/openai.yaml），说明 AIGC 生产工作流正在"Skill 化"——与我们同赛道，验证了 Skill 形态是正确载体
- 它的 90 分钟电影级复杂度对短剧用户是负担，不构成卖点冲击

**一句话**：DramaClaw 给了我们提示词工程的细节，Hell-Grind 给了我们项目管理模板的骨架——两者都指向同一件事：Story Bible + Character Graph 是正确方向，且有现成工程化模板可借鉴。
