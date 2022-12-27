from azure.iot.hub import IoTHubRegistryManager

IOT_HUB_NAME = "myhub-1"
IOT_HUB_KEY = "LNmnGL0vP7zOKK4tsvHast9qvJ5DnRlH0CAvCik7WtI="

IOT_HUB_CONNECTION_STRING = f"HostName={IOT_HUB_NAME}.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey={IOT_HUB_KEY}"
# Replace <IOTHUB_CONNECTION_STRING> with the connection string for your IoT hub
registry_manager = IoTHubRegistryManager(IOT_HUB_CONNECTION_STRING)

# Get a list of devices
devices = registry_manager.get_devices()

# Iterate over the devices list
for device in devices:
    # Delete the device
    registry_manager.delete_device(device.device_id)
    print(f"Deleted device: {device.device_id}")
