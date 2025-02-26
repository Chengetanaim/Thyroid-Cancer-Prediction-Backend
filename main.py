from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routes import prediction

app = FastAPI(title="Thyroid Cancer Prediction")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(prediction.router)
