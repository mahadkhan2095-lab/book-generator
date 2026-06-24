import os
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

book = supabase.table("books").select("*").order("created_at").limit(1).execute()
if not book.data:
    print("Book not found.")
else:
    supabase.table("books").update({"final_review_notes_status": "approved"}).eq("id", book.data[0]["id"]).execute()
    print(f"Final review approved for: {book.data[0]['title']}")
