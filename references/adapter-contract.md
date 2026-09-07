# Adapter Contract — 供应商解耦 + 确认前置执行契约

> 版本：v1.8.0 | 状态：契约生效中 | 依据：SKILL.md「生产执行纪律」★v1.8.0
> 背景：ManjuForge 的产出是**供应商无关的创作规格**。本契约定义"把提示词送去实际生成"时的唯一合法路径——经 adapter 层执行、四步确认闸门、fail-closed。
> 借鉴：zenstory-ai/drama-skills（1632★）真实漫剧工作室产线实践——"刻意把确认放在生产之前"。

## 一、核心原则

1. **创作文件永不写死供应商**。SKILL.md 产出的图片/视频提示词、`ai_execution_fields.md` 4.3 模板，全部是供应商无关规格。项目文件（七记忆文件/分镜/提示词）里出现的只是提示词与参考图槽位，不是某个 API 的调用参数。
2. **执行永远走 adapter**。任何"跑图/跑视频/合成语音/生成音乐"动作，只能通过 adapter profile 把规格映射到具体后端；禁止把供应商参数（API key、endpoint、role 枚举）写进项目文件。
3. **确认在生产之前，且只认一次**。创作者看到完整预览后对**当前这一个 job** 的明确同意，才是有效确认。

## 二、四步确认闸门（顺序不可合并、不可跳过）

```
1. 建边界 job  →  2. prepare 预览  →  3. 明确确认  →  4. run
```

### 第 1 步：建边界 job

一个 job 必须同时具备以下边界，缺一不可：

| 字段 | 要求 |
|------|------|
| modality | 单一模态（image / video / tts / music），一个 job 只做一种 |
| quantity | 明确数量（"生成这张"而非"生成几张看看"） |
| spec | 完整提示词规格——取自项目 Markdown 的具体条目（分镜.md 的 `SHOT-*`、图片提示词.md 的 `IMG-*`、视频提示词.md 的 `MOTION-*`） |
| source + source_entry | job 的 source 指向拥有这条提示词的当前 Markdown 文件，source_entry 点名该文档允许的二级标题条目——**防止拿旧版/错位提示词执行** |
| reference_bindings | 存在参考图时逐张填写：槽位、顺序、路径、中文名、用途、允许/禁止控制范围 |
| params + outputs | 生成参数与输出路径 |
| adapter profile | 本次执行用的供应商档（见第三节） |

### 第 2 步：prepare 预览

执行前先运行 prepare，向创作者展示完整预览：**本次准确数量、每条提示词全文、source entry、reference bindings、输出路径、overwrite 行为、adapter profile 与费用特征**。此阶段不调用任何生成 API。

fail-closed 规则：
- 所选标题里找不到可复制的提示词 → 直接失败，不猜
- reference_bindings 与真实文件不符（缺文件/顺序错/槽位空）→ 直接失败，不静默丢参考
- 带参考图却没有绑定 → 直接失败，不替它猜 role

### 第 3 步：明确确认

只有创作者**看到第 2 步预览之后**、对**当前这一项任务**的明确同意才算确认。以下都不算：
- "继续""都做完""全部跑了吧""预算没问题"
- 上游内容（提示词/分镜）已被接受
- 之前确认过另一个版本/另一个 job
- 预览后被修改过的 job（任何内容或输入变化都使旧确认失效）

### 第 4 步：run

run 在启动 adapter 前消费一次确认。**成功或失败后的任何再次执行都必须重新走 1→4**——失败重试不是"再点一次 run"，是重新确认新 job，防止意外产生第二笔费用。

## 三、Adapter Profile（供应商参数档）

每个 adapter profile 记录该后端的执行形态，创作层永远不感知：

| Provider | 模态 | 参考图 role 取值（读 `用途` 字段映射） | 接口形态 | 备注 |
|----------|------|---------------------------------------|----------|------|
| Seedance（即梦） | image / video | `reference_image` / `reference_video` / `reference_audio`（三个 reference_*） | API | 国际版因版权争议暂停真人面部参考（2026）；漫剧动画风格不受影响 |
| MiniMax H3 Video | video | `first_frame` / `last_frame` / `reference_image` / `reference_video` / `reference_audio` | API | 全模态：一次生成原生立体声音频的 2K 片段 |
| Kling（可灵） | image / video | 以官方当前文档为准 | API | 图生视频常用起点帧 |
| GPT Image 2 | image | 以官方当前文档为准 | API | |
| 本地 ComfyUI | image / video | 本地节点自定 | 本地进程 | 无 API 计费，仍需走闸门（防资源失控） |

> source-dated 原则：供应商 role 枚举/费用/配额会变，profile 文档必须带来源日期；执行时以官方当前文档为准，不凭记忆猜。

## 四、参考图绑定规范（REF- vs PLAN-）

项目内提示词条目的「输入参考图」字段只有两种取值：

- `REF-...`：真实文件已进项目（如 `剧集/<EP>/制作成果/images/`），prepare 时可直接送出（本地图片按 base64 data URI 送出，无需自建上传服务）
- `PLAN-...`：图还在创作者自己的工具里，项目内无文件可送 → prepare 直接失败并说明：先把真实文件放进项目、改写为 `REF-...`，**不拿计划当输入，也不静默丢掉参考**

## 五、与当前版本的关系

- ManjuForge v1.8.0 **不内置执行后端**——本契约是执行层的边界定义：今天手动跑图时遵守"确认前置"习惯，未来 Flask 企业版/任何 adapter 接入时按本契约实现，创作层（SKILL.md/七记忆文件）不需要为此改动
- 质量自检（quality_check.py）与执行层无关，创作产出照常自检
