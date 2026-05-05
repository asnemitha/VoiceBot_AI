# 🤖 VoiceBot AI — Multilingual Order Confirmation System

An automated voice calling system that confirms customer orders in their native Indian language using Twilio, FastAPI, and AI-powered speech recognition.

> Built for India's tier-2 and tier-3 markets where voice-first UX matters most.

---
# Live link: https://asnemitha.github.io/VoiceBot_AI/

## 📽️ Demo

```
Bot calls customer
    ↓
"Hello Ravi! Your order is 2x Idli, 1x Coffee. Say YES to confirm, NO to cancel, LATER to reschedule."
    ↓
Customer says "Haan" (Yes in Hindi)
    ↓
"Aapka order confirm ho gaya! Dhanyavaad!"
    ↓
Call ends. Order marked confirmed in database.
```

---

## ✨ Features

- 📞 **Automated outbound calls** via Twilio
- 🗣️ **Speech recognition** — customer can speak naturally
- ⌨️ **DTMF fallback** — press 1/2/3 if speech fails
- 🌍 **5 Indian languages** — English, Hindi, Kannada, Marathi, Telugu
- 🔄 **Smart rescheduling** — callback in 2 hours, 3 hours, or tomorrow 10 AM
- 📊 **Live dashboard** — track all order statuses in real time
- 🔁 **Auto retry** — retries up to 3 times if no response
- ⏰ **Scheduled callbacks** — APScheduler fires callbacks at exact time

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Voice Calls | Twilio Programmable Voice |
| Speech-to-Text | Twilio STT |
| Text-to-Speech | Google WaveNet, Amazon Polly |
| Database | SQLite |
| Scheduler | APScheduler |
| Tunneling (dev) | ngrok |

---

## 🌍 Supported Languages

| Code | Language | Voice Used |
|---|---|---|
| `en` | English | Polly.Raveena |
| `hi` | Hindi | Google.hi-IN-Wavenet-A |
| `kn` | Kannada | Google.kn-IN-Standard-A |
| `mr` | Marathi | Google.mr-IN-Standard-A |
| `te` | Telugu | Google.te-IN-Standard-A |

---

## 📁 Project Structure

```
voicebot-ai/
├── backend/
│   ├── main.py          # FastAPI app, all webhooks and routes
│   ├── database.py      # SQLite connection and init
│   ├── models.py        # Order and CallLog models
│   └── requirements.txt
├── frontend/
│   └── index.html       # Dashboard UI
├── logs/
│   └── voicebot.log     # Auto-generated logs
├── .env                 # Your credentials (never commit this)
├── .env.example         # Template for env vars
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/voicebot-ai.git
cd voicebot-ai
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn twilio python-dotenv apscheduler
```

### 3. Create your `.env` file

```bash
cp .env.example .env
```

Fill in your credentials:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
BASE_URL=https://your-ngrok-url.ngrok-free.app
```

### 4. Start ngrok

```bash
ngrok http 8000
```

Copy the `https://xxxx.ngrok-free.app` URL and paste it as `BASE_URL` in your `.env`

### 5. Run the server

```bash
cd backend
python main.py
```

Open `http://localhost:8000` in your browser.

---

## 🔁 Call Flow

```
Customer receives call
        ↓
Press any key to start
        ↓
Bot reads order details in customer's language
        ↓
Customer responds (voice or keypad)
        ↓
    ┌───────────────────────────────┐
    │                               │
   YES                             NO                          LATER
    │                               │                            │
Confirmed ✅                   Cancelled ❌              Reschedule menu 🔄
                                                                 │
                                                    ┌────────────┼────────────┐
                                                    1            2            3
                                                 +2 hours     +3 hours   Tomorrow
                                                                          10 AM IST
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Frontend dashboard |
| `POST` | `/call` | Trigger outbound call |
| `GET` | `/orders` | List all orders |
| `GET` | `/orders/{order_id}` | Get single order |
| `GET` | `/stats` | Confirmed/cancelled/pending counts |
| `GET` | `/scheduled` | List scheduled callbacks |
| `DELETE` | `/scheduled/{job_id}` | Cancel a scheduled callback |
| `POST` | `/webhook/trial_bypass` | Twilio entry webhook |
| `POST` | `/webhook/greet` | Plays order details to customer |
| `POST` | `/webhook/response` | Handles customer response |
| `POST` | `/webhook/reschedule_time` | Handles reschedule choice |
| `POST` | `/webhook/status` | Twilio call status updates |

---

## 📊 Order Statuses

| Status | Meaning |
|---|---|
| `pending` | Call initiated, waiting for response |
| `confirmed` | Customer said YES |
| `cancelled` | Customer said NO |
| `rescheduled` | Customer asked for callback |
| `no_response` | No answer after 3 retries |
| `no_answer` | Customer did not pick up |
| `failed` | Twilio or system error |

---

## 🧠 Intent Detection

The bot understands customer responses via keyword matching across all 5 languages:

| Intent | English | Hindi | Kannada | Marathi | Telugu |
|---|---|---|---|---|---|
| Confirm | yes, sure, ok | haan, ji | houdu, sari | ho, hoy | avunu |
| Cancel | no, cancel | nahi, radd | beda, illa | nako | vaddu |
| Reschedule | later, wait | baad mein | nantara | nantar | tarvata |

---

## 🚀 Production Deployment

For production, replace ngrok with a real server:

```bash
# Deploy to Railway / Render / AWS EC2
# Set BASE_URL to your domain
BASE_URL=https://yourdomain.com

# Use PostgreSQL instead of SQLite for scale
# Use a process manager like gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token |
| `TWILIO_PHONE_NUMBER` | Your Twilio phone number |
| `BASE_URL` | Public URL where your server is accessible |

---

## 📌 Known Limitations

- SQLite not suitable for high concurrency — use PostgreSQL in production
- ngrok URL changes on every restart — update `.env` each time
- Keyword matching may misfire on complex sentences (e.g. "I will NOT cancel" triggers cancel)
- No human agent handoff currently

---

## 🛣️ Roadmap

- [ ] WhatsApp integration
- [ ] GPT-powered dynamic conversation
- [ ] Sentiment detection — escalate frustrated customers
- [ ] CRM integration (Zoho, Salesforce)
- [ ] PostgreSQL support
- [ ] Docker support
- [ ] Real-time dashboard with websockets

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

```bash
git checkout -b feature/your-feature
git commit -m "Add your feature"
git push origin feature/your-feature
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👨‍💻 Built With ❤️ for Bharat

> Helping businesses reach every customer in their own language, automatically.
