# ComfyUI Prompt Helper - 视频提示词生成器

## 简介 / Introduction

**ComfyUI Prompt Helper** 是一个专为 ComfyUI 设计的自定义节点插件，提供强大的视频提示词生成功能。该插件支持中英文双语界面，基于 Denge AI 的视频提示词生成工具开发，帮助用户快速构建专业的电影化提示词。

**ComfyUI Prompt Helper** is a custom node plugin designed for ComfyUI that provides powerful video prompt generation capabilities. This plugin supports bilingual Chinese-English interface, developed based on Denge AI's video prompt generation tool, helping users quickly build professional cinematic prompts.

## 功能特点 / Features

- 🎬 **专业电影化提示词生成** - 构建高质量的视频生成提示词
- 🌐 **双语支持** - 自动检测系统语言，支持中文和英文界面
- 📋 **14个专业分类** - 覆盖电影制作的各个方面
- 🎯 **三种格式输出** - 专业、简单、详细三种提示词格式
- 🔧 **高度可定制** - 丰富的配置选项和预设
- 📚 **内置示例** - 包含多个使用示例和最佳实践

## 分类选项 / Categories

插件提供以下14个专业分类：

1. **镜头大小 / Shot Size** - 全景、中景、特写等
2. **灯光类型 / Lighting Type** - 自然光、戏剧化灯光、柔光等
3. **光源 / Light Source** - 阳光、月光、火光等
4. **色调 / Color Tone** - 暖色调、冷色调、高对比度等
5. **摄像机角度 / Camera Angle** - 平视、仰视、俯视等
6. **镜头 / Lens** - 广角、人像、长焦等
7. **基础摄像机运动 / Basic Camera Movement** - 静态、平移、缩放等
8. **高级摄像机运动 / Advanced Camera Movement** - 推轨、斯坦尼康、航拍等
9. **时间 / Time of Day** - 黎明、黄昏、夜晚等
10. **运动 / Motion** - 慢动作、快动作、正常速度等
11. **视觉效果 / Visual Effects** - 镜头光晕、雨滴、雾气等
12. **视觉风格 / Visual Style** - 电影风格、纪录片、动作等
13. **角色情感 / Character Emotion** - 开心、悲伤、紧张等
14. **构图 / Composition** - 三分法、对称、非对称等

## 安装方法 / Installation

### 方法一：Git Clone（推荐）

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YOUR_USERNAME/ComfyUI_Prompt_Helper.git
```

### 方法二：手动下载

1. 下载本仓库的 ZIP 文件
2. 解压到 `ComfyUI/custom_nodes/` 目录
3. 重启 ComfyUI

## 使用方法 / Usage

1. **启动 ComfyUI** - 插件会自动加载并检测系统语言
2. **添加节点** - 在节点菜单中找到 "视频提示词生成器" 或 "Video Prompt Generator"
3. **配置参数** - 从各个分类中选择所需的选项
4. **生成提示词** - 插件会自动组合生成专业的提示词

### 示例工作流 / Example Workflow

```
用户输入: "一个战士在战场上奔跑"
配置选项:
- 镜头大小: 中景
- 灯光类型: 戏剧化灯光
- 色调: 高对比度
- 摄像机角度: 仰视角度
- 提示词格式: 专业

输出结果: "一个战士在战场上奔跑，中景，戏剧化灯光，高对比度，仰视角度，专业电影质量，高细节，4K分辨率"
```

## 文件结构 / File Structure

```
ComfyUI_Prompt_Helper/
├── __init__.py                                  # 插件初始化文件
├── nodes.py                                     # 主要功能代码
├── Prompt_Presets.json                          # 预设配置文件
├── ui_labels.json                              # 界面标签文件
└── README.md                                   # 说明文档
```

## 配置文件 / Configuration Files

- **Prompt_Presets.json** - 包含所有分类的预设选项
- **ui_labels.json** - 定义界面标签的多语言文本

## 自定义配置 / Customization

您可以通过编辑 JSON 配置文件来自定义选项：

1. 编辑 `Prompt_Presets.json` 添加新的预设选项
2. 修改 `ui_labels.json` 更新界面文本

## 兼容性 / Compatibility

- **ComfyUI** - 支持最新版本的 ComfyUI
- **Python** - 需要 Python 3.7+
- **操作系统** - 支持 Windows、macOS、Linux

## 许可证 / License

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

## 更新日志 / Changelog

### v1.0.0
- 初始版本发布
- 支持14个专业分类
- 双语界面支持
- 三种提示词格式

## 致谢 / Acknowledgments

- 感谢 [ComfyUI](https://github.com/comfyanonymous/ComfyUI) 提供的优秀平台

---

