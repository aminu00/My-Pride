MY PRIDE — Chatbot for women's health

This repository contains the MY PRIDE Flask chatbot (local dev). The app uses the OpenRouter API for chat completions.

Quick start (Windows PowerShell):

1. Create a virtual environment and install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set your OpenRouter API key (example)

```powershell
$env:OPENROUTER_API_KEY = "sk-or-v1-..."
```

3. Run the app

```powershell
python app.py
```

Notes:
- Do not commit secrets. Use GitHub Secrets when deploying.
- If you want to deploy this repo to GitHub Actions or other hosts, add the OPENROUTER_API_KEY as a secret.

Repository: https://github.com/aminu00/My-Pride.git
