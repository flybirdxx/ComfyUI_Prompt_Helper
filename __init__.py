#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入视频提示词生成器节点
from .nodes import NODE_CLASS_MAPPINGS as VIDEO_NODE_CLASS_MAPPINGS
from .nodes import NODE_DISPLAY_NAME_MAPPINGS as VIDEO_NODE_DISPLAY_NAME_MAPPINGS

# 导入图片提示词生成器节点
from .image_nodes import NODE_CLASS_MAPPINGS as IMAGE_NODE_CLASS_MAPPINGS
from .image_nodes import NODE_DISPLAY_NAME_MAPPINGS as IMAGE_NODE_DISPLAY_NAME_MAPPINGS

# 合并所有节点映射
NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(VIDEO_NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(IMAGE_NODE_CLASS_MAPPINGS)

# 合并所有显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(VIDEO_NODE_DISPLAY_NAME_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(IMAGE_NODE_DISPLAY_NAME_MAPPINGS)

# 导出
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

# 导入语言检测和UI标签
try:
    from .nodes import DEFAULT_LANGUAGE, UI_LABELS_DATA
except ImportError:
    # 如果是直接运行测试，使用绝对导入
    try:
        from nodes import DEFAULT_LANGUAGE, UI_LABELS_DATA
    except ImportError:
        DEFAULT_LANGUAGE = "zh"
        UI_LABELS_DATA = {"messages": {"zh": {"load_message": "已加载节点"}}, "display_names": {}}

# 打印加载信息
print(UI_LABELS_DATA.get("messages", {}).get(DEFAULT_LANGUAGE, {}).get("load_message", "Loaded the following nodes:"))
for node_name, display_name in NODE_DISPLAY_NAME_MAPPINGS.items():
    print(f"  - {node_name}: {display_name}")