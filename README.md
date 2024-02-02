# Aratu - back end

Este é o repositório do backend da aplicação ARATU

## Project Structure

The project has the following structure:

```
my-fastapi-app
├── .github
│   └── workflows
│       └── deploy.yml
├── app
│   ├── main.py
│   ├── api
│   │   └── v1
│   │       └── __init__.py
│   ├── core
│   │   └── config.py
│   ├── db
│   │   └── base.py
│   ├── models
│   │   └── __init__.py
│   └── services
│       └── __init__.py
├── tests
│   └── __init__.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/username/my-fastapi-app.git
```

2. Change into the project directory:

```bash
cd aratu-api
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`.

## Deployment

This project includes a CD pipeline for deployment on GCP. The pipeline is defined in the `.github/workflows/deploy.yml` file. It is triggered on every push to the `main` branch.

To deploy the application, you need to set up the following secrets in your GitHub repository:

- `GCP_PROJECT_ID`: The ID of your GCP project.
- `GCP_SA_KEY`: The JSON key of your GCP service account.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.