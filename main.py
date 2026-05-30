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

@app.get("/ordens")
async def listar_ordens():

    conn = await get_db_connection()

    ordens = await conn.fetch(
        """
        SELECT * FROM ordens_servico
        """
    )

    await conn.close()

    lista_ordens = []

    for ordem in ordens:
        lista_ordens.append({
            "id": ordem["id"],
            "nome_cliente": ordem["nome_cliente"],
            "motor": ordem["motor"],
            "problema": ordem["problema"],
            "status": ordem["status"],
            "solucao": ordem["solucao"],
            "data_entrada": str(ordem["data_entrada"]),
            "data_fechamento": str(ordem["data_fechamento"]) if ordem["data_fechamento"] else None
        })

    return lista_ordens

@app.get("/ordens/{id}")
async def buscar_ordem(id: int):

    conn = await get_db_connection()

    ordem = await conn.fetchrow(
        """
        SELECT * FROM ordens_servico
        WHERE id = $1
        """,
        id
    )

    await conn.close()

    if ordem:
        return {
            "id": ordem["id"],
            "nome_cliente": ordem["nome_cliente"],
            "motor": ordem["motor"],
            "problema": ordem["problema"],
            "status": ordem["status"],
            "solucao": ordem["solucao"],
            "data_entrada": str(ordem["data_entrada"]),
            "data_fechamento": str(ordem["data_fechamento"]) if ordem["data_fechamento"] else None
        }
    else:
        return {"message": "Ordem de serviço não encontrada."}
    
@app.put("/ordens/{id}")
async def atualizar_ordem(id: int, ordem: OrdemAtualizada):

    conn = await get_db_connection()

    result = await conn.execute(
        """
        UPDATE ordens_servico
        SET nome_cliente = $2,
            motor = $3,
            problema = $4,
            status = $5
        WHERE id = $1
        """,
        id,
        ordem.nome_cliente,
        ordem.motor,
        ordem.problema,
        ordem.status
    )

    await conn.close()

    if result == "UPDATE 1":
        return {"message": f"Ordem {id} atualizada com sucesso!"}
    else:
        return {"message": "Ordem de serviço não encontrada."}
    
@app.delete("/ordens/{id}")
async def deletar_ordem(id: int):

    conn = await get_db_connection()

    result = await conn.execute(
        """
        DELETE FROM ordens_servico
        WHERE id = $1
        """,
        id
    )

    await conn.close()

    if result == "DELETE 1":
        return {"message": f"Ordem {id} removida com sucesso!"}
    else:
        return {"message": "Ordem de serviço não encontrada."}