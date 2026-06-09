# ManjuForge｜漫剧铸造

**AI漫剧连载创作引擎（Hermes Skill）**

> 别人做好看的单集，我们做活得久的IP。

<p align="center">
  <a href="https://github.com/mengxiujie/ManjuForge">GitHub</a> |
  <a href="https://gitcode.com/gcw_LRlig9U4/manjuforge">GitCode</a>
</p>

<p align="center">
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
| 记忆跨集连贯性 | ✅ | 6集零崩坏，三文件持久化机制有效 |
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
内置 13 个拉片案例 + 6 大风格模板：
- 盗梦空间/黑客帝国/千与千寻/你的名字/鬼灭之刃/进击的巨人
- 万神殿/中国奇谭/哪吒2/镖人/雾山五行
- 竖屏运镜字典、声音设计分层规范、AI执行字段规范

### 质量自检体系
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
├── LICENSE                           # MIT-0
├── templates/                        # 记忆模板
│   ├── character_template.md         # 角色档案模板
│   ├── worldbuilding_template.md     # 世界观模板
│   └── plot_summary.md               # 剧情摘要模板
├── references/                       # 专业参考资料
│   ├── evaluation_framework.md       # 六维度评估体系
│   ├── style_guide.md                # 六大风格详细指南
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
