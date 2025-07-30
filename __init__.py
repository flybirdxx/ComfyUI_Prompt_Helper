#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入nodes模块
from .nodes import NODE_CLASS_MAPPINGS as VIDEO_PROMPT_MAPPINGS
from .nodes import NODE_DISPLAY_NAME_MAPPINGS as VIDEO_PROMPT_DISPLAY_MAPPINGS

# 合并所有节点映射
NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(VIDEO_PROMPT_MAPPINGS)

# 合并所有显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(VIDEO_PROMPT_DISPLAY_MAPPINGS)

# 导出
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

# 导入语言检测和UI标签
from .nodes import DEFAULT_LANGUAGE, UI_LABELS_DATA

# 打印加载信息
print(UI_LABELS_DATA.get("messages", {}).get(DEFAULT_LANGUAGE, {}).get("load_message", "Loaded the following nodes:"))
for node_name, display_name in NODE_DISPLAY_NAME_MAPPINGS.items():
    print(f"  - {node_name}: {display_name}")