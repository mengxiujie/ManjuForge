# 竞品调研存档：DramaClaw（dramaclaw/dramaclaw）

> 调研日期：2026-08-07。结论先行：**它是"生产工具"，我们是"创作方法论"。工具会免费化，方法论不会。但它的提示词系统工程化程度远超我们当前知识库，有 5 个可直接吸收的设计洞见。**

---

## 一、项目概况（事实核查）

| 项 | 数据 |
|----|------|
| 仓库 | github.com/dramaclaw/dramaclaw |
| 出品方 | Neo Flying AI Laboratory（成都新飞翔科技） |
| Stars / Forks | 3,329 / 287（2026-08-07，当日仍在推送） |
| 语言 | Python (FastAPI) + TypeScript (React) |
| 授权 | **Elastic License 2.0**（源码可用，非OSI开源） |
| 官网 | dramaclaw.ai，产品手册在飞书 |
| 生产实例 | 《天命不可欺》58集、《归灵司》《鲁班》《乌龙仙途》《师兄你怎么不舔了》 |

**Elastic 2.0 关键限制**：可免费使用/修改/自部署/做衍生，但**禁止作为托管服务提供给第三方**（不能 SaaS 化转售），不得移除 license key 功能，保留版权声明。

**技术栈**：本地零GPU（推理全走 OpenAI 兼容网关：官方 relayclaw 或 BYO），无 Postgres/Redis/Celery，SQLite+文件系统，Docker 一键起。模型：LLM 任意 / 图像 gpt-image·nano-banana / 视频 Seedance 系列 / TTS IndexTTS2 / 知识图谱 Cognee。

**架构亮点**：Ports & Adapters 六边形架构——CE 社区版/EE 企业版同一代码库，企业版只换适配器（多租户/RBAC/计费）。这是"Skill版→企业版"路线的现成作业。

---

## 二、管线全景

Ingest（小说解析→Cognee故事图）→ Plan（分集/beat规划）→ Produce（剧本→分镜→首帧→配音→视频）→ Deliver（合成导出+SRT+资产包）。每步独立可跳过可续跑。

---

## 三、提示词系统深度拆解（核心收获）

### 3.1 Style Preset 设计哲学（最值得吸收的洞见）

文件：`src/novelvideo/styles/presets/` + `STYLE_DESIGN.md`

每个风格预设是结构化 JSON，不是一行风格词：

```json
{
  "style_instructions": "拍摄/渲染/打光/调色指导（明确defer到beat/scene/character/prop内容）",
  "avoid_instructions": "只防介质和质量：禁动漫/3D/塑料皮肤/AI伪影/多肢/水印",
  "style_tag": "ANIME 或 NATURAL PHOTOREALISTIC, CLEAN GRADE",
  "label": "用户面名称（如 写实现代），不注入生成",
  "style_family": "animation / live_action"
}
```

**关键设计原则（我们缺失的）**：
1. **Style/Content 严格分离**：风格只控制"渲染介质+完成度"，绝不携带时代/地点/服装内容词。
2. **style_tag 禁止 era/content 词**（PERIOD/REPUBLICAN/古装/民国/DRAMA 全禁）——因为 style_tag 会重复出现在每个 Panel header（`- **Panel N** [loc] [tod] [STYLE_TAG]:`），带时代词=每帧悄悄覆盖合法内容（闪回手机、西服、灾难前干净场景）。这就是"covert era injection"。
3. **avoid_instructions 不硬禁故事内容**：现代物品/外国人/混血/穿越细节属于内容层，不能出现在 avoid 里。
4. **族裔只作 fallback**：角色明确描述/参考图 > 项目默认族裔。
5. 参考图自动分析出的自定义风格也必须遵守同样约束，否则重新引入 covert injection。

**对照 ManjuForge**：我们的 Style Anchor 只要求"统一前缀"，没有防"锚点内容污染"这层。我们的知识库风格锚点示例（如 "Chinese ancient mythology style"）其实**违反了 DramaClaw 的 style_tag 约束**——"ancient mythology" 是内容词，会污染所有镜头内容。这是必须修正的。

### 3.2 身份锁定：参考图驱动（CHARACTER IDENTITY LOCK）

文件：`prompt_builder.py::build_identity_lock`

- 角色有参考图才输出锁定块；无参考图返回空（**参考图是主角，不是可选项**）
- 逐项锁定：骨相/眼睛/鼻子/下颌线/肤色 "IDENTICAL, not similar"；情绪只变表情不变脸型
- 三种外观来源模式：
  - `composite`（合成参考板）：脸+体型+服装全从图
  - `portrait`：脸从图，体型从身份，服装从 WEAR 文字
  - `prompt_only`：全靠文字描述（最弱，尽量避免）

**对照 ManjuForge**：我们有 Character ID 锚定（`Character ID: SHENZHOU`）但输出物是文字描述。DramaClaw 证明**参考图绑定才是工业级答案**——升级路径：分镜输出的 AI 提示词增加"参考图槽位"（Image N）语义，引导用户先定角色参考图再生成。

### 3.3 颜色映射：草图阶段锁定角色（COLOR IDENTIFICATION MAP）

