"""
MY PRIDE - single-file Flask chatbot app

Run: python app.py

Dependencies:
  pip install flask requests langdetect python-dotenv

Before running, set your OpenRouter API key in an environment variable:
  PowerShell (Windows):
    $env:OPENROUTER_API_KEY = "sk-or-v1-..."
  macOS / Linux:
    export OPENROUTER_API_KEY="sk-or-v1-..."

This app uses the browser Web Speech API for voice input and speechSynthesis for voice output.
Server uses OpenRouter API with DeepSeek model for chat completions.

Do NOT hardcode the key — put it in the environment variable `OPENROUTER_API_KEY`.
"""
from flask import Flask, request, jsonify, render_template_string, session
import os
import requests
import json
import time
from langdetect import detect, LangDetectException

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'change-this-secret-for-prod')

OPENROUTER_API = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_KEY = "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"
MODEL_NAME = "openai/gpt-3.5-turbo"  # Using a reliable, tested model

SYSTEM_PROMPT = (
    "You are MY PRIDE, a caring and supportive digital big sister focused exclusively on women's health and wellness. 💕\n\n"
    "Core Guidelines:\n"
    "1. ONLY respond to questions about:\n"
    "   - Menstrual health and hygiene\n"
    "   - Women's physical and emotional wellness\n"
    "   - Reproductive health education\n"
    "   - Body awareness and self-care\n"
    "   - Gender-specific health concerns\n"
    "   - Community support and stigma topics\n\n"
    "2. For off-topic questions, gently say: 'I'm your sister for women's health questions. Could you ask me something about menstrual health, feminine wellness, or related concerns instead? 💝'\n\n"
    "Style Guide:\n"
    "- Be warm, gentle, and understanding\n"
    "- Use simple, clear language\n"
    "- Keep responses short (3-4 sentences)\n"
    "- Add occasional emojis for warmth (💕 💝 🌸)\n"
    "- Always validate feelings first\n"
    "- Include practical, actionable advice\n\n"
    "Safety Rules:\n"
    "- Never give medical diagnoses\n"
    "- Encourage doctor visits for concerns\n"
    "- Focus on education and support\n"
    "- Maintain privacy and respect\n\n"
    "Remember: You're a supportive sister figure, not a medical professional. Make users feel heard, supported, and empowered while staying within women's health topics."
)

