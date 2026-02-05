from langchain.chains.llm import LLMChain
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-3.5-turbo-0125')
prompt = ChatPromptTemplate.from_template('Crie uma frase sobre o seguinte assunto: {assunto}')
output_parser = StrOutputParser()

chain = LLMChain(
    llm=model,
    prompt=prompt,
    output_parser=output_parser
)
resposta = chain.invoke({'assunto': 'futebol'})
print(resposta)