import os
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])


def approve_next_chapter(title: str):
    # Get book
    book = supabase.table("books").select("*").eq("title", title).order("created_at").limit(1).execute()
    if not book.data:
        print("Book not found.")
        return

    book_id = book.data[0]["id"]

    # Get next pending chapter with content
    chapters = supabase.table("chapters").select("*").eq("book_id", book_id).eq("chapter_notes_status", "pending").order("chapter_number").limit(1).execute()

    if not chapters.data:
        print("No pending chapters found.")
        return

    chapter = chapters.data[0]
    if not chapter["content"]:
        print(f"Chapter {chapter['chapter_number']} has no content yet. Run main.py first.")
        return

    supabase.table("chapters").update({"chapter_notes_status": "approved"}).eq("id", chapter["id"]).execute()
    print(f"Chapter {chapter['chapter_number']}: '{chapter['title']}' approved.")


if __name__ == "__main__":
    approve_next_chapter("The Art of Deep Focus")
