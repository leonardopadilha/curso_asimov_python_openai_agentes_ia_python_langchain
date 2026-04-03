"""
Criando tool com StructuredTool
Outra forma de criar uma tool sem o decorador é utilizando a metaclasse StructuredTool do LangChain. As  funcionalidades 
são bem similares, então você pode utilizar um ou outro dependendo da sua preferência.  
"""

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class RetornaTempArgs(BaseModel):
    localidade: str = Field(description='Localidade a ser buscada', examples=['São Paulo', 'Porto Alegre'])

def retorna_temperatura_atual(localidade: str):
    return '25ºC'

tool_temp = StructuredTool.from_function(
    func=retorna_temperatura_atual,
    name='ToolTemperatura',
    args_schema=RetornaTempArgs,
    description='Faz busca online de temperatura de uma localidade',
    return_direct=True
)

resposta = tool_temp.invoke({'localidade': 'Porto Alegre'})
print(resposta)