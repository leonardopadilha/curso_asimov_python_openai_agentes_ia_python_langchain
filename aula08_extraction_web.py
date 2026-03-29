import os
from dotenv import load_dotenv

load_dotenv()

SITE = "https://hub.asimov.academy/blog/"

from langchain_community.document_loaders.web_base import WebBaseLoader
from pydantic import BaseModel, Field
from typing import List
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

loader = WebBaseLoader(SITE)
page = loader.load()
# print(page)


class BlogPost(BaseModel):
    '''Informações sobre um post de blog'''
    titulo: str = Field(description='O título do post de blog')
    autor: str = Field(description='O autor do post de blog')
    data: str = Field(description='A data de publicação do post de blog')


class BlogSite(BaseModel):
    '''Lista de blog posts de um site'''
    posts: List[BlogPost] = Field(description='Lista de posts de blog do site')

tool_blog = convert_to_openai_function(BlogSite)
#print(tool_blog)

chat = ChatOpenAI()

prompt = ChatPromptTemplate.from_messages([
    ('system', 'Extraia da página todos os posts de blog com autor e data de publicação'),
    ('user', '{input}')
])

chain = (prompt
        | chat.bind(functions=[tool_blog], function_call={'name': 'BlogSite' })
        | JsonKeyOutputFunctionsParser(key_name='posts'))

resposta = chain.invoke({'input': page})
print(resposta)
