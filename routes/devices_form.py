from fastapi import APIRouter
from bson import ObjectId
from datetime import date
from datetime import datetime
from models.form_model import FormModel
from config.database import device_types, sensor_consumer_types, sensor_generator_types, models, trademarks, db_devices
import asyncio
import json
from fastapi.responses import JSONResponse
api = APIRouter(
    prefix="/devices"
)


@api.get("/get-models")
async def get_models(trademark_id: int):
    try:
        model_devices = []
        # Assuming models is a collection or a query object
        response = models.find({"trademarkID": trademark_id})
        for res in response:
            model_devices.append({
                "_id": str(res["_id"]),
                "trademarkID": res["trademarkID"],
                "name": res["name"],
                "path": res["path"]
            })
        return model_devices
    except Exception as e:
        errors = str(e)
        raise ValueError(errors) from e


@api.get("/get-device-types")
async def get_device_types():
    try:
        types = []
        # Assuming models is a collection or a query object
        response = device_types.find()
        for res in response:
            types.append({
                "_id": str(res["_id"]),
                "deviceID": res["deviceID"],
                "name": res["name"],
            })
        return types
    except Exception as e:
        errors = str(e)
        raise ValueError(errors) from e


@api.get("/get-sensor-consumer-types")
async def get_sensor_consumer_types():
    try:
        consumer_types = []
        # Assuming models is a collection or a query object
        response = sensor_consumer_types.find()
        for res in response:
            consumer_types.append({
                "_id": str(res["_id"]),
                "name": res["name"]
            })
        return consumer_types
    except Exception as e:
        errors = str(e)
        raise ValueError(errors) from e


@api.get("/get-sensor-generator-types")
async def get_sensor_consumer_types():
    try:
        generator_types = []
        # Assuming models is a collection or a query object
        response = sensor_generator_types.find()
        for res in response:
            generator_types.append({
                "_id": str(res["_id"]),
                "name": res["name"]
            })
        return generator_types
    except Exception as e:
        errors = str(e)
        raise ValueError(errors) from e


@api.get("/get-trademarks")
async def get_trademarks():
    try:
        constructor = []
        # Assuming models is a collection or a query object
        response = trademarks.find()
        for res in response:
            constructor.append({
                "_id": str(res["_id"]),
                "trademarkID": res["trademarkID"],
                "name": res["name"],
                "path": res["path"]
            })
        return constructor
    except Exception as e:
        errors = str(e)
        raise ValueError(errors) from e


@api.post("/send-submit-form")
async def send_submit_orm(form: FormModel):
    try:
        print(form)
        response = db_devices.insert_one(dict(form))
        print(response)
        return JSONResponse(status_code=200, content={"status": "success"})
    except Exception as e:
        raise ValueError(str(e)) from e

