from fastapi import APIRouter
from api.data_layer.azure_tables import AzureTables

from statsmodels.tsa.statespace.sarimax import SARIMAX
from random import random

from api.utils.time_parser import parser


router = APIRouter()

@router.get("/seasonal-autoregressive-integrated-moving-average/{location}/{field}/{steps}")
def seasonal_autoregressive_integrated_moving_average(location: int, field: str, steps: int):
    entities = []
    az_tables = AzureTables()
    entity_page_generator = az_tables.query_location_pager(location,select=[field])
    for entity_page in entity_page_generator:
        entities = entities + entity_page

    entities.sort(key=lambda d: parser(d['IotHubArrival']))

    
    # contrived dataset
    data = [entity[field] for entity in entities]
    # fit model
    model = SARIMAX(data, order=(1, 1, 1), seasonal_order=(0, 0, 0, 0))
    model_fit = model.fit(disp=False)
    # make prediction
    yhat = model_fit.predict(len(data), len(data) + steps)
    print(yhat)
    return yhat.tolist()
    
    