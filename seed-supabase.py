# supabase.py
from fastapi import APIRouter, HTTPException, Request
from supabase import create_client, Client
import os

router = APIRouter()

SUPABASE_URL = os.getenv("access token")
SUPABASE_API_KEY = os.getenv("anon_key")

if not SUPABASE_URL or not SUPABASE_API_KEY:
    raise EnvironmentError("Missing Supabase credentials")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

@router.post("/functions/v1/ask-mcp")
async def ask_mcp(request: Request):
    data = await request.json()
    try:
        # Example query: insert into 'logs' table
        result = supabase.table("logs").insert({"payload": data}).execute()
        return {"status": "success", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/v1/select/{table_name}")
async def select_data(table_name: str):
    try:
        result = supabase.table(table_name).select("*").execute()
        return {"status": "success", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/data/v1/insert/{table_name}")
async def insert_data(table_name: str, request: Request):
    data = await request.json()
    try:
        result = supabase.table(table_name).insert(data).execute()
        return {"status": "success", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/data/v1/update/{table_name}/{id}")
async def update_data(table_name: str, id: str, request: Request):
    data = await request.json()
    try:
        result = supabase.table(table_name).update(data).eq("id", id).execute()
        return {"status": "success", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/data/v1/delete/{table_name}/{id}")
async def delete_data(table_name: str, id: str):
    try:
        result = supabase.table(table_name).delete().eq("id", id).execute()
        return {"status": "success", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
