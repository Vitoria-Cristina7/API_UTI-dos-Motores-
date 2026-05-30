from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import asyncpg

app = FastAPI()

class OrdemCriada(BaseModel):
    nome_cliente: str
    motor: str
    problema: str

class OrdemAtualizada(BaseModel):
    nome_cliente: str
    motor: str
    problema: str
    status: str

async def get_db_connection():
    return await asyncpg.connect(
        user="postgres",
        password="bddinfomat",
        database="UTI dos Motores",
        host="localhost"
    )