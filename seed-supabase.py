# supabase.py
from fastapi import APIRouter, HTTPException, Request
from supabase import create_client, Client
import os

router = APIRouter()

SUPABASE_URL = os.getenv("https://jcxtocfdzrflfsuufxnr.supabase.co")
SUPABASE_API_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpjeHRvY2ZkenJmbGZzdXVmeG5yIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY1MjczMTIsImV4cCI6MjA2MjEwMzMxMn0.jR-1wEoeuAlMzhTea-BpjoWlx5l_ifzIlgDxMFiS7HA")

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
