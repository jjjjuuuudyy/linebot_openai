import paho.mqtt.publish as publish

MQTT_BROKER = "192.168.117.16"
MQTT_PORT = 1883
# MQTT_TOPIC_LED = "judy0528/class304/led"

def send_mqtt(topic, payload):
    try:
        publish.single(topic, payload=payload, hostname=MQTT_BROKER, port=MQTT_PORT)
        print(f"✅ MQTT 發送成功: topic={topic}, payload={payload}")
    except Exception as e:
        print(f"❌ MQTT 發送失敗: {e}")

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     msg = event.message.text

#     try:
#         if msg == "開啟LED":
#             publish.single(MQTT_TOPIC_LED, payload="ON", hostname=MQTT_BROKER, port=MQTT_PORT)
#             line_bot_api.reply_message(event.reply_token, TextSendMessage("🟢 已開啟 LED"))
#             return
#         elif msg == "關閉LED":
#             publish.single(MQTT_TOPIC_LED, payload="OFF", hostname=MQTT_BROKER, port=MQTT_PORT)
#             line_bot_api.reply_message(event.reply_token, TextSendMessage("⚪ 已關閉 LED"))
#             return

#         # 否則用 GPT 回覆
#         GPT_answer = GPT_response(msg)
#         print(GPT_answer)
#         line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))

#     except:
#         print(traceback.format_exc())
#         line_bot_api.reply_message(event.reply_token, TextSendMessage('你所使用的OPENAI API key額度可能已經超過，請於後台Log內確認錯誤訊息'))