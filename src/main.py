from fastapi import FastAPI, Depends, Query, Body
from typing import Optional
from crud import Database
from models import ItemCreate, ItemUpdate, ResponseMessage, Item

app = FastAPI()
db = Database()

@app.get("/select")
def get_data():
    """ Get all records using original endpoint"""
    return db.select_all()

@app.get("/items")
def get_items():
    """ Get all records using REST endpoint"""
    return db.select_all()

# Query_param
@app.post("/insert")
def insert_data_query(nome: str, idade: int):
    """ Create record with query parameters (original method)"""
    db.insert_data(nome, idade)
    return {"message": "Dados inseridos com sucesso!"}


# JSON_param
@app.post("/items")
def insert_data_json(item: ItemCreate):
    """ Create record with JSON body (REST method)"""
    db.insert_data(item.nome, item.idade)
    return ResponseMessage(message="Dados inseridos com sucesso!")

# Query_param
@app.put("/update")
def update_data_query(id: int, nome: str, idade: int):
    """ Update record with query parameters (original method)"""
    db.update_data(id, nome, idade)
    return {"message": "Dados atualizados com sucesso!"}

# JSON_param
@app.put("/items/{item_id}")
def update_data_json(item_id: int, item: ItemUpdate):
    """ Update record with JSON body (REST method)"""
    # Only update fields that were provided
    current_data = db.select_by_id(item_id)
    if not current_data:
        return {"message": "Registro não encontrado!"}
        
    nome = item.nome if item.nome is not None else current_data["nome"]
    idade = item.idade if item.idade is not None else current_data["idade"]
    
    db.update_data(item_id, nome, idade)
    return ResponseMessage(message="Dados atualizados com sucesso!")

# Query_param
@app.delete("/delete")
def delete_data_query(id: int):
    """Delete record with query parameter (original method)"""
    db.delete_data(id)
    return {"message": "Registro deletado!"}

# JSON_param
@app.delete("/items/{item_id}")
def delete_data_json(item_id: int):
    """Delete record with path parameter (REST method)"""
    db.delete_data(item_id)
    return ResponseMessage(message="Registro deletado!")