HTML = r'''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MY PRIDE 💕 Talk periods. Track periods. Own your body.</title>
  <style>
    :root {
      --pink: #ff5a86;
      --pink-light: #fff0f4;
      --pink-dark: #d44a6d;
      --gray: #667380;
      --bg: #fffbfc;
      --shadow: rgba(255,90,134,0.1);
    }
    
    body {
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: linear-gradient(165deg, var(--bg) 0%, var(--pink-light) 100%);
      color: #334155;
      margin: 0;
      padding: 0;
      min-height: 100vh;
    }
    
    header {
      padding: 28px 24px;
      text-align: center;
      background: linear-gradient(to bottom, white, var(--bg));
      border-bottom: 1px solid rgba(255,90,134,0.1);
    }
    
    h1 {
      color: var(--pink);
      letter-spacing: 1px;
      margin: 0;
      font-size: 36px;
      font-weight: 600;
    }
    
    p.lead {
      color: var(--gray);
      margin: 8px 0 24px;
      font-size: 1.1rem;
    }
    
    .container {
      max-width: 920px;
      margin: 0 auto;
      padding: 16px;
    }
    
    .card {
      background: white;
      border-radius: 16px;
      box-shadow: 0 8px 24px var(--shadow);
      padding: 24px;
      transition: all 0.3s ease;
    }
    
    .welcome {
      background: var(--pink-light);
      padding: 20px;
      border-radius: 12px;
      margin-bottom: 20px;
      border: 1px solid rgba(255,90,134,0.15);
      font-size: 1.1rem;
      line-height: 1.5;
    }
    
    .chat {
      height: 420px;
      overflow: auto;
      padding: 16px;
      border-radius: 12px;
      border: 1px solid rgba(255,90,134,0.15);
      background: white;
      scroll-behavior: smooth;
    }
    
    .chat::-webkit-scrollbar {
      width: 8px;
    }
    
    .chat::-webkit-scrollbar-track {
      background: var(--bg);
      border-radius: 4px;
    }
    
    .chat::-webkit-scrollbar-thumb {
      background: var(--pink);
      border-radius: 4px;
    }
    
    .msg {
      margin: 12px 0;
      padding: 12px 16px;
      border-radius: 12px;
      max-width: 80%;
      position: relative;
      animation: messageIn 0.3s ease-out;
      line-height: 1.5;
    }
    
    @keyframes messageIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    .user {
      background: var(--pink-light);
      margin-left: auto;
      border: 1px solid rgba(255,90,134,0.2);
      border-bottom-right-radius: 4px;
    }
    
    .bot {
      background: white;
      border: 1px solid rgba(255,90,134,0.15);
      border-bottom-left-radius: 4px;
    }
    
    .msg::after {
      content: attr(data-time);
      position: absolute;
      bottom: -18px;
      font-size: 0.75rem;
      color: var(--gray);
      opacity: 0.8;
    }
    
    .user::after { right: 4px; }
    .bot::after { left: 4px; }
    
    .controls {
      display: flex;
      gap: 8px;
      margin-top: 16px;
      align-items: center;
    }
    
    .input {
      flex: 1;
      padding: 12px 20px;
      border-radius: 24px;
      border: 2px solid rgba(255,90,134,0.2);
      font-size: 1rem;
      transition: all 0.2s ease;
      background: white;
    }
    
    .input:focus {
      outline: none;
      border-color: var(--pink);
      box-shadow: 0 0 0 3px rgba(255,90,134,0.1);
    }
    
    button {
      background: var(--pink);
      color: white;
      border: none;
      padding: 12px 16px;
      border-radius: 24px;
      cursor: pointer;
      font-weight: 500;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }
    
    button:hover {
      background: var(--pink-dark);
      transform: translateY(-1px);
    }
    
    button:active {
      transform: translateY(1px);
    }
    
    button[disabled] {
      opacity: 0.7;
      cursor: not-allowed;
    }
    
    .quick {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px;
      margin: 20px 0;
    }
    
    .quick button {
      background: white;
      border: 2px solid rgba(255,90,134,0.2);
      color: var(--pink);
      padding: 12px 16px;
      border-radius: 20px;
      font-size: 0.95rem;
      width: 100%;
      text-align: left;
      position: relative;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
      transition: all 0.2s ease;
    }
    
    .quick button:hover {
      background: var(--pink-light);
      border-color: var(--pink);
      color: var(--pink-dark);
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(255,90,134,0.1);
    }
    
    .quick button:active {
      transform: translateY(1px);
      box-shadow: none;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
      .quick {
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      }
      
      .quick button {
        font-size: 0.9rem;
        padding: 10px 14px;
      }
    }
    
    .typing {
      display: inline-flex;
      gap: 4px;
      padding: 12px 16px;
      background: var(--bg);
      border-radius: 12px;
      font-size: 0.9rem;
      color: var(--gray);
      margin: 8px 0;
    }
    
    .typing span {
      width: 6px;
      height: 6px;
      background: var(--pink);
      border-radius: 50%;
      animation: typing 1s infinite;
      opacity: 0.5;
    }
    
    .typing span:nth-child(2) { animation-delay: 0.2s; }
    .typing span:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-4px); }
    }
    
    footer {
      padding: 24px;
      text-align: center;
      color: var(--gray);
      font-size: 0.9rem;
      background: linear-gradient(to top, white, transparent);
      margin-top: 32px;
    }
  </style>
</head>
<body>
  <header>
    <h1>MY PRIDE 💕</h1>
    <p class="lead">Talk periods. Track periods. Own your body.</p>
  </header>
  <div class="container">
    <div class="card">
      <div class="welcome">
        <strong>Hey sis 💕</strong> I’m <strong>MY PRIDE</strong> — your digital big sister here to chat about anything period-related. Ask me anything!
        <div style="margin-top:8px;color:#8a4460;font-size:0.95rem">Use the controls below to speak or send your message.</div>
      </div>

      <div class="quick">
        <!-- First Row: Basic Topics -->
        <button data-q="What happens during menstruation? Explain the basics." title="Learn about the menstrual cycle">
          🩸 Period Basics
        </button>
        <button data-q="How can I track my period and understand my cycle better?" title="Period tracking tips">
          📅 Track My Cycle
        </button>
        <button data-q="What are the best hygiene practices during periods?" title="Hygiene and self-care tips">
          🧼 Hygiene Tips
        </button>
        
        <!-- Second Row: Health & Wellness -->
        <button data-q="What helps with period cramps and pain?" title="Pain relief and comfort tips">
          🌸 Pain Relief
        </button>
        <button data-q="How can I handle PMS and mood changes?" title="Emotional wellness support">
          💗 Mood & PMS
        </button>
        <button data-q="What exercise and diet tips help during periods?" title="Health and wellness advice">
          🧘‍♀️ Wellness Tips
        </button>

        <!-- Third Row: Products & Care -->
        <button data-q="What menstrual products are available and how do I choose?" title="Learn about period products">
          🛡️ Product Guide
        </button>
        <button data-q="How do I handle leaks and stains?" title="Practical tips for accidents">
          � Leak Prevention
        </button>
        <button data-q="What should I pack in my period emergency kit?" title="Emergency preparation tips">
          🎒 Emergency Kit
        </button>

        <!-- Fourth Row: Support & Education -->
        <button data-q="How can I talk to others about periods?" title="Communication tips">
          💝 Talk About It
        </button>
        <button data-q="What's normal and when should I see a doctor?" title="Health guidance">
          ⚕️ Health Check
        </button>
        <button data-q="How can I help break period stigma?" title="Community support and advocacy">
          � Fight Stigma
        </button>
      </div>

      <div id="chat" class="chat" aria-live="polite"></div>

      <div class="controls">
        <input id="input" class="input" placeholder="Ask me anything about periods..." />
        <button id="send" title="Send text message">➤</button>
        <button id="listenBtn" title="Start voice input">🎙️</button>
        <button id="stopListenBtn" title="Stop voice input">⏹️</button>
        <button id="ttsToggle" aria-pressed="true" title="Toggle AI voice on/off">🔊 AI Voice On</button>
      </div>

    </div>
  </div>

  <footer>MY PRIDE — your digital big sister</footer>

  <script>
    const chat = document.getElementById('chat');
    const input = document.getElementById('input');
    const send = document.getElementById('send');
    const listenBtn = document.getElementById('listenBtn');
    const stopListenBtn = document.getElementById('stopListenBtn');
    const ttsToggle = document.getElementById('ttsToggle');

    // AI voice enabled flag persisted in localStorage (default: true)
    let ttsEnabled = (localStorage.getItem('ttsEnabled') !== 'false');
    function updateTtsButton(){
      if(ttsEnabled){
        ttsToggle.textContent = '🔊 AI Voice On';
        ttsToggle.setAttribute('aria-pressed','true');
        ttsToggle.title = 'AI voice is on. Click to turn off.';
      } else {
        ttsToggle.textContent = '🔇 AI Voice Off';
        ttsToggle.setAttribute('aria-pressed','false');
        ttsToggle.title = 'AI voice is off. Click to turn on.';
      }
    }
    updateTtsButton();
    ttsToggle.addEventListener('click', ()=>{
      ttsEnabled = !ttsEnabled;
      localStorage.setItem('ttsEnabled', ttsEnabled);
      updateTtsButton();
      if(!ttsEnabled && 'speechSynthesis' in window){
        // stop any ongoing speech immediately
        window.speechSynthesis.cancel();
      }
    });

    function formatTime() {
      const now = new Date();
      return now.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: true 
      }).toLowerCase();
    }

    function showTyping() {
      const typing = document.createElement('div');
      typing.className = 'typing';
      typing.innerHTML = 'typing<span></span><span></span><span></span>';
      chat.appendChild(typing);
      chat.scrollTop = chat.scrollHeight;
      return typing;
    }

    function append(kind, text, isError = false) {
      const d = document.createElement('div');
      d.className = 'msg ' + (kind === 'user' ? 'user' : 'bot');
      if (isError) d.style.borderColor = '#ff6b6b';
      d.textContent = text;
      d.setAttribute('data-time', formatTime());
      
      // Fade in animation
      d.style.opacity = '0';
      chat.appendChild(d);
      chat.scrollTop = chat.scrollHeight;
      
      // Trigger animation after a small delay
      requestAnimationFrame(() => {
        d.style.opacity = '1';
      });
    }

    function setControlsEnabled(enabled) {
      input.disabled = !enabled;
      send.disabled = !enabled;
      listenBtn.disabled = !enabled;
      document.querySelectorAll('.quick button').forEach(b => b.disabled = !enabled);
    }

    async function sendMessage(text) {
      if (!text.trim()) return;
      
      setControlsEnabled(false);
      append('user', text);
      
      const typingIndicator = showTyping();
      
      try {
        const res = await fetch('/chat', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({message: text})
        });
        
        typingIndicator.remove();
        
        const data = await res.json();
        if (data.error) {
          append('bot', 'Sorry, something went wrong: ' + data.error, true);
          speak('Sorry, something went wrong.');
        } else {
          append('bot', data.reply);
          speak(data.reply, data.lang || 'en');
        }
      } catch(e) {
        typingIndicator.remove();
        append('bot', 'Network error. Please try again.', true);
      } finally {
        setControlsEnabled(true);
        input.focus();
      }
    }

    // Handle send button click
    send.addEventListener('click', () => {
      const v = input.value.trim();
      if (!v) return;
      sendMessage(v);
      input.value = '';
    });

    // Handle input key events
    input.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        send.click();
      }
    });

    // Handle input changes
    input.addEventListener('input', () => {
      const v = input.value.trim();
      send.disabled = !v;
    });

    // Quick reply buttons
    document.querySelectorAll('.quick button').forEach(b => {
      b.addEventListener('click', () => {
        if (b.disabled) return;
        const q = b.dataset.q;
        // Animate the quick reply selection
        b.style.transform = 'scale(0.95)';
        setTimeout(() => b.style.transform = '', 150);
        
        input.value = q;
        send.click();
        
        // Disable all quick reply buttons briefly
        const buttons = document.querySelectorAll('.quick button');
        buttons.forEach(btn => btn.disabled = true);
        setTimeout(() => buttons.forEach(btn => btn.disabled = false), 1000);
      });
    });

    // Speech Synthesis (voice output)
    function speak(text, lang='en'){
      // Do nothing if TTS is disabled or the browser doesn't support speech
      if(!ttsEnabled || !('speechSynthesis' in window)) return;
      try{
        // Remove emoji characters so the TTS doesn't read them aloud.
        // Try a Unicode property escape first (modern browsers), fallback to common ranges.
        let cleaned = text;
        try{
          cleaned = cleaned.replace(/\p{Extended_Pictographic}/gu, '');
        }catch(e){
          // Fallback ranges for older engines
          cleaned = cleaned.replace(/[\u2600-\u27BF\u1F300-\u1F6FF\u1F900-\u1F9FF\u1F1E6-\u1F1FF]/g, '');
        }
        // Also remove leftover extra whitespace
        cleaned = cleaned.replace(/\s{2,}/g, ' ').trim();
        if(!cleaned) return; // nothing worth speaking after cleaning
        const u = new SpeechSynthesisUtterance(cleaned);
        u.lang = lang;
        u.rate = 1;
        // Cancel any current utterance to avoid overlap
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
      }catch(e){console.warn('TTS failed',e);}    
    }

    // Speech Recognition (voice input)
    let recognition;
    if('webkitSpeechRecognition' in window || 'SpeechRecognition' in window){
      const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognition = new Rec();
      recognition.lang = 'en-US';
      recognition.interimResults = false;
      recognition.onresult = (e)=>{
        const text = Array.from(e.results).map(r=>r[0].transcript).join('');
        input.value = text;
        sendMessage(text);
      };
      recognition.onerror = (e)=>{console.error('recognition error',e);}
    } else {
      listenBtn.disabled = true;
    }

    listenBtn.addEventListener('click', ()=>{if(recognition){recognition.start();}});
    stopListenBtn.addEventListener('click', ()=>{if(recognition){recognition.stop();}});

    // initial welcome bot message
    append('bot', 'Hey sis 💕 I\u2019m MY PRIDE — your digital big sister here to chat about anything period-related. Ask me anything!');
    speak('Hey sis, I am My Pride. I am your digital big sister. Ask me anything about periods.');
  </script>
</body>
</html>
'''


