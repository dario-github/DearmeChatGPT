# -*- coding:utf-8 -*-
import os
from pathlib import Path
import gradio as gr
from .webui_locale import I18nAuto

i18n = I18nAuto()  # internationalization

CHATGLM_MODEL = None
CHATGLM_TOKENIZER = None
LLAMA_MODEL = None
LLAMA_INFERENCER = None

# ChatGPT 设置
INITIAL_SYSTEM_PROMPT = "你是一个非常专业的个人助理"
API_URL = "https://api.openai.com/v1/chat/completions"
API_HOST = "api.openai.com"
COMPLETION_URL = "https://api.openai.com/v1/chat/completions"
BALANCE_API_URL="https://api.openai.com/dashboard/billing/credit_grants"
USAGE_API_URL="https://api.openai.com/dashboard/billing/usage"
HISTORY_DIR = Path("history")
HISTORY_DIR = "history"
TEMPLATES_DIR = "templates"

# 错误信息
STANDARD_ERROR_MSG = i18n("☹️发生了错误：")  # 错误信息的标准前缀
GENERAL_ERROR_MSG = i18n("获取对话时发生错误，请查看后台日志")
ERROR_RETRIEVE_MSG = i18n("请检查网络连接，或者API-Key是否有效。")
CONNECTION_TIMEOUT_MSG = i18n("连接超时，无法获取对话。")  # 连接超时
READ_TIMEOUT_MSG = i18n("读取超时，无法获取对话。")  # 读取超时
PROXY_ERROR_MSG = i18n("代理错误，无法获取对话。")  # 代理错误
SSL_ERROR_PROMPT = i18n("SSL错误，无法获取对话。")  # SSL 错误
NO_APIKEY_MSG = i18n("API key为空，请检查是否输入正确。")  # API key 长度不足 51 位
NO_INPUT_MSG = i18n("请输入对话内容。")  # 未输入对话内容
BILLING_NOT_APPLICABLE_MSG = i18n("账单信息不适用") # 本地运行的模型返回的账单信息

TIMEOUT_STREAMING = 60  # 流式对话时的超时时间
TIMEOUT_ALL = 200  # 非流式对话时的超时时间
ENABLE_STREAMING_OPTION = True  # 是否启用选择选择是否实时显示回答的勾选框
HIDE_MY_KEY = False  # 如果你想在UI中隐藏你的 API 密钥，将此值设置为 True
CONCURRENT_COUNT = 100 # 允许同时使用的用户数量

SIM_K = 5
INDEX_QUERY_TEMPRATURE = 1.0

CHUANHU_TITLE = i18n("ChatGPT 增强版")

CHUANHU_DESCRIPTION = i18n("基于openAI API")

FOOTER = """<div class="versions">{versions}</div>"""

APPEARANCE_SWITCHER = """
<div style="display: flex; justify-content: space-between;">
<span style="margin-top: 4px !important;">"""+ i18n("切换亮暗色主题")  + """</span>
<span><label class="apSwitch" for="checkbox">
    <input type="checkbox" id="checkbox">
    <div class="apSlider"></div>
</label></span>
</div>
"""

ONLINE_MODELS = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "川虎助理",
    "川虎助理 Pro",
    "xmchat",
    "yuanai-1.0-base_10B",
    "yuanai-1.0-translate",
    "yuanai-1.0-dialog",
    "yuanai-1.0-rhythm_poems",
    "minimax-abab4-chat",
    "minimax-abab5-chat",
]

LOCAL_MODELS = [
    "chatglm-6b",
    "chatglm-6b-int4",
    "chatglm-6b-int4-qe",
    "StableLM",
    "MOSS",
    "llama-7b-hf",
    "llama-13b-hf",
    "llama-30b-hf",
    "llama-65b-hf",
]

if os.environ.get('HIDE_LOCAL_MODELS', 'false') == 'true':
    MODELS = ONLINE_MODELS
else:
    MODELS = ONLINE_MODELS + LOCAL_MODELS

DEFAULT_MODEL = 0

os.makedirs("models", exist_ok=True)
os.makedirs("lora", exist_ok=True)
os.makedirs("history", exist_ok=True)
for dir_name in os.listdir("models"):
    if os.path.isdir(os.path.join("models", dir_name)):
        if dir_name not in MODELS:
            MODELS.append(dir_name)

MODEL_TOKEN_LIMIT = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-0301": 4096,
    "gpt-4": 8192,
    "gpt-4-0314": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-32k-0314": 32768
}

