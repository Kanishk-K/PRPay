import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase client instance
supabase_client: Client | None = None


def get_supabase_client() -> Client:
    """
    Get or create Supabase client instance.

    Returns:
        Client: Supabase client for database operations

    Raises:
        ValueError: If Supabase credentials are not configured
    """
    global supabase_client

    if supabase_client is None:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError(
                "Supabase credentials not found. "
                "Please set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env file"
            )

        supabase_client = create_client(supabase_url, supabase_key)

    return supabase_client


def get_db() -> Client:
    """Dependency for FastAPI endpoints to get database client"""
    return get_supabase_client()
