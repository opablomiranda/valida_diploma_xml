from fastapi import FastAPI
from app.routers.routes import router
from app.middleware.middleware import log_requests


app = FastAPI()
app.include_router(router)
app.middleware("http")(log_requests)