TOKEN_OFFSET = 1000 # 模型的token上限减去这个值，得到软上限。到达软上限之后，自动尝试减少token占用。
DEFAULT_TOKEN_LIMIT = 3000 # 默认的token上限
REDUCE_TOKEN_FACTOR = 0.5 # 与模型token上限想乘，得到目标token数。减少token占用时，将token占用减少到目标token数以下。

REPLY_LANGUAGES = [
    "简体中文",
    "繁體中文",
    "English",
    "日本語",
    "Español",
    "Français",
    "Deutsch",
    "跟随问题语言（不稳定）"
]


WEBSEARCH_PTOMPT_TEMPLATE = """\
网络搜索结果：
{web_results}
当前日期：{current_date}

说明：利用提供的网络搜索结果，为给定的问题编写全面的回答。确保在引用后使用[[number](URL)]标记引用结果。如果提供的搜索结果涉及多个同名主题，请为每个主题撰写单独的答案。
问题：{query}
用{reply_language}回答
"""

PROMPT_TEMPLATE = """\
以下是背景信息。
---------------------
{context_str}
---------------------
当前日期：{current_date}。
根据提供的背景信息，以朋友聊天的语气来为给定问题撰写一份回复，尽量简短口语化。
如果提供的背景信息涉及多个同名主题，请为每个主题撰写单独的答案。
仅在给定的背景信息不足以提供足够信息时，使用先前的知识。
如果背景信息不足且先前知识也不足，按照你所模仿的人物的特点自行决定回复内容。
问题：{query_str}
用{reply_language}回复
"""
# """
# 根据提供的背景信息，为给定问题撰写一份全面的回答。
# 请确保在引用之后使用 [number] 标记来引用结果。
# 如果提供的背景信息涉及多个同名主题，请为每个主题撰写单独的答案。
# 仅在给定的背景信息不足以提供足够信息时，使用先前的知识。
# 回答问题：{query_str}
# 用{reply_language}回复
# """

REFINE_TEMPLATE = """\
原始问题如下：{query_str}
我们提供了一个现有的答案：{existing_answer}
如果需要，我们有机会在下文中完善现有答案。
这是新的背景信息：{context_msg}
根据新的背景信息，优化原始答案以更好地回答
用{reply_language}回复
如果上下文无用，请返回原始答案。
"""

SUMMARIZE_PROMPT = """Write a concise summary of the following:

{text}

CONCISE SUMMARY IN 中文:"""

ALREADY_CONVERTED_MARK = "<!-- ALREADY CONVERTED BY PARSER. -->"

small_and_beautiful_theme = gr.themes.Soft(
        primary_hue=gr.themes.Color(
            c50="#EBFAF2",
            c100="#CFF3E1",
            c200="#A8EAC8",
            c300="#77DEA9",
            c400="#3FD086",
            c500="#02C160",
            c600="#06AE56",
            c700="#05974E",
            c800="#057F45",
            c900="#04673D",
            c950="#2E5541",
            name="small_and_beautiful",
        ),
        secondary_hue=gr.themes.Color(
            c50="#576b95",
            c100="#576b95",
            c200="#576b95",
            c300="#576b95",
            c400="#576b95",
            c500="#576b95",
            c600="#576b95",
            c700="#576b95",
            c800="#576b95",
            c900="#576b95",
            c950="#576b95",
        ),
        neutral_hue=gr.themes.Color(
            name="gray",
            c50="#f6f7f8",
            # c100="#f3f4f6",
            c100="#F2F2F2",
            c200="#e5e7eb",
            c300="#d1d5db",
            c400="#B2B2B2",
            c500="#808080",
            c600="#636363",
            c700="#515151",
            c800="#393939",
            # c900="#272727",
            c900="#2B2B2B",
            c950="#171717",
        ),
        radius_size=gr.themes.sizes.radius_sm,
    ).set(
        # button_primary_background_fill="*primary_500",
        button_primary_background_fill_dark="*primary_600",
        # button_primary_background_fill_hover="*primary_400",
        # button_primary_border_color="*primary_500",
        button_primary_border_color_dark="*primary_600",
        button_primary_text_color="wihte",
        button_primary_text_color_dark="white",
        button_secondary_background_fill="*neutral_100",
        button_secondary_background_fill_hover="*neutral_50",
        button_secondary_background_fill_dark="*neutral_900",
        button_secondary_text_color="*neutral_800",
        button_secondary_text_color_dark="white",
        # background_fill_primary="#F7F7F7",
        # background_fill_primary_dark="#1F1F1F",
        # block_title_text_color="*primary_500",
        block_title_background_fill_dark="*primary_900",
        block_label_background_fill_dark="*primary_900",
        input_background_fill="#F6F6F6",
    )
