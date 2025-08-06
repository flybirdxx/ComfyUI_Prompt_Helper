#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图片提示词生成器 ComfyUI 自定义节点 (双语版本)
基于AI图片生成最佳实践创建
支持中文和英文两种语言
"""

import json
import os
import locale
import random
import time

# 获取当前文件所在的目录路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 检测系统语言
def detect_system_language():
    """检测系统语言并返回支持的语言代码"""
    try:
        # 获取系统语言设置
        system_locale = locale.getdefaultlocale()[0]
        if system_locale:
            # 如果是中文相关的locale，返回zh
            if system_locale.startswith('zh'):
                return 'zh'
            # 其他情况返回英文
            else:
                return 'en'
    except Exception as e:
        pass
    
    # 默认返回中文
    return 'zh'

# 获取系统默认语言
DEFAULT_LANGUAGE = detect_system_language()

# 构建 JSON 文件的完整路径
IMAGE_PRESETS_FILE_PATH = os.path.join(CURRENT_DIR, 'Image_Presets.json')
IMAGE_UI_LABELS_FILE_PATH = os.path.join(CURRENT_DIR, 'image_ui_labels.json')

# 从 JSON 文件加载图片预设数据
def load_image_presets():
    try:
        with open(IMAGE_PRESETS_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading Image_Presets.json: {e}")
        return {}

# 从 JSON 文件加载UI标签
def load_image_ui_labels():
    try:
        with open(IMAGE_UI_LABELS_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading image_ui_labels.json: {e}")
        # 返回基本的英文标签作为回退
        return {
            "zh": {"language": "语言", "default_prompt": "一个美丽的场景"},
            "en": {"language": "Language", "default_prompt": "A beautiful scene"},
            "messages": {"zh": {}, "en": {}},
            "display_names": {"zh": "图片提示词生成器", "en": "Image Prompt Generator"}
        }

# 加载预设数据和UI标签
IMAGE_PRESETS = load_image_presets()
IMAGE_UI_LABELS_DATA = load_image_ui_labels()
IMAGE_UI_LABELS = IMAGE_UI_LABELS_DATA  # 保持向后兼容

class WanImagePromptGenerator:
    """
    图片提示词生成器节点（双语版本）
    Image Prompt Generator Node (Bilingual Version)
    
    允许用户从10个不同的艺术分类中选择选项来构建专业的图片生成提示词
    Allows users to build professional image generation prompts by selecting from 10 different artistic categories
    """
    
    @classmethod
    def INPUT_TYPES(s):
        """定义输入类型"""
        
        # 为每个分类创建选项列表，添加 "none" 和 "random" 选项在前面
        def get_options(category, language=DEFAULT_LANGUAGE):
            if language in IMAGE_PRESETS and category in IMAGE_PRESETS[language]:
                # 获取本地化的显示文本，而不是键名
                category_data = IMAGE_PRESETS[language][category]
                options = []
                
                # 先添加 "none" 选项，显示为本地化的文本
                if "none" in category_data:
                    none_text = IMAGE_UI_LABELS_DATA[language].get("none_option", "none")
                    options.append(none_text)
                
                # 添加 "random" 选项，显示为本地化的文本
                if "random" in category_data:
                    random_text = IMAGE_UI_LABELS_DATA[language].get("random_option", "random")
                    options.append(random_text)
                
                # 添加其他选项的本地化文本
                for key, value in category_data.items():
                    if key not in ["none", "random"] and value:  # 跳过none、random和空值
                        options.append(value)
                
                return options
            none_text = IMAGE_UI_LABELS_DATA[language].get("none_option", "none")
            return [none_text]
        
        # 根据默认语言设置默认提示词和属性名称
        default_prompt = IMAGE_UI_LABELS[DEFAULT_LANGUAGE]["default_prompt"]
        labels = IMAGE_UI_LABELS[DEFAULT_LANGUAGE]
        
        # 本地化的属性名称映射
        return {
            "required": {
                labels["language"]: (["zh", "en"], {"default": DEFAULT_LANGUAGE}),
                labels["user_prompt"]: ("STRING", {
                    "multiline": True,
                    "default": default_prompt
                }),
                labels["subject_type"]: (get_options("subject_type"), {"default": IMAGE_UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["art_style"]: (get_options("art_style"), {"default": IMAGE_UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["mood_atmosphere"]: (get_options("mood_atmosphere"), {"default": IMAGE_UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["color_palette"]: (get_options("color_palette"), {"default": IMAGE_UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["lighting"]: (get_options("lighting"), {"default": IMAGE_UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["composition"]: (get_options("composition"), {"default": IMAGE_UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["camera_settings"]: (get_options("camera_settings"), {"default": IMAGE_UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["texture_detail"]: (get_options("texture_detail"), {"default": IMAGE_UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["environment"]: (get_options("environment"), {"default": IMAGE_UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["quality_enhancement"]: (get_options("quality_enhancement"), {"default": IMAGE_UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["artist_style"]: (get_options("artist_style"), {"default": IMAGE_UI_LABELS_DATA[DEFAULT_LANGUAGE].get("none_option", "none")}),
                labels["prompt_format"]: ([
                    labels["format_professional"], 
                    labels["format_simple"], 
                    labels["format_detailed"]
                ], {"default": labels["format_professional"]}),
                labels["seed"]: ("INT", {"default": -1, "min": -1, "max": 2147483647, "step": 1})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("generated_prompt",)
    FUNCTION = "generate_image_prompt"
    CATEGORY = "self_node/Image"
    
    def generate_image_prompt(self, **kwargs):
        # 处理随机种子
        seed = kwargs.get("seed", -1)
        if seed == -1:
            # 使用当前时间+随机数作为种子，确保每次都不同
            import hashlib
            timestamp = str(time.time())
            # 使用时间戳和一个额外的随机因子来生成更好的种子
            seed_str = timestamp + str(random.randint(0, 999999))
            seed = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16) % 2147483647
        random.seed(seed)
        print(f"[图片提示词生成器] 使用随机种子: {seed}")
        """生成图片提示词"""
        
        # 创建参数映射以支持本地化的参数名称
        # 将本地化的参数名映射回英文键名
        param_mapping = {}
        for lang_code in ["zh", "en"]:
            labels = IMAGE_UI_LABELS[lang_code]
            for en_key, localized_name in labels.items():
                if en_key in ["language", "user_prompt", "subject_type", "art_style", "mood_atmosphere", 
                             "color_palette", "lighting", "composition", "camera_settings", 
                             "texture_detail", "environment", "quality_enhancement", "artist_style", "prompt_format", "seed"]:
                    param_mapping[localized_name] = en_key
        
        # 创建选项值的反向映射（本地化文本 -> 键名）
        def create_value_to_key_mapping(language):
            value_to_key = {}
            if language in IMAGE_PRESETS:
                for category, items in IMAGE_PRESETS[language].items():
                    for key, value in items.items():
                        if value:  # 只映射非空值
                            value_to_key[value] = key
                # 处理"无"和"随机"选项
                none_text = IMAGE_UI_LABELS_DATA[language].get("none_option", "none")
                value_to_key[none_text] = "none"
                random_text = IMAGE_UI_LABELS_DATA[language].get("random_option", "random")
                value_to_key[random_text] = "random"
                
                # 处理prompt_format选项的映射
                labels = IMAGE_UI_LABELS[language]
                value_to_key[labels["format_professional"]] = "professional"
                value_to_key[labels["format_simple"]] = "simple"
                value_to_key[labels["format_detailed"]] = "detailed"
            return value_to_key
        
        # 将本地化参数名和值映射为英文参数名和键名
        params = {}
        for key, value in kwargs.items():
            mapped_key = param_mapping.get(key, key)
            params[mapped_key] = value
        
        # 提取参数
        language = params.get("language", DEFAULT_LANGUAGE)
        
        # 验证语言参数并获取预设数据
        if language not in IMAGE_PRESETS:
            messages = IMAGE_UI_LABELS_DATA.get("messages", {}).get(DEFAULT_LANGUAGE, {})
            unsupported_msg = messages.get("unsupported_language", "Unsupported language")
            fallback_msg = messages.get("fallback_to_default", ", fallback to default language")
            print(f"[ImagePromptGenerator] {unsupported_msg}: {language}{fallback_msg}: {DEFAULT_LANGUAGE}")
            language = DEFAULT_LANGUAGE
        
        # 获取当前语言的预设数据
        current_presets = IMAGE_PRESETS[language]
        current_labels = IMAGE_UI_LABELS[language]
        
        # 创建当前语言的值到键的映射
        value_to_key = create_value_to_key_mapping(language)
        
        # 提取并转换参数值
        user_prompt = params.get("user_prompt", IMAGE_UI_LABELS[language]["default_prompt"])
        
        # 对于选项类型的参数，需要将本地化文本转换回键名，并处理随机选择
        def convert_value_to_key(value, category, default="none"):
            if not value:
                return default
            
            # 获取键名
            key = value_to_key.get(value, value)
            
            # 如果选择了随机，从该分类中随机选择一个非none、非random的选项
            if key == "random" and category in current_presets:
                available_options = [k for k in current_presets[category].keys() 
                                   if k not in ["none", "random"] and current_presets[category][k]]
                if available_options:
                    key = random.choice(available_options)
                    print(f"[随机选择] {category}: {current_presets[category][key]}")
                else:
                    key = "none"
            
            return key
        
        subject_type = convert_value_to_key(params.get("subject_type"), "subject_type")
        art_style = convert_value_to_key(params.get("art_style"), "art_style")
        mood_atmosphere = convert_value_to_key(params.get("mood_atmosphere"), "mood_atmosphere")
        color_palette = convert_value_to_key(params.get("color_palette"), "color_palette")
        lighting = convert_value_to_key(params.get("lighting"), "lighting")
        composition = convert_value_to_key(params.get("composition"), "composition")
        camera_settings = convert_value_to_key(params.get("camera_settings"), "camera_settings")
        texture_detail = convert_value_to_key(params.get("texture_detail"), "texture_detail")
        environment = convert_value_to_key(params.get("environment"), "environment")
        quality_enhancement = convert_value_to_key(params.get("quality_enhancement"), "quality_enhancement")
        artist_style = convert_value_to_key(params.get("artist_style"), "artist_style")
        
        # prompt_format不需要随机功能，单独处理
        prompt_format_value = params.get("prompt_format")
        prompt_format = value_to_key.get(prompt_format_value, "professional") if prompt_format_value else "professional"
        
        # 收集所有选择的元素
        selected_elements = []
        
        # 定义参数映射
        category_params = {
            "subject_type": subject_type,
            "art_style": art_style,
            "mood_atmosphere": mood_atmosphere,
            "color_palette": color_palette,
            "lighting": lighting,
            "composition": composition,
            "camera_settings": camera_settings,
            "texture_detail": texture_detail,
            "environment": environment,
            "quality_enhancement": quality_enhancement,
            "artist_style": artist_style
        }
        
        # 提取选中的非空元素
        for category, value in category_params.items():
            if value != "none" and category in current_presets and value in current_presets[category]:
                element_text = current_presets[category][value]
                if element_text:  # 确保元素文本不为空
                    selected_elements.append(element_text)
        
        # 根据格式生成提示词
        if prompt_format == "professional":
            if selected_elements:
                artistic_elements = "，".join(selected_elements) if language == "zh" else ", ".join(selected_elements)
                separator = "，" if language == "zh" else ", "
                generated_prompt = f"{user_prompt}{separator}{artistic_elements}{current_labels['professional_suffix']}"
            else:
                generated_prompt = f"{user_prompt}{current_labels['professional_suffix']}"
                
        elif prompt_format == "detailed":
            if selected_elements:
                # 按类别组织元素
                style_elements = []
                technical_elements = []
                aesthetic_elements = []
                
                # 分类整理元素
                style_categories = ["subject_type", "art_style", "mood_atmosphere", "artist_style"]
                technical_categories = ["composition", "camera_settings", "lighting"]
                aesthetic_categories = ["color_palette", "texture_detail", "environment", "quality_enhancement"]
                
                for category, value in category_params.items():
                    if value != "none" and category in current_presets and value in current_presets[category]:
                        element_text = current_presets[category][value]
                        if element_text:
                            if category in style_categories:
                                style_elements.append(element_text)
                            elif category in technical_categories:
                                technical_elements.append(element_text)
                            elif category in aesthetic_categories:
                                aesthetic_elements.append(element_text)
                
                # 构建详细提示词
                prompt_parts = [user_prompt]
                separator = "，" if language == "zh" else ", "
                
                if language == "zh":
                    if style_elements:
                        prompt_parts.append(f"风格：{separator.join(style_elements)}")
                    if technical_elements:
                        prompt_parts.append(f"技术：{separator.join(technical_elements)}")
                    if aesthetic_elements:
                        prompt_parts.append(f"美学：{separator.join(aesthetic_elements)}")
                else:
                    if style_elements:
                        prompt_parts.append(f"Style: {separator.join(style_elements)}")
                    if technical_elements:
                        prompt_parts.append(f"Technical: {separator.join(technical_elements)}")
                    if aesthetic_elements:
                        prompt_parts.append(f"Aesthetic: {separator.join(aesthetic_elements)}")
                
                prompt_parts.append(current_labels['detailed_suffix'].lstrip(". "))
                connector = "。" if language == "zh" else ". "
                generated_prompt = connector.join(prompt_parts)
            else:
                connector = "。" if language == "zh" else ". "
                generated_prompt = f"{user_prompt}{connector}{current_labels['detailed_suffix'].lstrip('. ')}"
                
        else:  # simple format
            if selected_elements:
                # 选择最重要的几个元素
                key_elements = selected_elements[:4]  # 只取前4个元素
                separator = "，" if language == "zh" else ", "
                generated_prompt = f"{user_prompt}{separator}{separator.join(key_elements)}"
            else:
                generated_prompt = user_prompt
        
        # 本地化的输出信息
        messages = IMAGE_UI_LABELS_DATA.get("messages", {}).get(language, {})
        generated_msg = messages.get("generated_prompt", "Generated prompt with")
        elements_msg = messages.get("artistic_elements", "artistic elements")
        selected_msg = messages.get("selected_elements", "Selected elements")
        
        if language == "zh":
            print(f"图片提示词生成器 ({language}): {generated_msg} {len(selected_elements)} {elements_msg}")
        else:
            print(f"ImagePromptGenerator ({language}): {generated_msg} {len(selected_elements)} {elements_msg}")
        
        if selected_elements:
            print(f"{selected_msg}: {selected_elements}")
        
        return (generated_prompt,)

# ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "Wan_image_prompt_generator": WanImagePromptGenerator
}

# 节点显示名称的本地化映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "Wan_image_prompt_generator": IMAGE_UI_LABELS_DATA.get("display_names", {}).get(DEFAULT_LANGUAGE, "Image Prompt Generator")
}