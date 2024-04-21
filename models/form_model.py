from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime



class FormModel(BaseModel):
    name: str
    deviceType: Dict
    deviceTrademark: Dict
    deviceModel: str
    placedDate: datetime
    dataSheetURL: str
    deviceImage: str
    sensorType: Dict
    index: str
    parentDevice: str
    sensorConstructor: Dict
    sensorModel: Dict
    ipAddress: str
    port: str
    zone: str
    sensorID: str
    gatewayType: str
    gatewayID: str
