import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = <influxDB bucket name>
org = <influxDB user name>
token = <influxDB token>
client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

# MQTT settings
MQTT_BROKER = <RaspberryPi ip>
MQTT_PORT = 1883
TOPICS = ["parking", "charging", "sensor/raw_distance", "sensor/temperature_humidity" ]

charging_level = 0

def on_message(client, userdata, msg):
    global charging_level
    try:
        print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
        topic = msg.topic
        payload = json.loads(msg.payload.decode("utf-8"))

        if topic == "sensor/raw_distance":
            point = Point("Ultrasonic").tag("sensor", "raw").field("parking", payload["parking"]).field("charging", payload["charging"])
        elif topic == "parking":
            point = Point("parking").tag("sensor", "status").field("status", payload)
        elif topic == "charging":
            if payload == 0 : 
                charging_level = 0 
            elif payload == 1: 
                charging_level += 1
                if charging_level >= 100:
                    charging_level = 100

            point = Point("charging").tag("sensor", "status").field("status", payload)
            point = Point("charging_level").tag("sensor", "charging_level").field("level", charging_level)
        elif topic == "sensor/temperature_humidity":
                temperature = payload.get("temperature", None)
                humidity = payload.get("humidity", None)
                point = Point("environment").tag("location", "living_room").field("temperature", temperature).field("humidity", humidity)
                write_api.write(bucket, org, point)
            
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")

    write_api.write(bucket, org, point)

# MQTT setup
client = mqtt.Client()
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

for topic in TOPICS:
    client.subscribe(topic)

client.loop_forever()
