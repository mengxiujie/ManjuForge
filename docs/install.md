# 快速安装教程

## 1. 仓库克隆

```bash
git clone https://github.com/xxx/ai-drama-storyboard-skill.git
cd ai-drama-storyboard-skill
```

## 2. 平台部署

### Hermes Agent

1. 将项目文件夹复制到 `~/.hermes/skills/creative/` 目录
2. 重启 Hermes Agent
3. 使用触发词：`漫剧剧本`/`分镜脚本`/`竖屏分镜`

### OpenClaw / ClawHub

1. 登录 OpenClaw 平台
2. 上传项目文件夹
3. 填写 `skill.json` 中的配置信息
4. 提交审核上架

### SiliconFlow（硅基流动）

1. 登录 SiliconFlow 平台
2. 创建自定义技能
3. 导入 `skill.json` 和 `prompt.core.txt`
4. 选择兼容模型（如 GLM-4.7-Flash）

### Cursor / 本地部署

1. 安装 Cursor 或其他支持 OpenAI 接口的工具
2. 导入项目文件夹
3. 配置 API 接口指向本地或远程模型
4. 加载 `skill.json` 配置

## 3. 快速使用

### 输入示例

```
请将以下故事改编为竖屏9:16漫剧分镜脚本：

少女女娃站在东海悬崖边，好奇地望着远方。一只赤红色的蝴蝶从身旁飞过，
女娃被吸引，追着蝴蝶跑过礁石。她伸手去够蝴蝶，身体越来越靠近悬崖边缘。
突然，脚下的礁石碎裂——女娃坠落悬崖，坠入深海。
```

### 输出示例

将生成：
1. 完整剧本结构（含人设、场景、台词）
2. 竖屏9:16分镜脚本（38碎片+时间轴）
3. 资产清单（P0/P1/P2优先级）
4. AI绘图提示词（可直接用于出图）

## 4. 依赖说明

- 本项目为纯 Prompt 工具，无额外软件依赖
- 需要 AI Agent 平台支持（Hermes/OpenClaw/Cursor等）
- 建议使用支持长文本生成的模型（如 GPT-4、Claude、GLM-4等）

## 5. 常见问题

**Q: 支持哪些AI模型？**
A: 支持所有兼容 OpenAI 接口的大模型，包括 GPT-4、Claude、GLM-4、通义千问等。

**Q: 可以商用吗？**
A: MIT-0 协议允许商用，但建议联系作者获取商用授权和支持。

**Q: 如何自定义风格模板？**
A: 在 `style-templates/` 目录下创建新的模板文件，参考现有模板格式。
