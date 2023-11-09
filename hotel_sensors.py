import time
import paho.mqtt.client as mqtt
import grovepi
import math
import json

# Connect the Grove Ultrasonic Rangers to digital ports D5 and D6
dht         = 4  # The Sensor goes on digital port 4.
parking_D5  = 5  #
charging_D6 = 6

# MQTT settings
broker_address  = "localhost"
port            = 1883
topic_parking   = "parking"
topic_charging  = "charging"
topic_raw       = "sensor/raw_distance"
topic           = "sensor/temperature_humidity"

# Initialize MQTT client
client = mqtt.Client("hotel_msgs")
client.connect(broker_address, port)

while True:
    try:
        # Get sensor values
        parking = grovepi.ultrasonicRead(parking_D5)
        charging = grovepi.ultrasonicRead(charging_D6)
        [temp, humidity] = grovepi.dht(dht, 0) # 0 = blue sensor, 1 = white sensor

        # Publish raw distances
        payload_raw = {"parking": parking, "charging": charging}
        client.publish(topic_raw, json.dumps(payload_raw))

        # Check if distance is below 5 cm and publish to parking and charging topics
        payload_parking = 1 if parking < 5 else 0
        payload_charging = 1 if charging < 5 else 0

        client.publish(topic_parking, payload_parking)
        client.publish(topic_charging, payload_charging)

        print(f"Parking sensor: {parking} cm, charging sensor: {charging} cm")

        if math.isnan(temp) == False and math.isnan(humidity) == False:
            print(f"temp = {temp} C\thumidity = {humidity} %")

            # Publish to MQTT
            payload = {"temperature": temp, "humidity": humidity}
            client.publish(topic, json.dumps(payload))

        # Delay for a bit before reading the sensors again
        time.sleep(1)

    except KeyboardInterrupt:
        break
    except IOError:
        print("Error")
