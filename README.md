# ManjuForge｜漫剧铸造

**AI漫剧连载创作引擎（Hermes Skill）**

> 别人做好看的单集，我们做活得久的IP。

<p align="center">
  <a href="https://github.com/mengxiujie/ManjuForge">GitHub</a> |
  <a href="https://gitcode.com/gcw_LRlig9U4/manjuforge">GitCode</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-v1.6.0-brightgreen" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT--0-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Hermes%20Agent-blue" alt="Platform">
  <img src="https://img.shields.io/badge/Episodes--Tested-6-red" alt="Episodes">
  <img src="https://img.shields.io/badge/Foreshadow--Rate-100%25-orange" alt="Foreshadow">
</p>

---

## 📖 这是什么

ManjuForge 是一个 AI 漫剧**连载**创作工具，以 Hermes Skill 形态运行。

输入题材和人设，输出：**完整剧本 + 竖屏分镜 + 配音文案 + AI绘图提示词**。

核心解决一个问题：**连载30集以上，人设不崩、剧情不断、伏笔不丢。**

---

## ✨ 实测验证（6集Demo）

用《代码赘婿》（古风穿越爽剧）完成6集完整创作测试：

| 集数 | 标题 | 综合评分 | 第三方评分 |
|------|------|:--------:|:----------:|
| 1 | 赘婿被当众扇耳光，他忍了，但账本上的数字让他笑了 | 7.8 | 88 |
| 2 | 赘婿拿着八千两证据去告发，被拦在门外——没人听他说话 | 7.8 | 92 |
| 3 | 赘婿当众掀了桌子，八千两贪墨一笔笔念出来，全场鸦雀无声 | 8.3 | 95 |
| 4 | 林家铺子被封、漕运断裂，赘婿在街口摆了个摊，第一天来了七个人 | 8.2 | — |
| 5 | 赘婿带绸缎样品上门推销，对方一摸料子说了句——"这比赵家的好" | 8.1 | 97 |
| 6 | 绸缎行会上赵家发难要封杀林家，赘婿站起来说了一个词——"联营" | 8.3 | 96.5 |

### 验证结果

| 验证项 | 结果 | 说明 |
|--------|:----:|------|
| 记忆跨集连贯性 | ✅ | 6集零崩坏，七文件持久化机制有效（角色/世界观/场景/剧情/伏笔/圣经/关系图） |
| 人设一致性 | ✅ | 沈舟始终用数字+逻辑，无能力跳变 |
| 伏笔回收率 | ✅ | 100%（11个伏笔全部回收或推进） |
| 关系自然演进 | ✅ | Show Not Tell：空间距离/道具/行为转变 |
| 多主线并行 | ✅ | 第4集起成功引入第二条主线 |
| 势力对抗升级 | ✅ | 第6集从个人对抗→阵营对抗 |

### 第三方评估评级（6集综合）

```
Character Memory:    A+
Relationship Graph:  A+
State Engine:        A+
Faction Engine:      A
Economic Logic:      A+
World Consistency:   A+
Narrative Engine:    A+
综合等级：A+
```

---

## 🔗 核心能力

### 连载记忆机制
三个文件实现跨集记忆：
- **角色档案** — 锁定人设、关系、台词风格
- **世界观** — 锁定时代、规则、势力
- **剧情摘要** — 记录关键剧情、伏笔、时间线，每集自动更新

### 竖屏分镜（9:16）
- 碎片化时间轴（3-7秒/碎片）
- 声音四层标注（🎵音乐+🔊环境+💓生理+🫧细节）
- 统一风格锚点 + Character ID 跨集锁定

### 专业知识库
内置 16 个专业参考文件 + 13 个拉片案例 + 6 大风格模板：
- 盗梦空间/黑客帝国/千与千寻/你的名字/鬼灭之刃/进击的巨人
- 万神殿/中国奇谭/哪吒2/镖人/雾山五行
- 竖屏运镜字典、声音设计分层规范、AI执行字段规范

