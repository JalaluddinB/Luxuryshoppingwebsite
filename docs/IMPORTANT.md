AI API Key:

You can set your AI API Key with /apikey command in the chat box. Currently supported OpenAI and Gemini only


----------------------


Database:

A) Connect to Azure SQL Database (recommended)1) Clone the repo
powershell


git clone https://github.com/JalaluddinB/Luxuryshoppingwebsite.git
cd Luxuryshoppingwebsite2) Create + activate a virtual environment
powershell


python -m venv .venv
.\.venv\Scripts\Activate.ps1If activation is blocked:
powershell



Set-ExecutionPolicy -Scope CurrentUser RemoteSigned3) Install dependencies
powershell



pip install -r requirements.txt4) Create .env (this is required now)In the project root, copy the template:• Copy .env.example → .envThen edit .env and set the real Azure SQL Database connection string:
env


DATABASE_URL=mssql+pyodbc://USERNAME:PASSWORD@luxurydatabase.database.windows.net:1433/luxurydb?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=noNotes:.env is not committed to GitHub (it’s gitignored).Use a safe way to share the password (don’t paste in public chat).5) Run the website
powershell



./venv/bin/python3 app.pyOpen:http://localhost:5000) (Optional) Confirm it’s really connected to Azure SQL Database
powershell



./venv/bin/python3 -c "import app; from sqlalchemy import text; app.app.app_context().push(); print(app.db.session.execute(text('select 1')).scalar())"Expected output:1StatusThese are the exact steps your teammates need to run locally to view the website with Azure SQL Database.