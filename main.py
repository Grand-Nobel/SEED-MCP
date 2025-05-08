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
        },
        {
            "name": "select_data",
            "description": "Select data from a Supabase table",
            "method": "GET",
            "path": "/data/v1/select/{table_name}"
        },
        {
            "name": "insert_data",
            "description": "Insert data into a Supabase table",
            "method": "POST",
            "path": "/data/v1/insert/{table_name}"
        },
        {
            "name": "update_data",
            "description": "Update data in a Supabase table by ID",
            "method": "PUT",
            "path": "/data/v1/update/{table_name}/{id}"
        },
        {
            "name": "delete_data",
            "description": "Delete data from a Supabase table by ID",
            "method": "DELETE",
            "path": "/data/v1/delete/{table_name}/{id}"
        }
    ]

app.include_router(supabase_router)
