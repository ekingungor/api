import requests
import json
import random
import threading
import time

methods = [
    "autoregression",
    "moving-average",
    "autoregressive-moving-average",
    "autoregressive-integrated-moving-average",
    "seasonal-autoregressive-integrated-moving-average",
]

f = open("iot_devices/iot_devices.json")
devices = json.load(f)
iot_device_nums = list(range(4))

columns = ["Temperature", "Oxygen", "Humidity"]


def func():
    while True:
        print("requested")
        method = random.choice(methods)
        iot_device_num = random.choice(iot_device_nums)
        column = random.choice(columns)
        steps = random.randint(3, 1000)

        url = f"http://51.142.111.99:8000/{method}/{iot_device_num}/{column}/{steps}"
        try:
            response = requests.get(url)
            print(response.status_code)
        except Exception as e:
            print(e)


threads = []
for i in range(1):
    threads.append(
        threading.Thread(
            target=func,
        )
    )

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
