# Supabase Stack Interaction Tools
from supabase import create_client
from typing import Dict, Any, List, Optional, Union
import json # For parsing filters_json
import os
from fastapi import APIRouter
from supabase.client import Client

router = APIRouter()
@router.get("/status")
async def supabase_status():
    try:
        response = db_client.table("tenant_themes").select("*").limit(1).execute()
        return {"status": "Supabase module connected", "ping": bool(response.data)}
    except Exception as e:
        return {"status": "Supabase module error", "error": str(e)}

# Placeholder for a more specific Pydantic model if we define one for Theme
TenantTheme = Dict[str, Any]

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise RuntimeError("Missing Supabase credentials in environment variables.")

db_client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_tenant_theme(tenant_id: str) -> TenantTheme | None:
    """
    Fetches theme data (colors, typography) for a given tenant from the 'tenant_themes' table.
    Assumes 'tenant_themes' table has 'tenant_id' as primary key and theme-related columns.
    """
    try:
        response = db_client.table("tenant_themes").select("*").eq("tenant_id", tenant_id).single().execute()
        if response.data:
            return response.data
        return None
    except Exception as e:
        # Log error (e.g., print or use a proper logger)
        print(f"Error fetching theme for tenant {tenant_id}: {e}")
        # In a real scenario, you might raise a custom exception or return a specific error object
        return None

def log_ui_event(tenant_id: str, event_type: str, payload: Dict[str, Any]) -> str | None:
    
    """
    Logs UI events to the 'ui_events' table in Supabase.
    Assumes 'ui_events' table has columns: tenant_id, event_type, payload, and an auto-generated id.
    Returns the id of the newly created event log, or None if an error occurs.
    """
    try:
        event_data = {
            "tenant_id": tenant_id,
            "event_type": event_type,
            "payload": payload
        }
        response = db_client.table("ui_events").insert(event_data).execute()
        if response.data and len(response.data) > 0:
            # Assuming the response.data contains a list of inserted records,
            # and each record has an 'id' field.
            return response.data[0].get("id")
        return None
    except Exception as e:
        print(f"Error logging UI event for tenant {tenant_id}, event type {event_type}: {e}")
        return None
def get_tenant_validation_rules(db_client: Client, tenant_id: str) -> Dict[str, Any] | None:
    """
    Fetches form validation rules for a given tenant.
    Assumes a 'tenant_validation_rules' table with 'tenant_id' and a 'rules' JSONB column.
    """
    try:
        response = db_client.table("tenant_validation_rules").select("rules").eq("tenant_id", tenant_id).single().execute()
        if response.data and "rules" in response.data:
            return response.data["rules"]
        return None
    except Exception as e:
        print(f"Error fetching validation rules for tenant {tenant_id}: {e}")
        return None

def get_tenant_table_config(db_client: Client, tenant_id: str) -> Dict[str, Any] | None:
    """
    Fetches table column configurations for a given tenant.
    Assumes a 'tenant_configurations' table with 'tenant_id' and a 'table_configs' JSONB column,
    where 'table_configs' holds all table configurations for that tenant.
    """
    try:
        response = db_client.table("tenant_configurations").select("table_configs").eq("tenant_id", tenant_id).single().execute()
        if response.data and "table_configs" in response.data:
            return response.data["table_configs"]
        return None
    except Exception as e:
        print(f"Error fetching table configurations for tenant {tenant_id}: {e}")
        return None

def get_tenant_accessibility_config(db_client: Client, tenant_id: str) -> Dict[str, Any] | None:
    """
    Fetches accessibility configurations for a given tenant.
    Assumes a 'tenant_accessibility_configs' table with 'tenant_id' and a 'config' JSONB column.
    """
    try:
        response = db_client.table("tenant_accessibility_configs").select("config").eq("tenant_id", tenant_id).single().execute()
        if response.data and "config" in response.data:
            return response.data["config"]
        return None
    except Exception as e:
        print(f"Error fetching accessibility configurations for tenant {tenant_id}: {e}")
        return None

def get_tenant_icon_set_config(db_client: Client, tenant_id: str) -> Dict[str, Any] | None:
    """
    Fetches tenant-specific icon sets configuration if managed via Supabase.
    Assumes a 'tenant_configurations' table with 'tenant_id' and an 'icon_set_config' JSONB column.
    """
    try:
        response = db_client.table("tenant_configurations").select("icon_set_config").eq("tenant_id", tenant_id).single().execute()
        if response.data and "icon_set_config" in response.data:
            return response.data["icon_set_config"]
        return None
    except Exception as e:
        print(f"Error fetching icon set configuration for tenant {tenant_id}: {e}")
        return None


