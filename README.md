# Product CRUD API

Este projeto é uma API de CRUD (Create, Read, Update, Delete) para gerenciamento de produtos. A API foi desenvolvida utilizando **FastAPI**, **SQLAlchemy**, e **MongoDB** para armazenar logs de visualização de produtos.

## Tecnologias Utilizadas

- **FastAPI**: Framework para desenvolvimento de APIs rápidas e eficientes.
- **SQLAlchemy**: ORM para manipulação do banco de dados relacional (SQLite).
- **Alembic**: Ferramenta para migração de banco de dados em SQLAlchemy.
- **MongoDB**: Banco de dados NoSQL utilizado para armazenar logs de visualização de produtos.
- **Docker**: Utilizado para criar containers para a aplicação e banco de dados.
- **Docker Compose**: Ferramenta para definir e gerenciar múltiplos containers Docker.
- **Pydantic**: Biblioteca de validação de dados utilizada para validar os dados de entrada na API.

## Pré-requisitos

- **Docker**: Para rodar os containers.
- **Docker Compose**: Para gerenciar múltiplos containers.
- **MongoDB**: Instância do MongoDB para armazenar logs de visualizações.

## Estrutura do Projeto

products-crud-api
├── README.md                                     # Descrição do projeto
├── alembic                                       # Diretório para migrações de banco de dados
│   ├── README                                    # Informações sobre o uso do Alembic
│   ├── env.py                                    # Configurações de conexão com a base de dados
│   ├── script.py.mako                            # Template para geração de scripts de migração
│   └── versions                                  # Arquivos de migração gerados pelo Alembic
│       └── <initial_migration>.py                # Migração gerada pelo Alembic
├── alembic.ini                                   # Configuração principal do Alembic
├── app                                           # Diretório principal da aplicação
│   ├── api                                       # Endpoints da API
│   │   └── v1                                    # Versão 1 dos endpoints
            └── routes.py                         # Define as rotas        
│   ├── controllers                               # Lógica de controle para requisições da API
│   │   └── controllers.py                        # Gerencia requisições de produtos
│   ├── core                                      # Configurações principais e utilitários
│   ├── db                                        # Configuração do banco de dados
│   │   ├── __init__.py                           # Inicialização do pacote do banco de dados
│   │   ├── database.py                           # Configura conexão com o banco de dados
│   │   └── models.py                             # Definição das tabelas e modelos do banco
│   ├── main.py                                   # Inicia a aplicação FastAPI
│   └── schemas                                   # Schemas (definições de dados) da API
│       └── schemas.py                            # Definições para validação de dados
├── docker-compose.yml                            # Configuração dos containers Docker
├── dockerfile                                    # Construção do container Docker para a aplicação
├── docs                                          # Documentação adicional do projeto
│   └── CRUD Produtos.postman_collection.json     # Coleção do Postman para testes
├── requirements.txt                              # Dependências do projeto (FastAPI, SQLAlchemy, etc.)
├── tests                                         # Diretório com os testes da aplicação
│   ├── __init__.py                               # Inicialização do pacote de testes
│   └── test_controllers.py                       # Testes para os controllers da API
└── venv                                          # Ambiente virtual Python


## Configuração do Projeto

### Acesso ao Postman
O arquivo para realizar o CRUD via Postman com os exemplos pré-definidos está no diretório "docs".

### Clonando o Repositório, Rodando os Containers e os Testes Unitários.

Primeiro, clone este repositório para o seu ambiente local:

```bash
git clone https://github.com/mrodriguesoliv/products-crud-api.git
cd products-crud-api
```

Depois disso, rode os containers e os testes unitários:

```bash
docker-compose up -d --build
docker exec -it products_crud_api_app pytest
```

Com isso, realize o CRUD via Postman.
