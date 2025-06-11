from supabase import create_client, Client
from config import settings as cf


super_client: Client = create_client(cf.SUPABASE_URL,cf.SUPABASE_KEY)



