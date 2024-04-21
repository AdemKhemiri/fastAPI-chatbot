from fastapi import FastAPI
# from routes.route import router
from routes.devices_form import api
from fastapi.middleware.cors import CORSMiddleware

import uvicorn


import warnings
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(router)
app.include_router(api)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True, workers=2)

