# FastStack

FastStack is an AI-powered, choose-your-own-adventure storytelling application built with the OpenAI API, featuring a Python backend and a JavaScript frontend. The entire application is containerized using Podman and Docker.

## Installation

### From source

Clone the repository:

```
git clone https://github.com/lapointek/faststack
```

## OpenAI API Key

Add OpenAI API Key to the .env file in backend:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Using podman-compose

```
cd faststack
podman-compose up --build
```

### Using docker-compose

```
cd faststack
docker-compose up --build
```

## Run

### Frontend (Docker)

- http://localhost:5173

### Backend API (Docker)

- http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

## About

This project is based on a tutorial implementation [link](https://www.youtube.com/watch?v=_1P0Uqk50Ps) and has been adapted to run in docker containers.
