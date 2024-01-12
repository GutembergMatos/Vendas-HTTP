from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from typing import List, Optional
from pydantic import field_validator
from fastapi import status
from fastapi.responses import HTMLResponse

app = FastAPI()

class Item(BaseModel):
    id: Optional[str] = ''
    nome:str
    valor:float
    quantidade:int

    @field_validator("valor")
    @classmethod
    def validar_valor(cls,valor:float)->float:
        if valor <= 0: 
            raise ValueError("valor não pode ser negativo")
        return valor
    
    @field_validator("quantidade")
    @classmethod
    def validar_quantidade(cls,quantidade:int)->int:
        if quantidade <= 0:
            raise ValueError("sem produto no estoque")
        return quantidade
    
    @field_validator("nome")
    @classmethod
    def validar_nome(cls,nome:str)->str:
        if len(nome) >= 50:
            raise ValueError("quantidade de caracteres execida")
        return nome

lista_de_items = {}


@app.post("/item")
async def createitem(item:Item):
    id_a_ser_utilizado =  uuid4().hex
    item.id = id_a_ser_utilizado
    lista_de_items[id_a_ser_utilizado] = item    #chave do item em hexadecimal
    return {"message": "item criado com sucesso!" } 

@app.get("/item")
async def readitem(item_id): # da forma que eu pensei kakakkak...
    result = lista_de_items.get(item_id, None)
    if result is None:
        return HTMLResponse(content="Item nao encontrado", status_code=404)
    
    return result

@app.get("/item/all")
async def readitems()->List[Item]:
    return list(lista_de_items.values())

@app.delete("/item/{item_id}")
async def deleteitem(item_id:str):
    if item_id in lista_de_items:
        del lista_de_items[item_id]
        return{"message": "Item deletado com sucesso!"}
    else:
        return HTMLResponse(content="Item não encontrado", status_code=404)
@app.put("/item/{item_id}")
async def updateitem(item:Item):
    if item_id in lista_de_items:
        # Atualiza os valores do item com os novos valores fornecidos
        lista_de_items[item_id].nome = updated_item.nome
        lista_de_items[item_id].valor = updated_item.valor
        lista_de_items[item_id].quantidade = updated_item.quantidade
        return {"message": "Item atualizado com sucesso!"}
    else:
        return HTMLResponse(content="Item não encontrado", status_code=404)
