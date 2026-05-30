# Azure Smart Notifier

A Python-based system that accepts messages via a REST API, routes them through Azure Service Bus, processes them with an Azure Function, and logs results to SQL Server.

## Architecture

Client → REST API (FastAPI) → Azure Service Bus → Azure Function → SQL Server

## Project Structure

```
azure-smart-notifier/
├── api/                  # FastAPI REST app (POST /notify)
├── function_app/         # Azure Function (Service Bus trigger)
├── db/                   # SQL schema
├── tests/                # Pytest unit tests
├── azure-pipelines.yml   # CI/CD pipeline
└── .env.example          # Environment variable template
```
## Technologies Used

- Python 3.10+ with FastAPI
- Azure Service Bus — message queue
- Azure Functions — serverless message processor
- Azure SQL Server — persistent logging
- Azure DevOps — CI/CD pipeline
- SonarQube — code quality scanning

## Setup

1. Clone the repo
2. Copy .env.example to .env and fill in your Azure credentials
3. Create a virtual environment: python -m venv venv
4. Activate it: venv\Scripts\activate
5. Install dependencies: pip install -r api/requirements.txt
6. Run locally: uvicorn api.main:app --reload

## Steps Built

- [x] Step 1 — Git repo + project scaffold
- [ ] Step 2 — Python REST API (FastAPI)
- [ ] Step 3 — Azure Service Bus integration
- [ ] Step 4 — Azure Function (Service Bus trigger)
- [ ] Step 5 — SQL Server logging
- [ ] Step 6 — Azure DevOps CI pipeline


