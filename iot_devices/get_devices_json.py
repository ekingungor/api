import json

from azure.iot.hub import IoTHubRegistryManager

IOT_HUB_NAME = "myhub-1"
IOT_HUB_KEY = "LNmnGL0vP7zOKK4tsvHast9qvJ5DnRlH0CAvCik7WtI="

IOT_HUB_CONNECTION_STRING = f"HostName={IOT_HUB_NAME}.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey={IOT_HUB_KEY}"

# Replace <IOTHUB_CONNECTION_STRING> with the connection string for your IoT hub
registry_manager = IoTHubRegistryManager(IOT_HUB_CONNECTION_STRING)

# Get the list of devices
devices = registry_manager.get_devices()

# Initialize an empty list
device_list = []

# Iterate over the devices list
for device in devices:
    # Create a dictionary with the device ID and primary key as the keys and the corresponding values
    device_dict = {
        "device_id": device.device_id,
        "key": device.authentication.symmetric_key.primary_key,
    }
    # Append the dictionary to the device_list
    device_list.append(device_dict)

# Write the device_list to a file called iot_devices.json
with open("iot_devices/iot_devices.json", "w") as f:
    json.dump(device_list, f, indent=5)
