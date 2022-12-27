import sys
import os
sys.path.insert(0, os.getcwd())

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from api.endpoints import (
    autoregression, 
    moving_average, 
    autoregressive_moving_average,
    autoregressive_integrated_moving_average,
    seasonal_autoregressive_integrated_moving_average,
    vector_autoregression
    )

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(autoregression.router)
app.include_router(moving_average.router)
app.include_router(autoregressive_moving_average.router)
app.include_router(autoregressive_integrated_moving_average.router)
app.include_router(seasonal_autoregressive_integrated_moving_average.router)
app.include_router(vector_autoregression.router)


@app.get("/")
def home():
    return "Welcome to the home page!"


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, log_level='debug')
