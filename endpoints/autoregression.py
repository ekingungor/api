from fastapi import APIRouter
from api.data_layer.azure_tables import AzureTables
from statsmodels.tsa.ar_model import AutoReg
from random import random
from api.utils.time_parser import parser


router = APIRouter()

@router.get("/autoregression/{location}/{field}/{steps}")
def autoregression(location: int, field: str, steps: int):
    entities = []
    az_tables = AzureTables()
    entity_page_generator = az_tables.query_location_pager(location,select=[field])
    for entity_page in entity_page_generator:
        entities = entities + entity_page

    print("LENGHT::", len(entities))

    entities.sort(key=lambda d: parser(d['IotHubArrival']))
    

    data = [entity[field] for entity in entities]
    model = AutoReg(data, lags=1)
    model_fit = model.fit()
    # make prediction
    yhat = model_fit.predict(len(data), len(data) + steps)
    return yhat.tolist()
    
    