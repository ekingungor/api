from fastapi import APIRouter
from api.data_layer.azure_tables import AzureTables

from statsmodels.tsa.vector_ar.var_model import VAR
from random import random

from api.utils.time_parser import parser

router = APIRouter()

@router.get("/vector-autoregression/{location}/{field_1}/{field_2}/{steps}")
def vector_autoregression(location: int, field_1: str, field_2: str, steps: int):
    entities = []
    az_tables = AzureTables()
    entity_page_generator = az_tables.query_location_pager(location, select=[field_1, field_2])
    for entity_page in entity_page_generator:
        entities = entities + entity_page

    entities.sort(key=lambda d: parser(d['IotHubArrival']))

    # MA example
    
    # contrived dataset
    data = [[entity['Temperature'], entity['Humidity'], entity['Oxygen'], entity['CarbonDioxide']] for entity in entities]
    print("len of fdatataaa: ", len(data))
    # fit model
    model = VAR(data)
    model_fit = model.fit()
    # make prediction
    yhat = model_fit.forecast(model_fit.endog, steps=TIME_STEPS)
    print(yhat)
    return yhat.tolist()
    
    