# 竞品调研：Seedance 2.0 Skill OS（Emily2040/seedance-2.0）

> 调研日期：2026-08-07 | 状态：已存档 | 来源：github.com/Emily2040/seedance-2.0（MIT）
> 结论速览：**"导演式提示词"是最大参考价值——直接升级 ManjuForge 的 AI 提示词范式；管线/多语言/电影级工作流不吸收。**

---

## 一、仓库验证（真实非空壳）

| 项 | 值 |
|----|----|
| 仓库 | Emily2040/seedance-2.0 |
| 描述 | Comprehensive production pipeline for quad-modal AI filmmaking with Seedance 2.0 |
| Stars / Forks | **6244 / 932**（目前调研项目最高热度，DramaClaw 3.3k 的 1.9 倍） |
| 协议 | **MIT**（真开源，可放心借鉴） |
| 创建 / 最后推送 | 2026-02-25 / 2026-08-06（活跃） |
| 版本 | v6.7.0（2026-08-05） |
| 定位 | Seedance 2.0（字节跳动视频模型）的"导演式"提示词 Skill 操作系统 |

## 二、核心理念：Direct the scene, don't decorate it

**"指挥场景，不要装饰它"**——大多数工具让模型生成"cinematic look"，导演式做法是：先问场景在*做什么*，再让 camera/lens/light/blocking/performance/sound 全部服务一个意图，用一个可识别的导演声音贯穿全片。

对比示例（README 原例）：
- **装饰式**：`epic cinematic shot of a woman reading a letter, emotional, beautiful lighting`
- **导演式**：`A woman at a kitchen table reads the letter twice, then her hands lower it and go still. Camera: medium close-up at eye level, a slow push-in that settles when her hands stop. Soft window light keeps her face plain. Sound: room tone, one chair scrape, near-silence — the realization lands in the stilled hands, not a word.`

**语序原则**：主体+动作占开头（模型先锁定"这段是谁在干什么"），camera/light/sound 跟随。
**情绪承载原则**：情绪靠可见动作承载（"the realization lands in the stilled hands, not a word"），不靠形容词堆叠。

## 三、核心机制拆解（与 ManjuForge 对照）

| Seedance 机制 | 内容 | ManjuForge 对照 | 吸收判断 |
|---------------|------|-----------------|----------|
| **Director's Read**（导演读场） | 每次叙事提示词前的强制判断：function/turn/POV/power shift/objective/obstacle/tactic/contradiction/一个可见的压抑行为/一个不可迁移细节/一个明确的类型拒绝 | 我们有六维评估（剧本级），但无"单镜头意图清单" | 🔴 精简版 6 要素接入分镜创作 |
| **Directing engine**（导演引擎） | 读场→camera/light/blocking/performance/sound 具体设置，拒绝"堆形容词" | 我们 4.3 提示词模板（Subject/Key visual details/Color/mood） | 🔴 "Direct it"语序原则直接升级 4.3 |
| **Reference role 分离** | 参考资产按角色绑定：identity/environment/motion/camera rhythm/audio tempo/style/endpoint | 我们 4.5 参考图槽位（composite/portrait/prompt_only） | 🟡 我们的 I2V 规则存档可参考其 motion 分离 |
| **five-verdict take triage** | 生成后五判定镜头筛选（保留/重拍/换方案等） | 无（AI视频暂停战略内） | 🟡 Flask 企业版/成片层的现成机制 |
| **one-variable retakes + attempt budgets** | 单变量重拍 + 尝试预算（不无脑重试） | 无 | 🟡 同上 |
| **source-dated platform facts** | 平台/模型事实带来源日期（API/价格/配额不猜） | 竞品调研存档惯例一致 | ✅ 原则确认 |
| **continuity ledgers**（连续性台账） | 跨镜头连续性管理 | Story Bible/Character Graph 同功能 | 🟢 对照设计参考 |
| 四模态管线（T2V/I2V/V2V/R2V/FLF2V） | Seedance 2.0 具体模型工作流 | 不集成具体模型（AI视频暂停） | ⛔ 不吸收 |
| 多语言（6语种） | 英/中/日/韩/西/俄 | 单语即可 | ⛔ 不吸收 |
| 专业电影工作流（ACES/color handoff/campaign cutdowns） | 电影级交付复杂度 | 短剧过重（同 Hell-Grind 10 阶段 CSV 判断） | ⛔ 不吸收 |

## 四、可吸收点分级（按 ManjuForge 优先级）

1. 🔴 **"Direct it" 语序 + 情绪承载原则** → `ai_execution_fields.md` 4.3 提示词模板升级：
   - 语序：主体动作开篇 → camera/light/sound 跟随（当前模板 Subject 字段增强）
   - 情绪：用"一个可见动作"承载（"realization lands in the stilled hands"），形容词降级为辅助
   - 影响面：全部分镜提示词（AI 执行版质量直接升级）
2. 🟡 **Director's Read 精简版（6 要素）** → 分镜创作流程加"单镜头意图"前置检查：
   - function（这个镜头干什么）/ objective（角色要什么）/ obstacle（障碍）/ contradiction（行为与心理矛盾）/ suppressed behavior（一个被压抑的行为）/ non-transferable detail（一个不可迁移细节）
   - 对应我们已确立的"行为否定+心理认可"高级手法（demo E2 母亲细节）——清单化后更可执行
3. 🟡 **生成后管理机制**（five-verdict/单变量重拍/尝试预算）→ 记录在案，留给 Flask 企业版（成片层）
4. ✅ **source-dated 原则** → 确认我们竞品调研惯例（事实可核验）

## 五、战略判断

**Seedance 2.0 Skill OS 验证了三件事：**
1. **"Skill 型 AI 视频工作流"是成熟高热度赛道**（6244 stars）——但它的卖点是"导演式提示词"，不是叙事方法论（没有伏笔引擎/记忆体系/连载管理）
2. **方法论正是它缺的**——Seedance Skill 教模型"怎么拍"，ManjuForge 教"拍什么、怎么连载"——互补不冲突
3. **不碰成片层也能做出高价值 Skill**——支持"AI视频暂停"战略（我们不做成片，做方法论，方法论正是这个 6244-star 项目缺的）

**行动**：调研存档（本文档）+ 4.3 模板升级（🔴）待用户确认后执行。
