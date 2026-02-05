from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatOpenAI(model='gpt-3.5-turbo-0125')

prompt = ChatPromptTemplate.from_template('Crie uma frase sobre o seguinte assunto: {assunto}')

chain = prompt | model
resposta = chain.invoke({'assunto': 'futebol'})
#print(resposta)
print(resposta.content)