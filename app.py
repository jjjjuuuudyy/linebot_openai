from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import openai
import time
import traceback
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key初始化設定
openai.api_key = os.getenv("GITHUB_TOKEN")
openai.api_base = "https://models.github.ai/inference"


def GPT_response(text):
    prompt = f""" 
        你是一個友善且精簡的助理，請用繁體中文回覆，語氣自然溫暖。
        適度加入 Emoji 增添親切感。回答應簡短、有重點，避免冗長。
        不要出現 Markdown 或換行符號。
    """
    # 接收回應
    # response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=text, temperature=0.5, max_tokens=500)
    response = openai.ChatCompletion.create(
        model="openai/gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ]
    )
    print(response)
    # 重組回應
    # answer = response['choices'][0]['text'].replace('。','')
    answer = response["choices"][0]["message"]["content"]
    return answer


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     msg = event.message.text
#     try:
#         GPT_answer = GPT_response(msg)
#         print(GPT_answer)
#         line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
#     except:
#         print(traceback.format_exc())
#         line_bot_api.reply_message(event.reply_token, TextSendMessage('你所使用的OPENAI API key額度可能已經超過，請於後台Log內確認錯誤訊息'))
        

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


#========MQTT相關==========
from mqtt import send_mqtt

MQTT_TOPIC_LED = "judy0528/class304/led"
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    try:
        if msg == "開啟LED":
            send_mqtt(MQTT_TOPIC_LED, "ON")
            line_bot_api.reply_message(event.reply_token, TextSendMessage("🟢 已開啟 LED"))
            return
        elif msg == "關閉LED":
            send_mqtt(MQTT_TOPIC_LED, "OFF")
            line_bot_api.reply_message(event.reply_token, TextSendMessage("⚪ 已關閉 LED"))
            return

        # 其他訊息
        line_bot_api.reply_message(event.reply_token, TextSendMessage("未授權的指令"))

    except Exception as e:
        print(traceback.format_exc())
        line_bot_api.reply_message(event.reply_token, TextSendMessage("發生錯誤，請稍後再試。"))
#========MQTT相關==========