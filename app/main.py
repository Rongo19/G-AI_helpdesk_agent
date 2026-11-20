from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.agent.graph import build_agent
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting GoAified HR/IT Helpdesk...")

    # Initialize LangGraph agent once
    app.state.agent = build_agent()

    print("AI Agent initialized successfully!")

    yield

    print("Shutting down GoAified HR/IT Helpdesk...")


app = FastAPI(
    title="GoAified HR/IT Helpdesk",
    description=(
        "AI-powered HR and IT Helpdesk using "
        "RAG, Groq, LangGraph, MCP and PostgreSQL."
    ),
    version="1.0.0",
    lifespan=lifespan
)


# Register API routes
app.include_router(router)


@app.get("/")
async def root():

    return {
        "application": "GoAified HR/IT Helpdesk",
        "message": "Welcome to the AI Helpdesk API",
        "docs": "/docs"
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy",
        "application": "GoAified HR/IT Helpdesk"
    }