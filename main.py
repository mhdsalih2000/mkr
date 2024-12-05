import paho.mqtt.client as mqtt
import ssl
import time
from const import imei_pass
from logger import SimpleLogger
import json
from ProcessData import get_vd1_vd0
from const import data
from db import establish_db_connection



class MqttClient:
    logger = SimpleLogger()
    def __init__(self, data,imei_pass ,url="pmkrms.mahadiscom.in", port=8883, keepalive=120):
        self.url = url
        self.port = port
        self.keepalive = keepalive
        self.client = None
        self.data = data
        self.imei_pass =imei_pass

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            decoded_imei = client._client_id.decode('utf-8')
            imei = decoded_imei.split(':')[1].split('$')[0]
            self.logger.log("SUCCESS",f"{imei}")
        else:
            self.logger.log("ERROR", f"Connection failed with return code {rc}")

    def on_message(self, client, userdata, message):
        self.logger.log("INFO", f"Received message: {message.payload.decode()} on topic {message.topic}")

    def establish_connection(self, clientId, userName, password):
        self.client = mqtt.Client(client_id=clientId)
        if userName and password:
            self.client.username_pw_set(userName, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.tls_set(cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLS)
        try:
            self.client.connect(self.url, self.port, self.keepalive)
            self.client.loop_start()
        except Exception as e:
            self.logger.log("ERROR", f"Error establishing connection: {e}")
            return None
        return self.client

    def publish_data(self, client, topic0, topic1, vd0, vd1):
        try:
            if not client.is_connected():
                self.logger.log("WARNING", "Client disconnected, reconnecting...")
                for retry in range(3):
                    client.reconnect()
                    print(f"Client disconnected, reconnecting.{retry+1}/3")
                    time.sleep(7) 
                    if client.is_connected():
                        break
            self.logger.log("INPROGRESS", f"{topic0}")
            result0 = client.publish(topic0, vd0)
            if result0.rc == mqtt.MQTT_ERR_SUCCESS:
                self.logger.log("VD0", f"{vd0}")
            else:
                self.logger.log("ERROR", f"Failed to publish message '{vd0}' to topic '{topic0}'. Error code: {result0.rc}")

            self.logger.log("INPROGRESS", f"{topic1}")
            result1 = client.publish(topic1, vd1)
            if result1.rc == mqtt.MQTT_ERR_SUCCESS:
                self.logger.log("VD1", f"{vd1}")
                self.client.disconnect()
                print("conection disconnected")
                
            else:
                self.logger.log("ERROR", f"Failed to publish message '{vd1}' to topic '{topic1}'. Error code: {result1.rc}")
        except Exception as e:
            self.logger.log("ERROR", f"Error occurred while publishing data: {e}")

    def bulk_publish(self):
        engine, session = establish_db_connection()
        for imei, password in self.imei_pass.items():
            clientId = f"d:{imei}$standalonesolarpump$187"
            userName = f"{imei}$standalonesolarpump$187"
            vd1 ,vd0 = get_vd1_vd0(self.data , imei ,session)
            mqttcliet = self.establish_connection(clientId, userName, password)
            time.sleep(0.3)  
            if mqttcliet and vd0 and vd1:
                vd0_json  =json.dumps(vd0)
                vd1_json  =json.dumps(vd1)
                topic0 = f"iiot-1/standalonesolarpump/{imei}/data/pub"
                topic1 = f"iiot-1/standalonesolarpump/{imei}/heartbeat/pub"
                self.publish_data(mqttcliet, topic0, topic1, vd0_json, vd1_json)