def call_model(messages, max_tokens=512, timeout=30):
    if not OPENROUTER_KEY:
        raise RuntimeError('OpenRouter API key not found.')

    headers = {
        'Authorization': f'Bearer {OPENROUTER_KEY}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:7860',
        'X-Title': 'MY PRIDE'
    }

    payload = {
        'model': MODEL_NAME,
        'messages': messages,  # OpenAI models handle system messages natively
        'temperature': 0.7,
        'max_tokens': max_tokens,
        'stream': False
    }

    try:
        resp = requests.post(OPENROUTER_API, headers=headers, json=payload, timeout=timeout)
    except requests.exceptions.RequestException as e:
        return {'error': f'API request failed: {str(e)}'}

    if resp.status_code != 200:
        try:
            return {'error': resp.json().get('error', {}).get('message', resp.text)}
        except Exception:
            return {'error': f'Status {resp.status_code}: {resp.text}'}

    try:
        data = resp.json()
        if 'choices' in data and len(data['choices']) > 0:
            message = data['choices'][0].get('message', {})
            if message and 'content' in message:
                return {'reply': message['content'].strip()}
        return {'error': 'No valid response content found'}
    except Exception as e:
        return {'error': f'Failed to parse response: {str(e)}'}


def likely_women_health_related(text):
    # Keywords organized by category for better maintenance and coverage
    keywords = {
        'menstrual': [
            'period', 'menstru', 'cramp', 'pms', 'pad', 'tampon', 'flow', 'spot', 
            'bleed', 'sanitary', 'cycle', 'ovulat', 'cup', 'leak', 'stain', 'discharge',
            'irregular', 'late', 'early', 'heavy', 'light', 'miss'
        ],
        'symptoms': [
            'pain', 'ache', 'tender', 'mood', 'emotion', 'irritable', 'fatigue',
            'breast', 'bloat', 'nausea', 'headache', 'migraine', 'back pain'
        ],
        'wellness': [
            'pregnancy', 'pregnant', 'birth control', 'contraceptive', 'hormone',
            'fertil', 'reproduc', 'gyneco', 'health', 'hygiene', 'self-care', 
            'stress', 'anxiety', 'depression', 'emotion'
        ],
        'support': [
            'shame', 'stigma', 'taboo', 'embarrass', 'afraid', 'worry', 'scared',
            'normal', 'advice', 'help', 'support', 'sister', 'woman', 'girl'
        ]
    }
    
    # Combine all keywords
    all_keywords = [kw for category in keywords.values() for kw in category]
    
    # Check if text contains any keywords
    t = (text or '').lower()
    return any(kw in t for kw in all_keywords)


