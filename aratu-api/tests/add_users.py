import requests

# URL do endpoint para criar usuários
url = "http://localhost:8080/usuarios/"

# Lista de usuários para adicionar
usuarios_para_adicionar = [
    {
        "nome": "Alice Santos",
        "email": "alice.san22tos@example.com",
        "senha": "senha123",
        "telefone": "11998827766",
        "ativo": True,
        "categorias_interesse": ["Infantil", "Ar Livre"]
    },
    {
        "nome": "Carlos Oliveira",
        "email": "carlos.ol22iveira@example.com",
        "senha": "senha123",
        "telefone": "11987276655",
        "ativo": True,
        "categorias_interesse": ["Show", "Sertanejo"]
    },
    {
        "nome": "Julia Martins",
        "email": "julia.mar22tins@example.com",
        "senha": "senha123",
        "telefone": "11987524321",
        "ativo": True,
        "categorias_interesse": ["Religião", "Adulto"]
    },
    {
        "nome": "Roberto Silva",
        "email": "roberto.si22lva@example.com",
        "senha": "senha123",
        "telefone": "2129992887766",
        "ativo": True,
        "categorias_interesse": ["Adulto", "Show"]
    },
    {
        "nome": "Fernanda Gomes",
        "email": "fernanda.go22mes@example.com",
        "senha": "senha123",
        "telefone": "2192882776655",
        "ativo": True,
        "categorias_interesse": ["Ar Livre", "Infantil"]
    },
    {
        "nome": "Lucas Pereira",
        "email": "lucas.per22eira@example.com",
        "senha": "senha123",
        "telefone": "2198762542321",
        "ativo": True,
        "categorias_interesse": ["Sertanejo", "Show"]
    },
    {
        "nome": "Mariana Li2ma",
        "email": "mariana.l2ima@example.com",
        "senha": "senha123",
        "telefone": "319992887766",
        "ativo": True,
        "categorias_interesse": ["Religião", "Ar Livre"]
    },
    {
        "nome": "Tiago R2ocha",
        "email": "tiago.ro2cha@example.com",
        "senha": "senha123",
        "telefone": "319828776655",
        "ativo": True,
        "categorias_interesse": ["Adulto", "Religião"]
    },
    {
        "nome": "Patricia S2ouza",
        "email": "patricia.so2uza@example.com",
        "senha": "senha123",
        "telefone": "319876524321",
        "ativo": True,
        "categorias_interesse": ["Infantil", "Sertanejo"]
    },
    {
        "nome": "Eduardo Me2ndes",
        "email": "eduardo.mend2es@example.com",
        "senha": "senha123",
        "telefone": "119776625544",
        "ativo": True,
        "categorias_interesse": ["Show", "Ar Livre"]
    }
]

# Armazenar os IDs dos usuários criados
ids_usuarios = []

# Cabeçalhos para a requisição
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    # Inclua outros cabeçalhos necessários, como tokens de autenticação
}

# Enviar requisição para criar cada usuário
for usuario in usuarios_para_adicionar:
    response = requests.post(url, json=usuario, headers=headers)
    if response.status_code == 201:
        usuario_criado = response.json()
        print(f"Usuário '{usuario['nome']}' criado com sucesso.")
        ids_usuarios.append(usuario_criado['id'])
    else:
        print(f"Erro ao criar o usuário '{usuario['nome']}': {response.text}")

# Função para adicionar um amigo
def adicionar_amigo(usuario_id, amigo_id):
    response = requests.post(f"{url}{usuario_id}/amigos/{amigo_id}", headers=headers)
    if response.status_code == 201:
        print(f"Usuário {usuario_id} e usuário {amigo_id} agora são amigos.")
    else:
        print(f"Erro ao adicionar amigo: {response.text}")

# Adicionar amigos em cadeia
for i in range(len(ids_usuarios) - 1):
    adicionar_amigo(ids_usuarios[i], ids_usuarios[i+1])