# app/main.py
from fastapi import FastAPI
from .api.v1.health import router as health_router
from .api.v1.agents import router as agents_router
from .api.v1.properties import router as properties_router
from .api.v1.chat import router as chat_router
from .api.v1.pdf import router as pdf_router

app = FastAPI(title="SA Thomson Nerys Chatbot API", version="0.2.0")

app.include_router(health_router,     prefix="/api/v1", tags=["health"])
app.include_router(agents_router,     prefix="/api/v1", tags=["agents"])
app.include_router(properties_router, prefix="/api/v1", tags=["properties"])
app.include_router(chat_router,       prefix="/api/v1", tags=["chat"])
app.include_router(pdf_router,        prefix="/api/v1", tags=["pdf"])

@app.get("/")
def root():
    return {"service": "satn-chatbot", "status": "running"}
