from fastapi import FastAPI

from app.database import Base, engine
from app.routes.tickets import router as tickets_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Automation Pro",
    description="Agente de IA e RPA para tratamento de chamados",
    version="1.0.0",
)

app.include_router(tickets_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}