def build_prompt(user_message, history, lang_code='en'):
    # Compose a prompt for the instruction model including system prompt and conversation history
    parts = [f"[SYSTEM]\n{SYSTEM_PROMPT}\nReply in the same language as the user's message ({lang_code}).\n---\n"]
    if history:
        for turn in history[-6:]:
            who = 'USER' if turn['role']=='user' else 'ASSISTANT'
            parts.append(f"[{who}]\n{turn['text']}\n")
    parts.append(f"[USER]\n{user_message}\n")
    parts.append('\n[ASSISTANT]\n')
    return "\n".join(parts)


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Empty message.'}), 400

    # detect language
    try:
        lang = detect(message)
    except LangDetectException:
        lang = 'en'

    # initialize session history
    history = session.get('history', [])
    history.append({'role': 'user', 'text': message})

    # Build messages for the chat
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    if history:
        for turn in history[-6:]:  # Keep last 6 turns for context
            role = "assistant" if turn['role'] == 'assistant' else "user"
            messages.append({"role": role, "content": turn['text']})
    
    # Add the current message with clear instructions for menstruation-related context
    if likely_women_health_related(message):
        context_message = (
            "Remember: You are MY PRIDE, a compassionate digital big sister. "
            "Provide empathetic, actionable advice about menstrual health. "
            "Give practical tips and emotional support. Stay focused on the user's needs."
        )
        messages.append({"role": "user", "content": context_message})
    
    messages.append({"role": "user", "content": message})
    
    # Call OpenRouter API
    model_res = call_model(messages)
    if 'error' in model_res:
        print(f"API Error: {model_res['error']}")  # Debug log
        session['history'] = history
        return jsonify({'error': "Sorry, I'm having trouble connecting. Please try again."}), 502

    reply = model_res.get('reply', '').strip()

    # If reply is empty, too short, or non-informative, prepare to retry
    retry_needed = False
    if not reply or len(reply) < 20 or 'i cannot' in reply.lower() or 'i am not able' in reply.lower():
        retry_needed = True

    # If the user's message is menstruation-related and the model response is weak, retry with explicit instructions
    if likely_women_health_related(message) and retry_needed:
        retry_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": (
                "Please answer this menstruation-related question directly and clearly in the same language as asked. "
                "Provide empathetic, actionable tips and short steps. If the question mentions cramps/pain, include at least 3 safe self-care tips. "
                "If the question mentions pad shortage or stigma, include practical alternatives and empowerment suggestions.\n\n"
                f"Question: {message}"
            )}
        ]
        alt_res = call_model(retry_messages)
        if 'reply' in alt_res and alt_res['reply'].strip():
            reply = alt_res['reply'].strip()
            retry_needed = False

    # Final fallback: short built-in answers to ensure helpful output when HF fails twice
    if (not reply or retry_needed) and likely_women_health_related(message):
        t = message.lower()
        if any(x in t for x in ['cramp', 'cramps', 'pain', 'pms']):
            reply = (
                "Here are some gentle self-care tips for cramps: 1) Use a warm heat pack on your lower belly for 15–20 minutes. "
                "2) Try gentle movement or light stretching. 3) Stay hydrated and rest when you can. 4) Over-the-counter pain relief (like ibuprofen) can help — follow dosing guidance and check with a clinician when needed. "
                "If pain is severe or sudden, please seek medical attention. 💕"
            )
        elif any(x in t for x in ['pad shortage', 'pad', 'sanitary', 'tampon', 'menstrual cup']):
            reply = (
                "If you can't access pads: consider clean cloths (changed and washed), menstrual cups or reusable pads when available, or layering soft fabric. "
                "Community centres, schools or local NGOs sometimes provide supplies — ask a trusted adult or local health worker. If you're in immediate need, local women's groups or social services can help."
            )
        elif 'stigma' in t or 'shame' in t or 'embarrass' in t:
            reply = (
                "Menstrual stigma is real — you're not alone. Share your experiences with trusted friends or supportive groups, learn facts to counter myths, and consider connecting with community groups or online spaces that advocate for menstrual equity. Education and conversation help reduce stigma. 💖"
            )
        else:
            reply = "I'm sorry — I couldn't reach the assistant right now. Please try rephrasing your question or ask something specific about hygiene, tracking, cramps, or support."

    history.append({'role': 'assistant', 'text': reply})
    # keep history in session (small; we keep only last N in prompt builder)
    session['history'] = history[-30:]

    return jsonify({'reply': reply, 'lang': lang})


if __name__ == '__main__':
    print('Starting MY PRIDE app...')
    if not OPENROUTER_KEY:
        print('WARNING: OPENROUTER_API_KEY environment variable not set. The app will not be able to call the model.')
        print('Set it in PowerShell like: $env:OPENROUTER_API_KEY = "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"')
    else:
        print('OpenRouter API key found ✓')
    print('Access the app at: http://127.0.0.1:7860')
    # debug True for development only
    app.run(host='0.0.0.0', port=7860, debug=True)
