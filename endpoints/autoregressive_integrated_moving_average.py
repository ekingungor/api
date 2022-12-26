from fastapi import APIRouter
from api.data_layer.azure_tables import AzureTables
from statsmodels.tsa.arima.model import ARIMA
from random import random
from api.utils.time_parser import parser


router = APIRouter()

@router.get("/autoregressive-integrated-moving-average/{location}/{field}/{steps}")
def autoregressive_integrated_moving_average(location: int, field: str, steps: int):
    entities = []
    az_tables = AzureTables()
    entity_page_generator = az_tables.query_location_pager(location,select=[field])
    for entity_page in entity_page_generator:
        entities = entities + entity_page

    entities.sort(key=lambda d: parser(d['IotHubArrival']))

    data = [entity[field] for entity in entities]

    # contrived dataset
    data = [x + random() for x in range(1, 100)]
    # fit model
    model = ARIMA(data, order=(1, 1, 1))
    model_fit = model.fit()
    # make prediction
    yhat = model_fit.predict(len(data), len(data) + steps, typ='levels')
    print(yhat)
    return yhat.tolist()
    
    