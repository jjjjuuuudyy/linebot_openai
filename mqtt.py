import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

MQTT_BROKER = "192.168.117.16"
MQTT_PORT = 1883
# MQTT_TOPIC_LED = "judy0528/class304/led"

def send_mqtt(topic, payload):
    try:
        publish.single(topic, payload=payload, hostname=MQTT_BROKER, port=MQTT_PORT)
        print(f"✅ MQTT 發送成功: topic={topic}, payload={payload}")
    except Exception as e:
        print(f"❌ MQTT 發送失敗: {e}")

def send_mqtt_message(broker_ip, topic, message):
    try:
        client = mqtt.Client()
        client.connect(broker_ip, 1883, 60)
        client.publish(topic, message)
        client.disconnect()
        print(f"✅ 發送成功：{topic} -> {message}")
    except Exception as e:
        print(f"❌ MQTT 發送失敗: {e}")