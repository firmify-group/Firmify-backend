import os
from ..database.deps import super_client
from ..models.request_models.request_in import RequestSave
from ..service import auth_service
from src.models.response_models.requests_out import adminRequestOut
from fastapi import HTTPException
from datetime import datetime
from typing import List, Optional
from datetime import datetime, timezone
from uuid import uuid4
import pytz
from config import settings

import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from uuid import uuid4

S3_ENDPOINT = settings.S3_ENDPOINT
S3_BUCKET = "solicitudes"
S3_REGION = "sa-east-1"
ACCESS_KEY = settings.ACCESS_KEY
SECRET_KEY = settings.SECRET_KEY

s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    region_name=S3_REGION,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=boto3.session.Config(signature_version="s3v4")
)

def create_request_with_upload(request_file, filename, content_type):
    try:
        unique_filename = f"{uuid4()}_{filename}"
        upload_response = s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=unique_filename,
            Body=request_file,
            ContentType=content_type
        )
        
        print("Upload response:", upload_response)
        if upload_response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception("Error al subir el archivo a S3")

        file_url = f"{S3_ENDPOINT}/{S3_BUCKET}/{unique_filename}"

        return file_url

    except NoCredentialsError:
        print("Error: Las credenciales no son válidas o no están configuradas correctamente.")
    except ClientError as e:
        print(f"Error al crear solicitud con archivo: {e}")
    except Exception as e:
        print(f"Error desconocido: {e}")

    return None


# # Crear solicitud con archivo
# def create_request_with_upload(request_file, filename, content_type):
#     try:
#         # Generar un nombre único para el archivo
#         unique_filename = f"{uuid4()}_{filename}"
#         bucket_name = "solicitudes"

#         # Subir archivo binario directamente
#         upload_response = super_client.storage.from_(bucket_name).upload(
#             unique_filename,
#             request_file,
#             file_options={"content_type": content_type}
#         )
#         print("Upload response:", upload_response)

#         # Verificar si hubo un error al subir el archivo
#         if upload_response["error"]:
#             print("Error al subir el archivo:", upload_response["error"])
#             raise Exception(upload_response["error"]["message"])
#     except Exception as e:
#         print(f"Error al crear solicitud: {e}")
#         return None


# Crear solicitud
def create_request(start_date, end_date, category_id, user_id, public_url):
    try:
        chile_tz = pytz.timezone("Chile/Continental")
        if isinstance(start_date, datetime):
            start_date = start_date.astimezone(chile_tz)

        end_date_str = end_date.astimezone(chile_tz).isoformat() if isinstance(end_date, datetime) else end_date
        sign_date_str = datetime.now(chile_tz).isoformat()
        response = super_client.table("request").insert({
            "start_date": start_date.isoformat() if isinstance(start_date, datetime) else start_date,
            "end_date": end_date_str,
            "file_path": public_url,
            "sign_date": sign_date_str,
            "category_id": category_id,
            "state_id": 1,
            "user_id": user_id,
        }).execute()

        print("Response de inserción:", response)
        return response.data
    except Exception as e:
        print(f"Error al crear solicitud: {e}")
        return None


# Obtener solicitudes dentro de un intervalo de fechas
def get_request_from_date_intervals(from_date: datetime, until_date: datetime):
    try:
        response = (
            super_client
            .table("request")
            .select("start_date")
            .range_gte("start_date", [from_date, until_date])
            .execute()
        )
        return response.data or None
    except Exception as e:
        print(f"Error al obtener solicitudes por fecha: {e}")
        return None


# Obtener solicitudes por ID de usuario
def get_request_by_user_id(user_id):
    try:
        response = (
            super_client
            .table("request")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return response.data or None
    except Exception as e:
        print(f"Error al obtener solicitudes por usuario: {e}")
        return None


# Obtener todas las solicitudes (versión básica)
def get_all_request():
    try:
        response = (
            super_client
            .table("request")
            .select("*")
            .execute()
        )
        return response.data or None
    except Exception as e:
        print(f"Error al obtener todas las solicitudes: {e}")
        return None


# Obtener todas las solicitudes (versión administrador)
async def get_all_requests_admin() -> list[adminRequestOut]:
    try:
        response = (
            super_client
            .from_("request")
            .select("""
                id,
                start_date,
                end_date,
                user: user_id ( rut, email, name ),
                category: category_id (category_name),
                state: state_id (state_name)
            """)
            .execute()
        )

        data = response.data or []
        result = []

        for item in data:
            user = item.get("user") or {}
            category = item.get("category")
            state = item.get("state")

            start_date_raw = item.get("start_date")
            end_date_raw = item.get("end_date")

            start_date = datetime.fromisoformat(start_date_raw).date() if isinstance(start_date_raw, str) else start_date_raw
            end_date = datetime.fromisoformat(end_date_raw).date() if isinstance(end_date_raw, str) else end_date_raw

            result.append(adminRequestOut(
                id=item.get("id"),
                rut=user.get("rut", ""),
                email=user.get("email", ""),
                name=user.get("name", ""),
                category=category.get("category_name") if category else None,
                status=state.get("state_name") if state else None,
                start_date=start_date,
                end_date=end_date
            ))

        return result

    except Exception as e:
        print(f"Error en get_all_requests_admin: {e}")
        return []


# Obtener solicitudes creadas por el usuario actual
def getRequestsByUser(user_id: Optional[str] = None):
    try:
        query = (
            super_client.table("request")
            .select("id, category:category_id(category_name), state:state_id(state_name), start_date:start_date, end_date:end_date")
        )
        if user_id:
            query = query.eq("user_id", user_id)

        response = query.execute()
        return response.data or []

    except Exception as e:
        print(f"Error en getRequestsByUser: {e}")
        return []


# Objetar una solicitud
async def object_request(request_id: int, description: str) -> bool:
    try:
        request_check = (
            super_client.table("request")
            .select("id, state_id")
            .eq("id", request_id)
            .single()
            .execute()
        )

        request_data = request_check.data
        if not request_data or request_data["state_id"] != 5:
            return False

        insert_response = super_client.table("objection").insert({
            "description": description,
            "request_id": request_id,
            "state_id": 2
        }).execute()

        if not insert_response.data:
            return False

        update_response = super_client.table("request").update({
            "state_id": 2
        }).eq("id", request_id).execute()

        return bool(update_response.data)

    except Exception as e:
        print(f"Error en object_request: {e}")
        return False


# Evaluar (cambiar estado de) una solicitud
async def evaluate_request(request_id: int, new_status: str) -> bool:
    try:
        state_response = super_client.table("state").select("id").eq("state_name", new_status.upper()).execute()
        state_data = state_response.data

        if not state_data:
            print(f"Estado no encontrado: {new_status}")
            return False

        new_state_id = state_data[0]["id"]

        update_response = super_client.table("request").update({"state_id": new_state_id}).eq("id", request_id).execute()

        return len(update_response.data) > 0

    except Exception as e:
        print(f"Error en evaluate_request: {e}")
        return False

# Obtener categorías disponibles
def get_categories_from_db() -> List[dict]:
    try:
        response = super_client.table("category").select("*").execute()
        print("Supabase response:", response)
        return response.data or []
    except Exception as e:
        print(f"Error en get_categories_from_db: {e}")
        return []

