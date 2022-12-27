# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.
import json
import os
import asyncio
import random
import sys
import threading

sys.path.append(os.getcwd())


from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

# The device connection authenticates your device to your IoT hub. The connection string for
# a device should never be stored in code. For the sake of simplicity we're using an environment
# variable here. If you created the environment variable with the IDE running, stop and restart
# the IDE to pick up the environment variable.
#
# You can use the Azure CLI to find the connection string:
#     az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table


IOT_HUB_NAME = "myhub-1"
IOT_HUB_KEY = "LNmnGL0vP7zOKK4tsvHast9qvJ5DnRlH0CAvCik7WtI="
IOT_HUB_CONNECTION_STRING = f"HostName={IOT_HUB_NAME}.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey={IOT_HUB_KEY}"

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
OXYGEN = 90
CARBON_DIOXIDE = 500
MSG_TXT = '{{"Temperature": {temperature},"Humidity": {humidity}, "Oxygen": {oxygen}, "CarbonDioxide":{carbon_dioxide},"Location":{location}}}'


async def run_telemetry_sample(client, location):
    # This sample will send temperature telemetry every second

    await client.connect()
    print(f"IoT Hub device sending periodic messages")

    while True:
        # Build the message with simulated telemetry values.
        temperature = TEMPERATURE + (random.random() * 15)
        humidity = HUMIDITY + (random.random() * 20)
        oxygen = OXYGEN + (random.random() * 10)
        carbon_dioxide = CARBON_DIOXIDE + (random.random() * 600)
        location = location
        msg_txt_formatted = MSG_TXT.format(
            temperature=temperature,
            humidity=humidity,
            oxygen=oxygen,
            carbon_dioxide=carbon_dioxide,
            location=location,
        )
        message = Message(msg_txt_formatted)

        # Add a custom application property to the message.
        # An IoT hub can filter on these properties without access to the message body.
        if carbon_dioxide > 1000:
            message.custom_properties["carbonDioxideAlert"] = "true"
        else:
            message.custom_properties["carbonDioxideAlert"] = "false"

        await client.send_message(message)
        print("Message successfully sent")
        await asyncio.sleep(1)


def func(device_connection_string, location):
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Run the sample in the event loop
        loop.run_until_complete(run_telemetry_sample(client, location))
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped by user")
    finally:
        # Upon application exit, shut down the client
        print("Shutting down IoTHubClient")
        loop.run_until_complete(client.shutdown())
        loop.close()


def main():
    print("IoT Hub Quickstart #1 - Simulated device")
    print("Press Ctrl-C to exit")

    # Instantiate the client. Use the same instance of the client for the duration of
    # your application

    # Opening JSON file
    f = open("iot_devices/iot_devices.json")
    devices = json.load(f)
    threads = []
    for device in devices[:5]:
        device_id = device["device_id"]
        device_key = device["key"]
        device_location = device["location"]
        device_connection_string = f"HostName={IOT_HUB_NAME}.azure-devices.net;DeviceId={device_id};SharedAccessKey={device_key}"
        threads.append(
            threading.Thread(
                target=func,
                args=(
                    device_connection_string,
                    device_location,
                ),
            )
        )
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
