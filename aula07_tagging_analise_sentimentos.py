"""
Tagging - Interpretando dados com funções
Uma das principais aplicações das funções externas por desenvolvedores não é exatamente na utilização dessas
funções e sim, na utilização desta sintaxe e estruturação de dados gerados pela API da OpenAI para a categorização
e estruturação de dados em texto. Daremos um exemplo aqui ao categorizamento de falas.
"""
from pydantic import BaseModel, Field
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

load_dotenv()

class Sentimento(BaseModel):
    '''Define o sentimento e a língua da mensagem enviada'''
    sentimento: str = Field(description='Sentimento do texto. Deve ser "pos" para positivo, "neg" para negativo ou "nd" para não definido.')
    lingua: str = Field(description='Língua que o texto foi escrito (deve estar no formato ISO 639-1)')

tool_sentimento = convert_to_openai_function(Sentimento)
#print(tool_sentimento)

prompt = ChatPromptTemplate.from_messages([
    ('system', 'Pense com cuidado ao categorizar o texto conforme as instruções'),
    ('user', '{input}')
])

chat = ChatOpenAI()

texto = 'Eu gosto muito de massa aos quatro queijos'
text = "I don't like this kind of food because is not very healthy"


chain = prompt | chat.bind(functions=[tool_sentimento], function_call={'name': 'Sentimento'})
resposta = chain.invoke({'input': text})
print(resposta)

print()
print ("#" * 50)
print()

chain = (prompt 
        | chat.bind(functions=[tool_sentimento], function_call={'name': 'Sentimento'})
        | JsonOutputFunctionsParser())

resposta = chain.invoke({'input': text})
print(resposta)       