def get_tenant_grid_config(db_client: Client, tenant_id: str) -> Dict[str, Any] | None:
    """
    Fetches tenant-specific grid configurations if managed via Supabase.
    Assumes a 'tenant_configurations' table with 'tenant_id' and a 'grid_config' JSONB column.
    """
    try:
        response = db_client.table("tenant_configurations").select("grid_config").eq("tenant_id", tenant_id).single().execute()
        if response.data and "grid_config" in response.data:
            return response.data["grid_config"]
        return None
    except Exception as e:
        print(f"Error fetching grid configuration for tenant {tenant_id}: {e}")
        return None

def log_system_event(db_client: Client, tenant_id: Optional[str], event_type: str, payload: Dict[str, Any]) -> str | None:
    """
    Logs infrastructure-related events to the 'system_logs' table in Supabase.
    Returns the id of the newly created event log, or None if an error occurs.
    """
    try:
        event_data = {
            "event_type": event_type,
            "payload": payload
        }
        if tenant_id: 
            event_data["tenant_id"] = tenant_id
            
        response = db_client.table("system_logs").insert(event_data).execute()
        if response.data and len(response.data) > 0:
            return response.data[0].get("id")
        return None
    except Exception as e:
        print(f"Error logging system event (type: {event_type}): {e}")
        return None

def log_system_metric(db_client: Client, tenant_id: Optional[str], metric_name: str, value_payload: Dict[str, Any]) -> str | None:
    """
    Logs infrastructure-related metrics to the 'system_metrics' table in Supabase.
    Returns the id of the newly created metric log, or None if an error occurs.
    """
    try:
        metric_data = {
            "metric_name": metric_name,
            "value_payload": value_payload
        }
        if tenant_id:
            metric_data["tenant_id"] = tenant_id
            
        response = db_client.table("system_metrics").insert(metric_data).execute()
        if response.data and len(response.data) > 0:
            return response.data[0].get("id")
        return None
    except Exception as e:
        print(f"Error logging system metric (name: {metric_name}): {e}")
        return None

def get_tenant_service_config(db_client: Client, tenant_id: str) -> Dict[str, Any] | None:
    """
    Fetches configuration for stateless services for a given tenant.
    Assumes a 'tenant_service_configs' table with 'tenant_id' and a 'service_configs' JSONB column.
    """
    try:
        response = db_client.table("tenant_service_configs").select("service_configs").eq("tenant_id", tenant_id).single().execute()
        if response.data and "service_configs" in response.data:
            return response.data["service_configs"]
        return None
    except Exception as e:
        print(f"Error fetching service configurations for tenant {tenant_id}: {e}")
        return None

