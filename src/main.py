from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import models  # noqa: F401
from .database import Base, engine, get_db

from .routers import cartoes, catraca


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="ViaPass", lifespan=lifespan)
app.include_router(catraca.router)
app.include_router(cartoes.router)


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "banco": "conectado"}