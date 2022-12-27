from azure.servicebus import (
    ServiceBusClient,
    ServiceBusMessage,
    ServiceBusReceiveMode,
    ServiceBusReceivedMessage,
)
from azure.data.tables import TableServiceClient, TableEntity, EntityProperty
import json
import os

SERVICE_BUS_CONNECTION_STR = os.getenv("SERVICE_BUS_CONNECTION_STR")
STORAGE_ACCOUNT_CONNECTION_STR = os.getenv("STORAGE_ACCOUNT_CONNECTION_STR")
QUEUE_NAME = "queue1"
TABLE_NAME = "TelemetryData"


DEBUG = False
BATCH_SIZE = 30

servicebus_client = ServiceBusClient.from_connection_string(
    conn_str=SERVICE_BUS_CONNECTION_STR, logging_enable=True
)
table_service_client = TableServiceClient.from_connection_string(
    conn_str=STORAGE_ACCOUNT_CONNECTION_STR
)
while True:
    entities = []
    with servicebus_client:
        # get the Queue Receiver object for the queue
        receiver = servicebus_client.get_queue_receiver(
            queue_name=QUEUE_NAME,
            max_wait_time=5,
            prefetch_count=BATCH_SIZE,
            receive_mode=(
                ServiceBusReceiveMode.RECEIVE_AND_DELETE
                if not DEBUG
                else ServiceBusReceiveMode.PEEK_LOCK
            ),
        )
        count = 0
        with receiver:
            for msg in receiver:
                count = count + 1
                print(msg)
                msg_body = json.loads(str(msg))
                if DEBUG:
                    receiver.complete_message(msg)
                entity_dict = {}
                entity_dict["PartitionKey"] = "Sensors"

                entity_dict["RowKey"] = msg.message_id
                entity_dict["DeviceId"] = msg.message.application_properties[
                    b"iothub-connection-device-id"
                ].decode("utf-8")
                entity_dict["IotHubArrival"] = msg.application_properties[
                    b"iothub-enqueuedtime"
                ].decode("utf-8")
                entity_dict["carbonDioxideAlert"] = msg.message.application_properties[
                    b"carbonDioxideAlert"
                ].decode("utf-8")

                for key, value in msg_body.items():
                    entity_dict[key] = value
                entity = TableEntity(entity_dict)
                entities.append(entity)
                print(entity)
                if count == BATCH_SIZE:
                    break

    table_client = table_service_client.get_table_client(table_name=TABLE_NAME)
    for entity in entities:

        try:
            table_client.create_entity(entity)
        except Exception as e:
            print(
                f"Some error occurred while saving to the table. Error message: \n {e}"
            )

    if DEBUG:
        break