def manage_supabase_user(db_client: Client, action: str, user_details: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Manages Supabase users, primarily interacting with a 'users' (public.users) table.
    'action' can be "create_profile", "get_profile_by_auth_id", "update_profile".
    'user_details' should contain necessary fields like 'auth_id', 'email', etc.
    """
    users_table = "users" 
    try:
        if action == "create_profile":
            if "auth_id" not in user_details:
                print("Error: auth_id is required to create a user profile.")
                return {"error": "auth_id_required"}
            response = db_client.table(users_table).insert(user_details).execute()
            return response.data[0] if response.data else None
        
        elif action == "get_profile_by_auth_id":
            auth_id = user_details.get("auth_id")
            if not auth_id:
                print("Error: auth_id is required to get a user profile.")
                return {"error": "auth_id_required_for_get"}
            response = db_client.table(users_table).select("*").eq("auth_id", auth_id).maybe_single().execute()
            return response.data
            
        elif action == "update_profile":
            auth_id = user_details.get("auth_id")
            if not auth_id:
                print("Error: auth_id is required to update a user profile.")
                return {"error": "auth_id_required_for_update"}
            
            update_data = {k: v for k, v in user_details.items() if k != "auth_id"}
            if not update_data:
                print("Error: No data provided for update.")
                return {"error": "no_update_data"}

            response = db_client.table(users_table).update(update_data).eq("auth_id", auth_id).execute()
            return response.data[0] if response.data else None

        else:
            print(f"Error: Unknown action '{action}' for manage_supabase_user.")
            return {"error": f"unknown_action: {action}"}

    except Exception as e:
        print(f"Error during manage_supabase_user (action: {action}): {e}")
        return {"error": str(e)}

def get_file_storage_url(db_client: Client, action: str, bucket_name: str, file_path: str, expires_in: int = 3600, content_type: Optional[str] = None) -> Dict[str, Any] | None:
    """
    Gets a presigned URL for file storage (primarily download).
    'action' can be "download". Upload URL generation is complex and better handled by Edge Functions.
    'bucket_name' is the target Supabase storage bucket.
    'file_path' is the path to the file within the bucket.
    'expires_in' is the URL validity in seconds.
    """
    try:
        storage_client = db_client.storage.from_(bucket_name)
        if action == "download":
            response_data = storage_client.create_signed_url(file_path, expires_in)
            signed_url = response_data.get("signedURL") 
            if signed_url:
                 return {"signed_url": signed_url, "method": "GET", "path": file_path}
            else: 
                 error_message = response_data.get("error", "Failed to generate signed URL.")
                 print(f"Error from Supabase create_signed_url: {error_message}")
                 return {"error": error_message}

        elif action == "upload":
            print(f"Warning: 'upload' action for get_file_storage_url is not directly supported for client-side usage due to complexity. Consider an Edge Function.")
            return {"error": "Direct signed URL for 'upload' is not supported by this tool. Use an Edge Function or server-side upload."}
        else:
            return {"error": f"Unknown action: {action}. Supported actions are 'download'."}
            
    except Exception as e:
        print(f"Error generating file storage URL (action: {action}, bucket: {bucket_name}, path: {file_path}): {e}")
        return {"error": str(e)}


def delete_file_from_supabase_storage(db_client: Client, bucket_name: str, storage_paths: List[str]) -> Dict[str, Any]:
    """
    Deletes one or more files from Supabase Storage.
    Returns a dictionary with 'deleted_paths' and 'errors'.
    """
    try:
        storage_client = db_client.storage.from_(bucket_name)
        response = storage_client.remove(storage_paths) 
        
        deleted_successfully = []
        errors_occurred = []

        if isinstance(response, list): 
            for item in response:
                if isinstance(item, dict):
                    if item.get("error"):
                        errors_occurred.append({"path": item.get("name", "unknown_path"), "error": item.get("error")})
                    else:
                        deleted_successfully.append(item.get("name", "unknown_path"))
                else: 
                    errors_occurred.append({"path": "unknown_path", "error": "Unexpected item format in response from storage.remove"})
            return {"deleted_paths": deleted_successfully, "errors": errors_occurred}
        else: 
            print(f"Unexpected response format from storage.remove: {response}")
            return {"deleted_paths": [], "errors": [{"path": "all_paths", "error": "Unexpected response format from storage operation"}]}

    except Exception as e:
        print(f"Error deleting files from storage (bucket: {bucket_name}, paths: {storage_paths}): {e}")
        return {"deleted_paths": [], "errors": [{"path": str(storage_paths), "error": str(e)}]}


def invoke_edge_function(db_client: Client, function_name: str, payload: Dict[str, Any]) -> Any | None:
    """
    Invokes a Supabase Edge Function.
    Returns the data from the edge function response or None on error.
    """
    try:
        response = db_client.functions.invoke(function_name, invoke_options={'body': payload})
        return response 
    except Exception as e: 
        print(f"Error invoking edge function '{function_name}': {e}")
        return None


def manage_user_mfa_status(db_client: Client, user_id: str, action: str, factor_id: Optional[str] = None, challenge_id: Optional[str] = None, code: Optional[str] = None) -> Dict[str, Any]:
    """
    Manages a user's MFA status in Supabase Auth.
    Actions: "list_factors", "enroll_factor", "challenge_factor", "verify_challenge", "unenroll_factor".
    This is a conceptual implementation. Actual Supabase MFA calls might differ.
    """
    try:
        if action == "list_factors":
            print(f"Conceptual: Listing MFA factors for user {user_id}")
            return {"status": "conceptual", "message": "Listing MFA factors is conceptual.", "data": []}
        elif action == "unenroll_factor":
            if not factor_id:
                return {"status": "error", "message": "factor_id is required for unenroll_factor."}
            print(f"Conceptual: Unenrolling MFA factor {factor_id} for user {user_id}")
            return {"status": "conceptual", "message": f"Factor '{factor_id}' unenrollment conceptual."}
        else:
            return {"status": "error", "message": f"Unsupported or conceptual MFA action: {action}"}
    except Exception as e:
        print(f"Error managing MFA for user {user_id}, action {action}: {e}")
        return {"status": "error", "message": str(e)}


def revoke_supabase_user_session(db_client: Client, user_id: str, scope: str = "all") -> Dict[str, Any]:
    """
    Revokes a Supabase user session(s).
    'scope' can be "all". Specific session ID revocation is not directly supported by admin.sign_out.
    """
    try:
        if scope == "all":
            print(f"Conceptual: Revoking all sessions for user {user_id}. Actual implementation depends on supabase-py capabilities.")
            return {"status": "success", "message": f"All sessions for user {user_id} conceptually revoked."}
        else:
            return {"status": "error", "message": f"Unsupported scope '{scope}'. Only 'all' is conceptually supported."}
    except Exception as e:
        print(f"Error revoking sessions for user {user_id}: {e}")
        return {"status": "error", "message": str(e)}


def get_app_secret(db_client: Optional[Client], secret_name: str) -> Dict[str, Any] | None: 
    """
    Gets an application secret (If using Supabase Vault or a similar mechanism).
    This is a conceptual implementation.
    """
    print(f"Conceptual: Getting app secret '{secret_name}'. Implementation depends on Supabase Vault specifics.")
    if secret_name == "EXAMPLE_API_KEY":
        return {"secret_name": secret_name, "value": "dummy_secret_value_for_example"}
    return {"error": f"Secret '{secret_name}' not found or Vault not configured."}


def set_app_secret(db_client: Optional[Client], secret_name: str, secret_value: str) -> Dict[str, Any]:
    """
    Sets an application secret (If using Supabase Vault or a similar mechanism).
    This is a conceptual implementation.
    """
    print(f"Conceptual: Setting app secret '{secret_name}'. Implementation depends on Supabase Vault specifics.")
    return {"status": "conceptual", "message": f"Secret '{secret_name}' conceptually set."}


def get_translations(db_client: Client, locale: str, namespace: str) -> Dict[str, str] | None:
    """
    Fetches translations for a given locale and namespace from the 'translations' table.
    Assumes 'translations' table has columns: locale, namespace, key, value.
    Returns a dictionary of key-value pairs.
    """
    try:
        response = db_client.table("translations").select("key, value").eq("locale", locale).eq("namespace", namespace).execute()
        if response.data:
            return {item["key"]: item["value"] for item in response.data}
        return {} 
    except Exception as e:
        print(f"Error fetching translations for locale '{locale}', namespace '{namespace}': {e}")
        return None


def rpc_call(db_client: Client, function_name: str, params_dict: Optional[Dict[str, Any]] = None) -> Any | None:
    """
    Performs a generic Supabase RPC call.
    Returns the data from the RPC response or None on error.
    """
    try:
        if params_dict is None:
            params_dict = {}
        response = db_client.rpc(function_name, params=params_dict).execute()
        return response.data
    except Exception as e:
        print(f"Error calling RPC function '{function_name}' with params {params_dict}: {e}")
        return None


def get_cron_job_run_details(db_client: Client, limit: int = 10, job_name_filter: Optional[str] = None, status_filter: Optional[str] = None) -> List[Dict[str, Any]] | None:
    """
    Fetches details from cron.job_run_details.
    """
    try:
        query = db_client.from_("job_run_details", schema="cron").select("*").order("end_time", desc=True).limit(limit)
        if job_name_filter:
            query = query.ilike("job_name", f"%{job_name_filter}%")
        if status_filter:
            query = query.eq("status", status_filter)
        
        response = query.execute()
        return response.data
    except Exception as e:
        print(f"Error fetching cron job run details: {e}")
        return None


def invoke_supabase_function(db_client: Client, function_name: str, body_payload: Dict[str, Any], headers_dict: Optional[Dict[str, str]] = None) -> Any | None:
    """
    Invokes a Supabase function (e.g., Edge Function) with optional headers.
    Returns the data from the function response or None on error.
    """
    try:
        invoke_options = {'body': body_payload}
        if headers_dict:
            invoke_options['headers'] = headers_dict
        
        response = db_client.functions.invoke(function_name, invoke_options=invoke_options)
        return response
    except Exception as e:
        print(f"Error invoking Supabase function '{function_name}': {e}")
        return None


def get_table_data(db_client: Client, table_name: str, filters_list: Optional[List[Dict[str, Any]]] = None, select_columns: str = '*', order_by: Optional[str] = None, order_desc: bool = False, limit: Optional[int] = None, single: bool = False) -> Any | None:
    """
    Generic tool to fetch data from a Supabase table with dynamic filtering.
    filters_list: A list of filter dictionaries, e.g., [{"column": "id", "operator": "eq", "value": 1}, {"column": "name", "operator": "like", "value": "%test%"}]
    Supported operators: "eq", "neq", "gt", "gte", "lt", "lte", "like", "ilike", "is", "in", "cs", "cd".
    If 'single' is True, expects a single row and uses .maybe_single().
    """
    try:
        query = db_client.table(table_name).select(select_columns)
        
        if filters_list:
            for f_item in filters_list: 
                col, op, val = f_item.get("column"), f_item.get("operator"), f_item.get("value")
                if not all([col, op]): continue 

                if op == "eq": query = query.eq(col, val)
                elif op == "neq": query = query.neq(col, val)
                elif op == "gt": query = query.gt(col, val)
                elif op == "gte": query = query.gte(col, val)
                elif op == "lt": query = query.lt(col, val)
                elif op == "lte": query = query.lte(col, val)
                elif op == "like": query = query.like(col, val)
                elif op == "ilike": query = query.ilike(col, val)
                elif op == "is": query = query.is_(col, val) 
                elif op == "in": query = query.in_(col, val) 
                elif op == "cs": query = query.contains(col, val) 
                elif op == "cd": query = query.contained_by(col, val) 
        if order_by:
            query = query.order(order_by, desc=order_desc)
        if limit:
            query = query.limit(limit)
        
        if single:
            response = query.maybe_single().execute()
        else:
            response = query.execute()
            
        return response.data
    except Exception as e:
        print(f"Error fetching data from table '{table_name}': {e}")
        return None


def insert_table_data(db_client: Client, table_name: str, data_to_insert: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List[Dict[str, Any]] | None:
    """
    Generic tool to insert one or more rows into a Supabase table.
    data_to_insert: A single dictionary for one row, or a list of dictionaries for multiple rows.
    Returns the list of inserted records (data part of Supabase response) or None on error.
    """
    try:
        response = db_client.table(table_name).insert(data_to_insert).execute()
        return response.data
    except Exception as e:
        print(f"Error inserting data into table '{table_name}': {e}")
        return None


def update_table_data(db_client: Client, table_name: str, data_to_update: Dict[str, Any], filters_list: List[Dict[str, Any]]) -> List[Dict[str, Any]] | None:
    """
    Generic tool to update data in a Supabase table with dynamic filtering.
    data_to_update: Dictionary of columns and new values.
    filters_list: A list of filter dictionaries to specify which rows to update. Must not be empty.
    Returns the list of updated records or None on error.
    """
    if not filters_list:
        print(f"Error: filters_list cannot be empty for update operation on table '{table_name}'. This would update all rows.")
        return None # Or raise ValueError
    try:
        query = db_client.table(table_name).update(data_to_update)
        
        for f_item in filters_list:
            col, op, val = f_item.get("column"), f_item.get("operator"), f_item.get("value")
            if not all([col, op]): continue

            if op == "eq": query = query.eq(col, val)
            elif op == "neq": query = query.neq(col, val)
            elif op == "gt": query = query.gt(col, val)
            elif op == "gte": query = query.gte(col, val)
            elif op == "lt": query = query.lt(col, val)
            elif op == "lte": query = query.lte(col, val)
            elif op == "like": query = query.like(col, val) 
            elif op == "ilike": query = query.ilike(col, val) 
            elif op == "is": query = query.is_(col, val)
            elif op == "in": query = query.in_(col, val)
            # Add other filter operators as needed
            
        response = query.execute()
        return response.data
    except Exception as e:
        print(f"Error updating data in table '{table_name}': {e}")
        return None

    
def delete_table_data(db_client: Client, table_name: str, filters_list: List[Dict[str, Any]]) -> List[Dict[str, Any]] | None:
    """
    Generic tool to delete data from a Supabase table with dynamic filtering.
    filters_list: A list of filter dictionaries to specify which rows to delete. Must not be empty.
    Returns the list of deleted records or None on error.
    """
    # pass # Original content
    if not filters_list:
        print(f"Error: filters_list cannot be empty for delete operation on table '{table_name}'. This would delete all rows.")
        return None # Or raise ValueError
    try:
        query = db_client.table(table_name).delete()
        
        for f_item in filters_list:
            col, op, val = f_item.get("column"), f_item.get("operator"), f_item.get("value")
            if not all([col, op]): continue

            if op == "eq": query = query.eq(col, val)
            elif op == "neq": query = query.neq(col, val)
            elif op == "gt": query = query.gt(col, val)
            elif op == "gte": query = query.gte(col, val)
            elif op == "lt": query = query.lt(col, val)
            elif op == "lte": query = query.lte(col, val)
            elif op == "like": query = query.like(col, val)
            elif op == "ilike": query = query.ilike(col, val)
            elif op == "is": query = query.is_(col, val)
            elif op == "in": query = query.in_(col, val)
            # Add other filter operators as needed

        response = query.execute()
        return response.data
    except Exception as e:
        print(f"Error deleting data from table '{table_name}': {e}")
        return None
 
