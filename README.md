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
