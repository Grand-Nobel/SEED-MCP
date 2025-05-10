# Initial comment
from fastapi import FastAPI
import uvicorn

# Assuming seed_supabase.py is in the same directory (root of the project)
# and contains a router instance named 'router'
from tools.supabase.supabase_tools import router as supabase_router

# If you have other tool servers, you would import their routers as well
# For example:
# import seed_ai_agents
# import seed_file_storage

app = FastAPI(
    title="SEED-MCP Aggregated Server",
    description="Development server aggregating various MCP tool servers.",
    version="0.1.0"
)

# Include the Supabase router
# All routes from seed_supabase.py will be prefixed with /supabase
app.include_router(supabase_router, prefix="/supabase", tags=["Supabase Tools"])

# Include other routers here as they are developed:
# app.include_router(seed_ai_agents.router, prefix="/ai", tags=["AI Agent Tools"])
# app.include_router(seed_file_storage.router, prefix="/storage-tools", tags=["File Storage Tools"])
# ... and so on for other tool categories from task-master

@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "SEED-MCP Aggregated Server is running.",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "available_tool_groups": {
            "supabase_tools": "/supabase/docs"
            # Add other tool groups here as they are included
        }
    }

if __name__ == "__main__":
    # This is for local development running this main.py directly
    # For deployment (e.g., with Fly.io), Uvicorn will typically be run by the process manager
    # as configured in fly.toml or a Procfile (which uses Dockerfile CMD).
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=os.getenv("ENV", "") == "dev")