### 自动质量自检 ★v1.5.0 升级
一行命令跑完 **18 项**质量检查（开篇画面/标题欺诈/风格锚点/Character ID/碎片时长/声音匹配/视觉锤/反派台词/引导/字幕卡/负向提示词/标题格式/场景标记/跨时段过渡/参考图绑定/伏笔表健康/故事圣经健康/角色关系图健康）：
```bash
python scripts/quality_check.py demo/第1集_完整版.md --villain 赵天赐 --foreshadow demo/伏笔表.md --bible demo/故事圣经.md --graph demo/角色关系图.md
```
输出 🔴🟡🟢 分级判定，存在🔴自动拦截进入下一集。已在全部 6 集 Demo + 《渊烬》实战第一单元（E1-5）验证。**v1.5.0：声音匹配改为场景段级检测（按 `**场景：` 边界，跨场景晨/夜共存不再误报）；** v1.4.0 新增故事圣经健康 + 角色关系图健康。

### 实战验证 ★v1.5.0 新增（《渊烬》第一单元 E1-5）
用完整 7 文件流程**从零跑通一部新剧**（改编自同名小说第一卷），非 demo 回顾性迁移：
- 质量曲线：E1 4处修复 → E2 1处 → E3-5 零修复（流程内化为创作习惯）
- 单集六维均值 **91.1/100**；单元七项评级 **6×A+ / 1×A**
- 三引擎实战数据：伏笔表 10 条规划/5 条激活、关系图 8 事件落地、信任曲线 0→15→20
- 实战新认知：**介质锚点**（跨集情绪差异大的剧，锚点只锁介质+完成度，光照为场景变量——见 ai_execution_fields.md 4.4.1）
- 18 项检查实战抓出 4 类真实缺陷（碎片时长/标题覆盖/视觉锤/互动引导）并反哺流程

### Story Bible 故事圣经 ★v1.4.0 新增
**解决30集+"记不住设定"**：全剧设定的唯一事实源总纲——一页纸锚定世界观+角色+符号+禁令。
- 四段式：世界规则摘要/角色弧光表/视觉母题表/禁止变化汇总 + 主线脉络
- 视觉母题 = 全剧符号系统全景（令牌/敲桌子/bug口头禅跨集进化）
- 每5集刷新，创作前30秒锚定全貌

### Character Graph 角色关系图 ★v1.4.0 新增
**解决30集+"记不住关系"**：关系结构化数据——矩阵（当前状态）+ 事件时间线（变化轨迹）。
- 矩阵对称性自动检查（🔴）；单集信任突变>20自动检测（🔴）
- 信任曲线对照（E1-6每集+10~15，E7起平台期）；关系阶段不跳级
- demo 实证：沈舟-林霜 无视→好奇→认可→维护→托付（0→15→30→45→60→65）

