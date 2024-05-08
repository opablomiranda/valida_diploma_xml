from fastapi import FastAPI
from app.routers.routes import router
#from app.middleware.middleware import log_requests
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()
#app.middleware("http")(log_requests)
app.add_middleware(  
    CORSMiddleware,
    allow_origins=["*"], #Permitir solicitações de qualquer origem
    allow_credentials=True,
    allow_methods=["*"], #Permitir todos os métodos (GET, POST)
    allow_headers=["*"], #Permitir todos os cabeçalhos
)
app.include_router(router)