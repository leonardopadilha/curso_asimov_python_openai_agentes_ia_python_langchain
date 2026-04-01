from langchain.agents import tool
from pydantic import BaseModel, Field

'''
@tool # É um decorador, o decorador modifica uma função dada as próprias condições do decorador
def retorna_temperatura_atual(localidade: str):
    """Faz busca online de temperatura de uma localidade"""
    return '25ºC'
'''

class RetornaTempArgs(BaseModel):
    localidade: str = Field(description = 'Localidade a ser buscada', examples=['São Paulo', 'Porto Alegre'])

@tool(args_schema = RetornaTempArgs)
def retorna_temperatura_atual(localidade: str):
     '''Faz busca online de temperatura de uma localidade'''
     return '25ºC'

#print(retorna_temperatura_atual.args)
resposta = retorna_temperatura_atual.invoke({'localidade': 'Porto Alegre'})
print(resposta)


