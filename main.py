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

@app.get("/status")
async def status():
    return {"mensagem": "API funcionando"}

@app.post("/ordens")
async def criar_ordem(ordem: OrdemCriada):

    conn = await get_db_connection()

    result = await conn.execute(
        """
        INSERT INTO ordens_servico (nome_cliente, motor, problema)
        VALUES ($1, $2, $3)
        """,
        ordem.nome_cliente,
        ordem.motor,
        ordem.problema
    )

    await conn.close()

    if result == "INSERT 0 1":
        return {"message": "Ordem de serviço criada com sucesso!"}
    else:
        return {"message": "Ordem de serviço não foi criada."}