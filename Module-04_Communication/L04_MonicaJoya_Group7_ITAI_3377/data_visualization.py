import paho.mqtt.client as mqtt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
from datetime import datetime
from collections import deque

# Thread-safe data storage
data = deque(maxlen=100)

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    parsed = json.loads(payload)
    data.append({
        "timestamp": datetime.now(),
        "temperature": parsed["temperature"],
        "humidity": parsed["humidity"]
    })

def update_plot(frame):
    if len(data) < 2:
        return
    df = pd.DataFrame(list(data))
    ax.clear()
    ax.plot(df["timestamp"], df["temperature"], label="Temperature", color="tab:blue")
    ax.plot(df["timestamp"], df["humidity"], label="Humidity", color="tab:orange")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    ax.set_title("MQTT Sensor Data - Real Time")
    ax.legend()
    fig.autofmt_xdate()

# MQTT setup
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe("sensor/data")
client.loop_start()

# Matplotlib setup — animation runs on main thread
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update_plot, interval=1000)
plt.show()
