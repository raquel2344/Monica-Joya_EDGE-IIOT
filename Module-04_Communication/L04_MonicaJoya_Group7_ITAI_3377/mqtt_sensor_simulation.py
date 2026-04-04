import paho.mqtt.client as mqtt
import random
import time

broker = "localhost"
port = 1883
topic = "sensor/data"

def simulate_sensor_data():
    while True:
        temperature = random.uniform(20.0, 25.0)
        humidity = random.uniform(30.0, 50.0)
        payload = f'{{"temperature": {temperature}, "humidity": {humidity}}}'
        client.publish(topic, payload)
        print(f"Published - Temperature: {temperature:.2f}, Humidity: {humidity:.2f}")
        time.sleep(1)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(broker, port)
simulate_sensor_data()