### Foreshadow Engine 伏笔引擎 ★v1.3.0 新增
**解决30集+"记不住伏笔"**：伏笔表作为第4个记忆文件，追踪每根伏笔的生命周期（埋设→发酵→推进→回收/废弃）。
- 伏笔七型：道具/台词/人物/事件/设定/关系/**符号**（跨集进化的标志性动作与口头禅）
- 健康规则：每集新埋1-2个+推进1个；回收最早埋后2集；🔴回收内容必须与埋设一致（允许升级禁止降级）
- S级并发活跃≤3，A级≤5；每3集至少回收1个——读者持续获得"闭环爽感"
- demo 实证：12根伏笔全生命周期追踪，F001账本三集闭环、F011联营承接F007遗训（新旧伏笔交汇成网）

### Direct it 提示词范式 ★v1.6.0 新增
吸收 Seedance 2.0 Skill OS（MIT，6244★）"Direct the scene, don't decorate it"原则（调研见 `references/competitive_seedance_survey.md`）：
- **语序**：主体+一个可见动作开篇（模型先锁定"谁在干什么"）→ camera/light/sound 跟随 → 技术规格
- **情绪承载**：情绪用可见动作承载（"the realization lands in the stilled hands, not a word"），形容词降级为辅助
- 影响面：`ai_execution_fields.md` 4.3 提示词模板（全部分镜提示词的生成范式）

### 风格锚点防污染 ★v1.2.1 新增
吸收自 58 集生产管线 DramaClaw：风格锚点只描述渲染介质+完成度，严禁题材/时代/地点/服装内容词——锚点注入每个碎片，带内容词=每帧悄悄覆盖合法内容（闪回现代被压制）。参考图槽位绑定（Image N）提供工业级角色一致性。

### Hook 公式库 ★新增
6种开篇Hook类型 + 4种结尾截断 + 平台差异适配 + 实战检查清单：
- 冲突型/悬念型/情绪型/视觉锤型/提问型/世界建立型
- 每种Hook附模板、公式、示例、高频踩坑点
- 每集自动匹配最合适的Hook类型

### 心理触发点体系 ★新增
基于信息缺口、情感共鸣、认知负荷管理的留人机制：
- 上瘾循环设计（触发→行动→奖励→投入）
- 分集心理节奏模板（第1-3集/4-6集/7-10集/11-15集各有侧重）
- 常见心理触发失效诊断与修复指南

### 自动自检体系 🔄 **v1.1.0新增**

创作完成后立即自动执行18项质量检查（含通过/不通过判定标准）：
- 🔴 项自动标记"未通过"，修复后才能进入下一集
- 修复后自动重检确认闭环
- 覆盖：开篇画面/标题兑现/风格锚点/Character ID/碎片时长/声音设计/空间布局等

### Blocking空间布局 🎬 **v1.1.0新增**

每个关键场景生成文本俯视图（类似电影走位图）：
- 初始化时创建 `场景布局.md`，跨集持久化
- 标注角色位置、核心道具锚点、出入口
- 分镜时空间关系有据可查，杜绝跳位

### 六维度评估体系
六维度评估（剧本/分镜/配音/AI提示词/记忆机制/抖音适配），每集自检 + 每3集跨集评估。

---

## 🚀 快速开始

### 环境要求
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) 已安装
- 任意大模型 API 已配置

### 安装
```bash
git clone https://github.com/mengxiujie/ManjuForge.git ~/.hermes/skills/creative/manjuforge
```

### 使用
在 Hermes 对话中说：

```
我想用 ManjuForge 创作一部漫剧
```

然后告诉它：题材、平台、画幅、集数、核心卖点。

---

## 📁 项目结构

```
ManjuForge/
├── SKILL.md                          # 核心 Skill 定义
├── skill.json                        # 配置文件
├── prompt.core.txt                   # 核心引擎规则（开源稳定版）
├── LICENSE                           # MIT-0
├── scripts/                          # ★v1.2 工具
│   └── quality_check.py              # 18项自动质量自检（一行命令）
├── templates/                        # 记忆模板
│   ├── character_template.md         # 角色档案模板
│   ├── worldbuilding_template.md     # 世界观模板
│   └── plot_summary.md               # 剧情摘要模板
├── references/                       # 专业参考资料（28个专题文件，以目录实际为准 + knowledge_base 拉片库13个案例文件）
│   ├── evaluation_framework.md       # 六维度评估体系
│   ├── style_guide.md                # 六大风格详细指南
│   ├── hook_formula_library.md       # ★六型Hook公式库
│   ├── psychological_triggers.md     # ★心理触发点手册
│   ├── state_snapshot_guide.md       # State Snapshot 状态追踪方法
│   ├── strategy_and_positioning.md   # 定位与推广策略
│   ├── third_party_evaluation.md     # 第三方评估总结
│   └── knowledge_base/               # 13个拉片案例+专业规范
├── demo/                             # 6集完整Demo
│   ├── README.md                     # Demo说明
│   ├── 角色档案.md                   # 4个核心角色
│   ├── 世界观.md                     # 清河郡世界观
│   ├── 剧情摘要.md                   # 10集大纲+伏笔追踪
│   └── 第1-6集_完整版.md             # 每集完整产出
└── docs/                             # 文档
```

---

## 📜 开源协议

MIT-0 License — 免费商用、无需署名、可闭源改造。

---

## 🤝 参与贡献

欢迎 Star、Fork、提 Issue。

有问题或建议 → [GitHub Issues](https://github.com/mengxiujie/ManjuForge/issues)
