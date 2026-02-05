from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatOpenAI(model='gpt-3.5-turbo-0125')

prompt = ChatPromptTemplate.from_template('Crie uma frase sobre o seguinte assunto: {assunto}')

chain = prompt | model | StrOutputParser()
resposta = chain.invoke({'assunto': 'futebol'})
print(resposta)

"""
A Ordem Importa:
Para atingir o mesmo objetivo sem a criação da chain, os passos que devem ser seguidos são:
1. Formatar o prompt template
2. Enviar o prompt formatado para o modelo
3. Fazer o parseamento da saída do modelo. Essa mesma ordem deve ser seguida para que não ocorra erros.

Para não errar a ordem
É importante entendermos que cada componente recebe um tipo de entrada e gera um tipo de saída, e 
estes tipos precisam casar:

| Component       | Tipo de Entrada                                         | Tipo de Saída        |
|-----------------|---------------------------------------------------------|----------------------|
| Prompt          | Dicionário                                              | PromptValue          |
| ChatModel       | String única, lista de mensagens de chat ou PromptValue | Mensagem de Chat     |
| LLM             | String única, lista de mensagens de chat ou PromptValue | String               |
| OutputParser    | A saída de um LLM ou ChatModel                          | Depende do parser    |
| Retriever       | String única                                            | Lista de Documentos  |
| Tool            | String única ou dicionário, dependendo da ferramenta    | Depende da ferramenta|

"""