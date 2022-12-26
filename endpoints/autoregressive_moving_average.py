from fastapi import APIRouter
from api.data_layer.azure_tables import AzureTables
from statsmodels.tsa.arima.model import ARIMA
from random import random
from api.utils.time_parser import parser


router = APIRouter()

@router.get("/autoregressive-moving-average/{location}/{field}/{steps}")
def autoregressive_moving_average(location: int, field: str, steps: int):
    entities = []
    az_tables = AzureTables()
    entity_page_generator = az_tables.query_location_pager(location,select=[field])
    for entity_page in entity_page_generator:
        entities = entities + entity_page

    entities.sort(key=lambda d: parser(d['IotHubArrival']))

    # MA example
    
    # contrived dataset
    data = [entity[field] for entity in entities]
    # fit model
    model = ARIMA(data, order=(2, 0, 1))
    model_fit = model.fit()
    # make prediction
    yhat = model_fit.predict(len(data), len(data) + steps)
    print(yhat)
    return yhat.tolist()

    
    