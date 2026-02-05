import json

import openai
from dotenv import load_dotenv, find_dotenv

load_dotenv()

client = openai.Client()

def obter_temperatura_atual(local, unidade="celsius"):
    if "são paulo" in local.lower():
        return json.dumps({"local": "São Paulo", "temperatura": "32", "unidade": unidade})
    elif "porto alegre" in local.lower():
        return json.dumps({"local": "Porto Alegre", "temperatura": "25", "unidade": unidade})
    else:
        return json.dumps({"local": local, "temperatura": "unknown"})

#print(obter_temperatura_atual('Porto Alegre'))

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
                "required": ["local"],
            },
        },
    }
]

mensagens = [
    {'role': 'user', 'content': 'Qual é temperatura em Porto Alegre agora?'}
]

resposta = client.chat.completions.create(
    model='gpt-3.5-turbo-0125',
    messages=mensagens,
    tools=tools,
    tool_choice='auto'
)

print(resposta.choices[0].message)
print("-" * 100)
print(resposta.choices[0].message.content)
print("-" * 100)
print(resposta.choices[0].message.tool_calls)
print("-" * 100)
print(resposta.choices[0].message.tool_calls[0].function.arguments)
print("-" * 100)
print(resposta.choices[0].message.tool_calls[0].id)
print("-" * 100)
print(resposta.choices[0].message.tool_calls[0].function.name)
print("-" * 100)

mensagem = resposta.choices[0].message
print(mensagem)
print("-" * 100)
print(mensagem.content)
print(mensagem.tool_calls)
print("-" * 100)

tools_call = mensagem.tool_calls[0]
print(tools_call.id)
print(tools_call.function.name)
print(tools_call.function.arguments)
print("-" * 100)

observacao = obter_temperatura_atual(**json.loads(tools_call.function.arguments))
print(observacao)
print("-" * 100)

mensagens.append(mensagem)
print(mensagens)
print("-" * 100)

mensagens.append({
    'tool_call_id': tools_call.id,
    'role': 'tool',
    'name': tools_call.function.name,
    'content': observacao
})
print(mensagens)
print("-" * 100)

mensagens = [
    {'role': 'user', 'content': 'Qual é temperatura em Porto Alegre agora?'}
]
resposta = client.chat.completions.create(
    model='gpt-3.5-turbo-0125',
    messages=mensagens,
    tools=tools,
    tool_choice='auto'
)
print(resposta)
print("-" * 100)
print(resposta.choices[0].message.content)
print("-" * 100)

mensagem = resposta.choices[0].message
print('Conteúdo:', mensagem.content)
print('Tools:', mensagem.tool_calls)
