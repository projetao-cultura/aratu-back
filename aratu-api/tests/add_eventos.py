import requests
from datetime import datetime, timedelta

# URL do endpoint para criar eventos
url = "http://localhost:8080/eventos/"
# Gerar datas de início e fim para os eventos
data_inicio = datetime.now()
data_fim = data_inicio + timedelta(hours=4)

# Formatar as datas para strings no formato ISO 8601
data_inicio_str = data_inicio.strftime('%Y-%m-%dT%H:%M:%SZ')
data_fim_str = data_fim.strftime('%Y-%m-%dT%H:%M:%SZ')

eventos_para_adicionar = [
    {
        "nome": "Contação de Histórias Infantis",
        "descricao": "Uma tarde mágica para as crianças com as melhores histórias.",
        "categoria": ["Infantil"],
        "local": "Biblioteca Municipal",
        "endereco": "Rua das Flores, 123",
        "data_hora": data_inicio_str,
        "data_fim": data_fim_str,
        "fonte": "Biblioteca Municipal",
        "organizador": "Prefeitura da Cidade",
        "gratis": True,
        "atualizado_em": data_inicio_str,
        "valor": 0.0,
    },
    {
        "nome": "Show de Talentos da Cidade",
        "descricao": "Venha ver os talentos mais incríveis da nossa cidade em uma noite inesquecível.",
        "categoria": ["Show", "Adulto"],
        "local": "Teatro da Cidade",
        "endereco": "Avenida Central, 456",
        "data_hora": data_inicio_str,
        "data_fim": data_fim_str,
        "fonte": "Teatro Municipal",
        "organizador": "Casa de Cultura",
        "gratis": False,
        "atualizado_em": data_inicio_str,
        "valor": 50.0,
    },
    {
        "nome": "Retiro Espiritual",
        "descricao": "Um fim de semana de paz, meditação e reflexão espiritual.",
        "categoria": ["Religião"],
        "local": "Centro Espiritual Luz Divina",
        "endereco": "Estrada da Serenidade, Km 12",
        "data_hora": data_inicio_str,
        "data_fim": data_fim_str,
        "fonte": "Luz Divina",
        "organizador": "Comunidade Luz Divina",
        "gratis": False,
        "atualizado_em": data_inicio_str,
        "valor": 120.0,
    },
    {
        "nome": "Festival Sertanejo",
        "descricao": "O maior festival sertanejo da região, com os maiores nomes da música.",
        "categoria": ["Show", "Sertanejo"],
        "local": "Arena Show",
        "endereco": "Avenida dos Eventos, 789",
        "data_hora": data_inicio_str,
        "data_fim": data_fim_str,
        "fonte": "Festival Sertanejo Oficial",
        "organizador": "Produtora de Eventos S.A.",
        "gratis": False,
        "atualizado_em": data_inicio_str,
        "valor": 80.0,
    },
    {
        "nome": "Caminhada Ecológica",
        "descricao": "Conecte-se com a natureza em uma caminhada ecológica pelos caminhos do Parque da Cidade.",
        "categoria": ["Ar Livre"],
        "local": "Parque da Cidade",
        "endereco": "Rua do Parque, s/n",
        "data_hora": data_inicio_str,
        "data_fim": data_fim_str,
        "fonte": "Secretaria de Meio Ambiente",
        "organizador": "Prefeitura da Cidade",
        "gratis": True,
        "atualizado_em": data_inicio_str,
        "valor": 0.0,
    },
    # Adicione mais 5 eventos seguindo a estrutura acima
]

# Cabeçalhos para a requisição
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    # Inclua outros cabeçalhos necessários, como tokens de autenticação
}

# Enviar requisição para criar cada evento
for evento in eventos_para_adicionar:
    response = requests.post(url, json=evento, headers=headers)
    if response.status_code == 201:
        print(f"Evento '{evento['nome']}' criado com sucesso.")
    else:
        print(f"Erro ao criar o evento '{evento['nome']}': {response.text}")