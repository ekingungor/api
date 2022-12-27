from azure.data.tables import TableServiceClient, TableEntity, EntityProperty

SERVICE_BUS_CONNECTION_STR = "Endpoint=sb://iothubsbus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=JbgTg88r5U+6x6dAAA3dnHS2uyToyx8MhFfrwmvgXcA="
STORAGE_ACCOUNT_CONNECTION_STR = "DefaultEndpointsProtocol=https;AccountName=myresourcegroup849e;AccountKey=s6L9PM0sRXdOvsWFsqWgxYI/9n/k/HZPp9Urv5+vpIohppbMfpho2owf+xycxurUPABAAJujYZ+n+AStLvg7Lw==;EndpointSuffix=core.windows.net"
QUEUE_NAME = "queue1"
TABLE_NAME = "TelemetryData"


table_service_client = TableServiceClient.from_connection_string(
    conn_str=STORAGE_ACCOUNT_CONNECTION_STR
)
# table_client = table_service_client.get_table_client(table_name=TABLE_NAME)
# table_client.delete_table()
table_service_client.create_table(TABLE_NAME)
