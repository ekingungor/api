import os
from azure.data.tables import TableServiceClient, TableEntity, EntityProperty
from azure.core.exceptions import HttpResponseError

STORAGE_ACCOUNT_CONNECTION_STR = os.getenv("STORAGE_ACCOUNT_CONNECTION_STRING")
TABLE_NAME = "TelemetryData"
BATCH_SIZE = 100

class AzureTables():
    def __init__(self):
        self._service_client = TableServiceClient.from_connection_string(conn_str=STORAGE_ACCOUNT_CONNECTION_STR)
        
    def _get_table_client(self, table_name=TABLE_NAME):
        return self._service_client.get_table_client(table_name=table_name)

    def query_location_pager(self, location: int, select = []):
        #["IotHubArrival", "Temperature", "Humidity", "Oxygen", "CarbonDioxide", "Location"]
        select.append("IotHubArrival")
        with self._get_table_client() as table_client:
            try:
                parameters = {"location": location}
                temperature_filter = f"Location eq @location"

                queried_entities = table_client.query_entities(
                    query_filter=temperature_filter, parameters=parameters, select=select,results_per_page=BATCH_SIZE
                )
                entities = []
                count = 0

                for entity_chosen in queried_entities:
                    print(entities)
                    count = count + 1
                    corrupt = False
                    for key in select:
                        if entity_chosen[key] is None:
                            corrupt = True
                    if not corrupt:
                        entities.append(entity_chosen)
                    else:
                        count = count - 1

                    if count == BATCH_SIZE:
                        yield entities
                        count = 0
                        entities = []
                    
                yield entities
                
                
            except HttpResponseError as e:
                print(e.message)
    