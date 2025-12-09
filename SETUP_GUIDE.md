# FlowChat + Periodpal Setup & Run Guide

## What You Just Got

✨ **FlowChat** — a compassionate Flask chatbot for women's menstrual health
📚 **Periodpal Framework** — comprehensive menstrual health knowledge base integrated into the app
🎨 **Styled Responses** — all answers automatically formatted with emojis, tips, and affirmations

---

## Quick Start (Windows PowerShell)

### 1. Activate Virtual Environment
```powershell
cd "C:\Users\HP\Desktop\My Pride"
.\.venv\Scripts\Activate.ps1
```

### 2. Install python-dotenv (Optional but Recommended)
```powershell
pip install python-dotenv
```
This allows the app to load your API key from the `.env` file automatically.

### 3. Add Your OpenRouter API Key to .env

**Option A: Using Notepad**
```powershell
notepad .env
```
Replace `sk-or-REPLACE_ME` with your real OpenRouter API key, then save.

**Option B: Using PowerShell**
```powershell
# Set the content directly
(Get-Content .env) -replace 'sk-or-REPLACE_ME', 'sk-or-YOUR-REAL-KEY-HERE' | Set-Content .env
```

### 4. Run the App
```powershell
python app.py
```

**Expected Output:**
```
Starting FlowChat app...
OpenRouter API key found ✓
Access the app at: http://127.0.0.1:7860
```

### 5. Open in Browser
Visit: **http://127.0.0.1:7860**

---

## What FlowChat Does

✨ Responds to **any question about menstrual health** in the Periodpal format:
- 🩸 Emoji-led responses
- 💡 Clear section headers
- 🧼 2-3 practical, actionable tips
- 💪 Empowering affirmations
- 💕 Warm, validating language

### Example Questions to Ask:
- "What can I do about period cramps?"
- "Why is my period late?"
- "How do I make reusable pads at home?"
- "What's normal for period flow?"
- "How do I track my menstrual cycle?"
- "I'm dealing with PMS mood swings..."
- "Is it safe to exercise during my period?"

---

## Periodpal Framework

The app includes **12 major content areas**:

1. **PAD PROJECT** — DIY reusable pad making
2. **PERIOD DELAY 101** — 11 reasons periods come late
3. **MENSTRUAL STAGES** — Day-by-day guide (Days 1-5)
4. **CYCLE PHASES** — Follicular, ovulation, luteal
5. **50+ AFFIRMATIONS** — Empowerment messages
6. **MYTH vs TRUTH** — Myth debunking
7. **SANITARY PRODUCTS** — Guide to all product types
8. **MENSTRUAL HYGIENE 101** — Safe practices
9. **EMOTIONAL SUPPORT** — Validation & mental health
10. **DIET & LIFESTYLE** — Foods, exercise, sleep
11. **CYCLE TRACKING 101** — Why and how to track
12. **LGBTQ+ INCLUSION** — Respectful, inclusive language

Located in: `resources/periodpal.txt`

---

## File Structure

```
My Pride/
├── app.py                  # Main Flask app with Periodpal integration
├── test_api.py            # Optional API connectivity test
├── requirements.txt       # Python dependencies
├── .env                   # YOUR API KEY (created from .env.example)
├── .env.example           # Template for .env
├── .gitignore             # Prevents .env from being committed
├── README.md              # Project overview
└── resources/
    ├── periodpal.txt      # Complete Periodpal framework content
    └── README.md          # Periodpal documentation
```

---

## Testing the App

### Test 1: Verify Startup
```powershell
python app.py
```
Should show: "OpenRouter API key found ✓"

### Test 2: Test API Connection (Optional)
```powershell
python test_api.py
```
This makes a test call to OpenRouter to verify your API key is valid.

### Test 3: Chat in Browser
1. Open http://127.0.0.1:7860
2. Ask any menstrual health question
3. Response should include:
   - Relevant emoji
   - Clear sections
   - Practical tips
   - Empowering closing

---

## Troubleshooting

### Error: "OpenRouter API key not found"
- Make sure you created `.env` from `.env.example`
- Check that you replaced `sk-or-REPLACE_ME` with your real key
- Verify the `.env` file is in the project root directory

### Error: "User not found" in API response
- Your API key may be invalid or expired
- Create a new key at: https://openrouter.ai/keys
- Update the `.env` file with the new key
- Run `python app.py` again

### App won't start
- Make sure virtual environment is activated: `.\.venv\Scripts\Activate.ps1`
- Check Python is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`

### Port 7860 already in use
- Kill the existing process or edit `app.py` line ~800 to use a different port:
  ```python
  app.run(host='0.0.0.0', port=7861, debug=True)  # Use 7861 instead
  ```

---

## To Stop the App

Press **Ctrl + C** in PowerShell.

---

## Deploying to GitHub (Already Done ✓)

Your changes have been committed and pushed to:
```
https://github.com/aminu00/My-Pride
```

To push any future changes:
```powershell
git add .
git commit -m "Your commit message here"
git push
```

---

## Key Features

✅ **Compassionate** — Validating, non-judgmental responses  
✅ **Comprehensive** — 12 major content areas  
✅ **Styled** — Periodpal format with emojis and structure  
✅ **Practical** — Actionable tips for every situation  
✅ **Empowering** — 50+ affirmations for body confidence  
✅ **Inclusive** — Respectful language for all menstruators  
✅ **Low-Cost** — DIY solutions and community resources  
✅ **Safe** — Disclaimers about medical issues  

---

## Support

If you have questions about:
- **Menstrual health** → Ask FlowChat!
- **App setup** → Check the README.md and this guide
- **API issues** → Check your `.env` file and API key
- **Periodpal framework** → See `resources/README.md`

---

**You're all set! Open http://127.0.0.1:7860 and start chatting. 💕**
