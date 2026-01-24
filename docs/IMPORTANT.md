AI API Key:

You can set your AI API Key with /apikey command in the chat box. Currently supported OpenAI and Gemini only


----------------------


Supabase:

A) Connect to Supabase (recommended)1) Clone the repo
powershell


git clone https://github.com/JalaluddinB/Luxuryshoppingwebsite.git
cd Luxuryshoppingwebsite2) Create + activate a virtual environment
powershell


python -m venv .venv
.\.venv\Scripts\Activate.ps1If activation is blocked:
powershell



Set-ExecutionPolicy -Scope CurrentUser RemoteSigned3) Install dependencies
powershell



pip install -r requirements.txt4) Create .env (this is required now)In the project root, copy the template:• Copy .env.example → .envThen edit .env and set the real Supabase connection string:Password: Funnyjokes123!
env


DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@db.mtzobrvigigsndlzmwdh.supabase.co:5432/postgres?sslmode=requireNotes:.env is not committed to GitHub (it’s gitignored).Use a safe way to share the password (don’t paste in public chat).5) Run the website
powershell



python app.pyOpen:http://localhost:50006) (Optional) Confirm it’s really connected to Supabase
powershell



python -c "import app; from sqlalchemy import text; app.app.app_context().push(); print(app.db.session.execute(text('select 1')).scalar())"Expected output:1B) If they only want to view the site using SQLite (fallback)If they don’t have Supabase credentials yet, they can run with SQLite by setting:
powershell


$env:ALLOW_SQLITE="1"
python app.pyThen open:http://localhost:5000(Without DATABASE_URL, the app will otherwise error out—this is intentional.)StatusThese are the exact steps your teammates need to run locally to view the website with Supabase (or SQLite fallback).