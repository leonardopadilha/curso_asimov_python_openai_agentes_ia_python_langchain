"""
Indo para um exemplo um pouco mais complexo. Digamos que temos um chatbot e queremos fazer um roteamento
para os setores de interesse, no nosso caso atendimento_cliente, duvidas_alunos, vendas, spam. A primeira etapa é
criar um modelo que entenda a solicitação do cliente e direcione para o setor certo. Nas próximas etapas o
atendimento pode ser continuado por pessoas ou por agentes especializados para as tarefas do setor. Retiramos
as seguintes mensagens de email recebidos pela nossa equipe de atendimento e vamos tentar criar um
direcionamento para elas.
"""

duvidas = [
    'Bom dia, gostaria de saber se há um certificado final para cada trilha ou se os certificados são somente para os cursos e projetos? Obrigado!',
    'In Etsy, Amazon, eBay, Shopify https://pint77.com Pinterest+SEO +II = high sales results',
    'Boa tarde, estou iniciando hoje e estou perdido. Tenho vários objetivos. Não sei nada programação, exceto que utilizo o Power automate desktop da Microsoft. Quero aprender tudo na plataforma que se relacione ao Trading de criptomoedas. Quero automatizar Tradings, fazer o sistema reconhecer padrões, comprar e vender segundo critérios que eu defina, etc. Também tenho objetivos de aprender o máximo para utilizar em automações no trabalho também, que envolve a área jurídica e trabalho em processos. Como sou fã de eletrônica e tenho cursos na área, também queria aprender o que precisa para automatizacões diversas. Existe algum curso ou trilha que me prepare com base para todas essas áreas ao mesmo tempo e a partir dele eu aprenda isoladamente aquilo que seria exigido para aplicar aos meus projetos?',
    'Bom dia, Havia pedido cancelamento de minha mensalidade no mes 2 e continuaram cobrando. Peço cancelamento da assinatura. Peço por gentileza, para efetivarem o cancelamento da assomatura e pagamento.',
    'Bom dia. Não estou conseguindo tirar os certificados dos cursos que concluí. Por exemplo, já consegui 100% no python starter, porém, não consigo tirar o certificado. Como faço?',
    'Bom dia. Não enconte no site o preço de um curso avulso. SAberiam me informar?'
]

from enum import Enum
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

load_dotenv()

class SetorEnum(str, Enum):
    atendimento_cliente = 'atendimento_cliente'
    duvidas_aluno = 'duvidas_aluno'
    vendas = 'vendas'
    spam = 'spam'

class DirecionaSetorResponsavel(BaseModel):
    """Direciona a dúvida de um cliente ou aluno da escola de programação Asimov para o setor responsável"""
    setor: SetorEnum

tool_direcionamento = convert_to_openai_function(DirecionaSetorResponsavel)

prompt = ChatPromptTemplate.from_messages([
    ('system', 'Pense com cuidado ao categorizar o texto conforme as instruções'),
    ('user', '{input}')
])

chat = ChatOpenAI()

chain = (prompt 
            | chat.bind(functions=[tool_direcionamento], function_call={'name': 'DirecionaSetorResponsavel'}) 
            | JsonOutputFunctionsParser()
        )

duvida = duvidas[5]
resposta = chain.invoke({'input': duvida})
print('Dúvida: ', duvida)
print('Resposta: ', resposta)

print()

# Melhorando o prompt
system_message = '''Pense com cuidado ao categorizar o texto conforme as instruções.
    Questões relacionadas a dúvidas de preço, sobre o produto, como funciona devem ser direciodas para "vendas".
    Questões relacionadas a conta, acesso a plataforma, a cancelamento e renovação de assinatura para devem ser direciodas para "atendimento_cliente".
    Questões relacionadas a dúvidas técnicas de programação, conteúdos da plataforma ou tecnologias na área da programação devem ser direciodas para "duvidas_alunos".
    Mensagens suspeitas, em outras línguas que não português, contendo links devem ser direciodas para "spam".
'''

prompt = ChatPromptTemplate.from_messages([
    ('system', system_message),
    ('user', '{input}')
])

chat = ChatOpenAI()

chain = (prompt 
            | chat.bind(functions=[tool_direcionamento], function_call={'name': 'DirecionaSetorResponsavel'}) 
            | JsonOutputFunctionsParser()
        )

duvida = duvidas[5]
resposta = chain.invoke({'input': duvida})
print('Dúvida: ', duvida)
print('Resposta: ', resposta)
