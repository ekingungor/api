import uuid
import json
import random
import string

from azure.iot.hub import IoTHubRegistryManager

IOT_HUB_NAME = "myhub-1"
IOT_HUB_KEY = "LNmnGL0vP7zOKK4tsvHast9qvJ5DnRlH0CAvCik7WtI="


def key_generator(length=43):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return "".join(random.choice(letters) for i in range(length)) + "="


IOT_HUB_CONNECTION_STRING = f"HostName={IOT_HUB_NAME}.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey={IOT_HUB_KEY}"
registry_manager = IoTHubRegistryManager(IOT_HUB_CONNECTION_STRING)

# Number of simulated devices to create
num_devices = 1000

# Create the simulated devices
for i in range(num_devices):
    # Generate a unique device ID
    device_id = str(uuid.uuid4())

    # Create a device identity object
    device = registry_manager.create_device_with_sas(
        device_id, key_generator(), key_generator(), "enabled"
    )
    print(f"Created device: {device_id}")

# Get the list of devices
devices = registry_manager.get_devices()

# Initialize an empty list
device_list = []

# Iterate over the devices list
for i, device in enumerate(devices):
    # Create a dictionary with the device ID and primary key as the keys and the corresponding values
    device_dict = {
        "device_id": device.device_id,
        "key": device.authentication.symmetric_key.primary_key,
        "location": i,
    }
    # Append the dictionary to the device_list
    device_list.append(device_dict)

# Write the device_list to a file called iot_devices.json
with open("iot_devices/iot_devices.json", "w") as f:
    json.dump(device_list, f, indent=5)
