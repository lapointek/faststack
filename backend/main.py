from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import settings variables
from core.config import settings

app = FastAPI(
    # Documentation
    title="Choose Your Own Adventure Game API",
    description="api to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    # Have API used from a different origin
    # Cross Origin Resource Sharing
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # Run webserver
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
