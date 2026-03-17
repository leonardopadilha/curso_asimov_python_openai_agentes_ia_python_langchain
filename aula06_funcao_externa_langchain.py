"""
class Pessoa:
    def __init__(self, nome: str, idade: int, peso: float) -> None:
        self.nome = nome
        self.idade = idade
        self.peso = peso
"""

from pydantic import BaseModel

class pydPessoa(BaseModel):
    nome: str
    idade: int
    peso: float

adriano = pydPessoa(nome="Adriano", idade=32, peso=68)
#print(adriano.nome)

from typing import List

class pydAsimoTeam(BaseModel):
    funcionarios: List[pydPessoa]

#print(pydAsimoTeam(funcionarios=[pydPessoa(nome="Adriano", idade=32, peso=68)]))

# Utilizando pydantic para criação de tools da OpenAI
#import json

"""
def obter_temperatura_atual(local, unidade="celsius"):
    if "são paulo" in local.lower():
        return json.dumps(
            {"local": "São Paulo", "temperatura": "32", "unidade": unidade}
        )
    elif "porto alegre": in local.lower():
        return json.dumps(
            {"local": "Porto Alegre", "temperatura": "25", "unidade": unidade}
        )
    else:
        return json.dumps(
            {"local": local, "temperatura": "unknown"}
        )

tools = [
    {
        "type": "function",
        "function": {
            "name": "obter_temperatura_atual",
            "description": "Obtém a temperatura atual em uma dada cidade",
            "parameters": {
                "type": "object",
                "properties": {
                    "local": {
                        "type": "string",
                        "description": "O nome da cidade. Ex: São Paulo",
                    },
                    "unidade": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    },
                },
                "required": ["local"]
            }
        }
    }
]
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class UnidadeEnum(str, Enum):
    celsius = 'celsius'
    fahrenheit = 'fahrenheit'

class ObterTemperaturaAtual(BaseModel):
    """Obtém a temperatura atual de uma determinada localidade"""
    local: str = Field(description='O nome da cidade', examples=['São Paulo', 'Porto Alegre'])
    unidade: Optional[UnidadeEnum]

from langchain_core.utils.function_calling import convert_to_openai_function

tool_temperatura = convert_to_openai_function(ObterTemperaturaAtual)
# print(tool_temperatura)

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI()

resposta = chat.invoke('Qual é a temperatura de Porto Alegre', functions=[tool_temperatura])
#print(resposta)

"""
Também podemos dar um bind e criar um novo componente de chat_model que terá acesso a função sempre que for
chamado o invoke. Nestes dois casos, o modelo se comportará com o parâmetro "auto" de chamamento de função,
ou seja, ele chamará a função quando necessitar, caso contrário se comportará como um modelo de 
linguagem normal.
"""

chat_com_func = chat.bind(functions=[tool_temperatura])
resposta_bind = chat_com_func.invoke('Qual é a temperatura de Porto Alegre?')
#print(resposta_bind)

"""
Podemos obrigar o modelo a sempre chamar uma função da seguinte forma:
"""

resposta_func = chat.invoke(
    'Qual é a temperatura de Porto Alegre?',
    functions=[tool_temperatura],
    function_call={'name': 'ObterTemperaturaAtual'}
)

#print(resposta_func)

"""
Adicionando a uma chain
Podemos adicionar agora este modelo com funções a um prompt e criar uma chain
"""

from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ('system', 'Você é um assistente amigável chamado Asimo'),
    ('user', '{input}')
])

chain = prompt | chat.bind(functions=[tool_temperatura])

resposta = chain.invoke({'input': 'Qual é a temperatura de Floripa?'})
print(resposta)



