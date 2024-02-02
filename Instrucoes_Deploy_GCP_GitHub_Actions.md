
# Instruções para Deploy no Google Cloud Platform (GCP) com GitHub Actions

Este guia explica como configurar um projeto no Google Cloud Platform (GCP) e definir variáveis de ambiente no repositório GitHub para o deploy automático usando GitHub Actions.

## Configuração no Google Cloud Platform

### Criar ou Selecionar um Projeto no GCP
1. Faça login no [Google Cloud Console](https://console.cloud.google.com/).
2. Selecione ou crie um novo projeto para hospedar sua aplicação.

### Configurar o Cloud Run
1. No console do GCP, vá para o "Cloud Run".
2. Ative o serviço, se necessário.
3. Anote o ID do seu projeto.

### Criar uma Service Account
1. Vá para "IAM & Admin" > "Service Accounts".
2. Crie uma nova service account com as permissões necessárias para fazer o deploy no Cloud Run.
3. Crie e baixe uma chave privada para esta conta (formato JSON).

### Configurar o Container Registry
1. Ative o Container Registry no seu projeto.
2. Você precisará enviar a imagem do seu container para o GCR para usá-la no Cloud Run.

## Configuração das Variáveis no Repositório GitHub

### Adicionar Secret Keys ao Repositório GitHub
1. Vá ao seu repositório no GitHub.
2. Clique em "Settings" > "Secrets" > "New repository secret".
3. Adicione as seguintes secrets:
   - `GCP_PROJECT_ID`: O ID do seu projeto no GCP.
   - `GCP_SA_KEY`: O conteúdo do arquivo JSON da chave privada da sua service account.

### Configurar o Workflow de CI/CD
1. No seu arquivo `deploy.yml`, certifique-se de que o nome do serviço e a região estão corretos.
2. O passo "Deploy to GCP" usará as variáveis configuradas para autenticar no GCP e fazer o deploy.

## Teste e Verificação
- Faça um push para a branch `main` e veja se o workflow do GitHub Actions executa com sucesso.
- Verifique no Cloud Run se o serviço foi implantado corretamente.
- Teste o endpoint para garantir que a API está funcionando.

## Notas Finais
- Revise as permissões da sua Service Account.
- Mantenha suas chaves privadas seguras.
- Considere usar estratégias adicionais de CI/CD, como rodar testes automatizados antes do deploy.