文件：`prompt_builder.py::build_color_identification_map`

- 草图（staging）阶段用颜色标记区分角色（红色人影=角色A），渲染时映射到参考图：
  `Any figure with a {color_name} tint (even pale/desaturated) = {tag}, MALE/FEMALE. ... Marker color is only an identity key, not clothing color.`
- 多身份支持：同一角色不同身份可配不同颜色
- 性别+体型 LOCKED

**对照 ManjuForge**：我们分镜没有"角色位置/颜色标记"层。这是"线稿→成图"管线才需要的能力；ManjuForge 输出到提示词层，可吸收为"角色识别锚点"建议（如在画面描述里标注"红衣者=女主"）。

### 3.4 场景/道具锚点（SCENE/PROP IDENTITY LOCK）

- 场景锚点锁定架构/材质/固定装置；time-of-day 只能改光照不能重新设计场地
- 道具锚点锁定剪影/比例/材质/磨损；beat 级措辞可加临时状态但不得换基物
- 道具 marker 颜色是连续性控制符，不是最终材质色
- TIME-OF-DAY RULE：区分"光照已烘培进锚点图"vs"按标签重新打光"的 panel

**对照 ManjuForge**：我们的 Scene ID + 场景布局（Blocking）是文本俯视图。DramaClaw 是图片锚点+光照规则。升级路径：场景布局文件可增加"锚点图槽位"和"光照状态"字段。

### 3.5 I2V 运动描述规则（视频层，暂不吸收但存档）

文件：`video_prompt_builder.py` / `keyframe_prompt_builder.py`

- **首帧契约**：首帧是 t=0，只描述其后发生的事；禁止描述首帧前动作
- 字数按时长缩放：≤4s→50-60字，5-6s→60-75字，≥7s→75-90字
- 禁止角色名→视觉特征（"the woman in black"）
- 禁止情绪标签→肢体语言；禁止非视觉感官（气味/温度）
- 禁止静态镜头词（holds/stays/static/locked）与静态主动词（freezes/stares/stands）
- **单向运动链**：2-3 个同向连续动作填满时长，禁止往返/振荡运动
- 中文、现在时、4-6句
- 失败回退：默认提示词（"角色姿态自然调整，镜头平稳跟随"）

---

## 四、与 ManjuForge 能力对照

| 维度 | ManjuForge | DramaClaw | 差距 |
|------|-----------|-----------|------|
| 叙事方法论（Hook/心理触发点/信任曲线/六维评估） | ✅ 深度内置 | ❌ 通用LLM驱动 | 我们领先（护城河） |
| 风格锚定 | 前缀词（有内容污染风险） | 结构化preset+防污染约束 | 落后，需修正 |
| 角色一致性 | Character ID 文字锚定 | 参考图+面部几何锁定 | 落后，需升级 |
| 场景一致性 | Blocking 文本俯视图 | 场景锚点图+光照规则 | 落后，可升级 |
| 角色识别 | 无 | 草图颜色映射 | 落后 |
| 成片输出 | ❌（战略暂停AI视频） | ✅ 全链路 | 战略差异 |
| 架构 | Skill版→企业版规划 | CE/EE 六边形双版本 | 可借鉴 |
| 授权 | 开源 | Elastic 2.0 | 我们更开放 |

---

## 五、可吸收的 5 个改进点（按优先级）

1. **🔴 修正风格锚点规范**：Style Anchor 改为 medium/grade-only，禁止时代/内容词（PERIOD/古装/民国/DRAMA/ancient等）。更新知识库示例。这是唯一"我们做错了"的点。
2. **🔴 提示词增加参考图槽位语义**：AI 执行版分镜的提示词规范引入 Image N 槽位（参考图1=角色A），引导用户资产库先行。
3. **🟡 场景布局增加光照状态字段**：每个场景记录 time-of-day 与锚点图，防"跨时段场景崩"。
4. **🟡 角色识别锚点**：画面描述规范增加"色彩/位置锚点"标注（红衣者=女主），为未来线稿管线铺路。
5. **🟢 存档 I2V 规则**：若未来战略放开 AI 视频，首帧契约+单向运动链+禁静态镜头是现成规范。

**不做的**：不部署 DramaClaw、不集成、不抄 Elastic 2.0 授权模式（其禁止 SaaS 转售，我们未来企业版不受此限反而更自由）、不改变"AI视频暂停"战略。

---

## 六、威胁评估

- DramaClaw 免费提供"小说→成片"，挤压"素材层"卖点——但它的剧本/分镜是通用LLM生成，方法论深度不足
- 它已在长"创作伴侣"（Xia Director），叙事方法论可能是下一步；窗口期=我们落地 Story Bible + Character Graph 的 6 个月
- Elastic 2.0 让它无法被任何人 SaaS 化——我们未来企业版空间反而受保护

**一句话**：DramaClaw 验证了我们的赛道判断（资产库锁定+跨集一致性是行业标准答案），其工程实现值得我们抄 5 个作业，但其存在不改变我们的战略——方法论深度才是壁垒，而方法论不会开源。
