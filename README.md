# 📚 Automated Book Generator

A Python-based automated book generation system that uses the Groq LLM API to generate full books from a title and notes. It supports chapter-by-chapter generation with human review, exports to TXT, DOCX, and PDF, emails the final book, and includes a FastAPI web UI.

---

## 🚀 Features

- Generate detailed book outlines using Groq LLM
- Auto-parse chapter titles from the outline
- Generate chapters one by one with context from previous summaries
- Human review system (approve / needs_changes) at each step
- Store all data in Supabase (PostgreSQL)
- Export final book to TXT, DOCX, and PDF
- Email the final book via Resend
- FastAPI Web UI with Swagger docs

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Groq API | LLM for content generation |
| Supabase | Database storage |
| FastAPI | Web UI backend |
| Jinja2 | HTML templating |
| python-docx | DOCX export |
| ReportLab | PDF export |
| Resend | Email delivery |

---

## 📁 Project Structure

```
book-generator/
├── app.py              # FastAPI web app
├── main.py             # CLI pipeline (outline + chapters + export)
├── approve.py          # CLI: approve next pending chapter
├── approve_final.py    # CLI: approve final review
├── migrate.py          # Migrate book_data.json to Supabase
├── templates/
│   ├── index.html      # Home page
│   └── book.html       # Book dashboard
├── .env                # Environment variables
├── final_book.txt      # Exported TXT
├── final_book.docx     # Exported DOCX
└── final_book.pdf      # Exported PDF
```

---

## ⚙️ Setup

### 1. Clone the project

```bash
git clone <your-repo-url>
cd book-generator
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install groq supabase python-dotenv python-docx reportlab resend fastapi uvicorn jinja2 python-multipart
```

### 4. Configure environment variables

Create a `.env` file in the root folder:

```
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
RESEND_API_KEY=your_resend_api_key
```

### 5. Set up Supabase tables

Run these in your Supabase SQL Editor:

```sql
CREATE TABLE books (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  title text,
  notes_on_outline_before text,
  outline text,
  status_outline_notes text DEFAULT 'pending',
  final_review_notes_status text DEFAULT 'pending',
  created_at timestamp DEFAULT now()
);

CREATE TABLE chapters (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  book_id uuid REFERENCES books(id) ON DELETE CASCADE,
  chapter_number integer,
  title text,
  content text,
  summary text,
  chapter_notes_status text DEFAULT 'pending',
  chapter_notes text DEFAULT '',
  created_at timestamp DEFAULT now()
);
```

---

## 🖥 Running the Web UI

```bash
python -m uvicorn app:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

- Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ⌨️ Running via CLI

```bash
# Run the main pipeline
python main.py

# Approve next pending chapter
python approve.py

# Approve final review
python approve_final.py

# Migrate book_data.json to Supabase
python migrate.py
```

---

## 🔄 Book Generation Flow

```
1. Enter title + notes
        ↓
2. Generate outline (Groq LLM)
        ↓
3. Review outline → approve
        ↓
4. Parse chapter titles (Groq LLM)
        ↓
5. Generate chapters one by one
   (each uses previous summaries as context)
        ↓
6. Review each chapter → approve / needs_changes
        ↓
7. Compile final book
        ↓
8. Export → TXT + DOCX + PDF
        ↓
9. Email via Resend
```

---

## 📊 Status Fields

### Outline (`status_outline_notes`)
| Value | Meaning |
|---|---|
| `pending` | Waiting for review |
| `approved` | Proceed to chapter generation |
| `needs_changes` | Regenerate with updated notes |

### Chapter (`chapter_notes_status`)
| Value | Meaning |
|---|---|
| `pending` | Waiting for review |
| `approved` | Move to next chapter |
| `needs_changes` | Regenerate using `chapter_notes` field |

---

## 📬 Email

Uses [Resend](https://resend.com) to send the final DOCX as an email attachment. The sender is `onboarding@resend.dev` on the free plan.

---

## 📝 Model

Uses `llama-3.3-70b-versatile` via [Groq](https://console.groq.com).

---

## 🔒 Security

- All API keys stored in `.env` — never hardcoded
- `.env` should be added to `.gitignore`

```
.env
venv/
__pycache__/
*.pyc
final_book.txt
final_book.docx
final_book.pdf
book_data.json
```
