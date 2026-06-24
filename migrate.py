import json
import os
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

with open("book_data.json", "r") as f:
    book_data = json.load(f)

# Get the book from Supabase
book = supabase.table("books").select("*").eq("title", book_data["title"]).order("created_at").limit(1).execute()
if not book.data:
    print("Book not found in Supabase. Run main.py first.")
    exit()

book_id = book.data[0]["id"]

# Delete any existing chapters for this book
supabase.table("chapters").delete().eq("book_id", book_id).execute()
print("Cleared existing chapters.")

# Insert all chapters from book_data.json
rows = [
    {
        "book_id": book_id,
        "chapter_number": ch["chapter_number"],
        "title": ch["title"],
        "content": ch["content"],
        "summary": ch["summary"],
        "chapter_notes_status": "approved",
        "chapter_notes": ch.get("chapter_notes", "")
    }
    for ch in book_data["chapters"]
]

supabase.table("chapters").insert(rows).execute()
print(f"Migrated {len(rows)} chapters to Supabase successfully.")
