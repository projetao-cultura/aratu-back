# Aratu API v0.1

Bem-vindo à Aratu API, o backend da aplicação Aratu, um app de fomento ao turismo local em Recife-Pernambuco. Esta API fornece os serviços e dados necessários para explorar os pontos turísticos, eventos e atrações da região.

## Como Rodar Localmente

### Clonando o Projeto

Para começar, clone o repositório em sua máquina local:

```bash
git clone https://github.com/projetao-cultura/aratu-back.git
cd aratu-api
```

### Rodando Localmente sem Docker

Para rodar a aplicação localmente sem Docker, primeiro navegue até a pasta 'aratu-api', e então execute:

```bash
uvicorn main:app --reload
```

Isso iniciará o servidor de desenvolvimento localmente com recarregamento automático habilitado.

### Rodando com Docker (Recomendado)

O jeito mais fácil de rodar a aplicação é usando o Docker. Se você ainda não tem o Docker Desktop instalado, você pode baixá-lo e instalá-lo a partir do site oficial do Docker.

Após instalar o Docker Desktop, você precisará instalar o docker-compose para orquestrar o container da aplicação. A instalação do Docker Desktop já inclui o docker-compose.

Para iniciar a aplicação usando o Docker, execute o seguinte comando no diretório 'aratu-api' do projeto:

```bash
docker-compose up --build
```

Isso construirá a imagem Docker da aplicação (se necessário) e iniciará todos os serviços definidos no arquivo 'docker-compose.yml'.

## Deploy Automático via GitHub Actions

Este projeto está configurado para fazer deploy automático para o ambiente de produção sempre que mudanças são commitadas na branch main. O processo é gerenciado pelo GitHub Actions, assegurando que a última versão do código esteja sempre disponível.

### Desenvolvendo Novas Features

Para começar a trabalhar em uma nova feature, crie uma branch a partir da main:

```bash
git checkout -b nome-da-sua-branch
```

Após finalizar o desenvolvimento, submeta suas mudanças via Pull Request para a branch main. Após a revisão e aprovação do código, o merge iniciará o processo de deploy automático.
