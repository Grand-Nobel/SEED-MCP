from fastapi import FastAPI
from supabase import create_client
from supabase import router as supabase_router

app = FastAPI()

# Tool discovery route
@app.get("/")
def list_tools():
    return [
        {
            "name": "ask-mcp",
            "description": "Send request to Supabase",
            "method": "POST",
            "path": "/functions/v1/ask-mcp"
        }
    ]

app.include_router(supabase_router)
