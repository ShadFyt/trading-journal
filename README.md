# 📈 Personal Trading Journal App

A minimal yet visually appealing trading journal and watchlist management app built for serious swing traders. Designed for **tracking trade ideas**, **managing live trades**, and **viewing live market prices** via [Finnhub](https://finnhub.io/).

> 🚀 Built using **Vue 3 + TailwindCSS + shadcn/vue** for the frontend and **FastAPI + Python** for the backend.

---

## 📌 Purpose

This app is a **personal trading journal and watchlist manager** to:

- Log and organize **trade ideas** with detailed trade plans
- Monitor and manage **live trades**
- Display **live market prices** using the **Finnhub API**
- Build a focused, distraction-free interface that is trader-centric

---

## ✨ Features (MVP)

### ✅ Core Features

- **Watchlist Management**: Add trade ideas with full trading plans (entry, stop, targets, rating, catalyst)
- **Live Trade Tracker**: View and update currently open trades
- **Live Market Prices**: Integrate real-time prices via **Finnhub API**
- **Clean, Professional UI**: Using **Vue 3**, **TailwindCSS**, and **shadcn/vue** components

---

## 🏗️ Tech Stack

| Layer         | Technology                  |
|---------------|-----------------------------|
| Frontend      | Vue 3, TailwindCSS, shadcn/vue |
| Backend       | FastAPI (Python)            |
| Live Data API | [Finnhub API](https://finnhub.io/) |
| State Mgmt    | Pinia (or Vue Composition API) |
| Styling       | TailwindCSS + shadcn        |
| Persistence   | SQLite (MVP) or PostgreSQL (scalable) |
| Auth (Optional MVP) | Token-based (local storage or JWT) |

---
## 🗂️ Suggested Folder Structure
```
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ ├── pages/
│ │ ├── stores/
│ │ ├── api/
│ │ └── App.vue
├── backend/
│ ├── app/
│ │ ├── models/
│ │ ├── routes/
│ │ ├── services/
│ │ └── main.py
├── README.md
├── requirements.txt
├── .env (API Keys)
```

## 🔮 Future Features (Roadmap)
| Feature                                                    | Status     |
| ---------------------------------------------------------- | ---------- |
| ✅ Basic Watchlist                                          | ✅ MVP      |
| ✅ Live Trade Tracker                                       | ✅ MVP      |
| 🔄 Price Alerts (Email/SMS)                                | 🔜 Planned |
| 🔄 Trade Review Dashboard (metrics, win rate, R-multiples) | 🔜 Planned |
| 🔄 Custom Scanner (Breakouts, Retests)                     | 🔜 Planned |
| 🔄 Tagging & Filtering                                     | 🔜 Planned |
| 🔄 Export to CSV / PDF                                     | 🔜 Planned |

## 🧪 Development Setup
```bash
# Backend
# Install Poetry if you haven't already
pip install poetry

# Install dependencies
cd backend
poetry install

# Activate shell (optional, for Poetry-managed venv)
poetry shell

# Run the backend
poetry run uvicorn app.main:app --reload
```

```bash
# Frontend
npm install
npm run dev
```

## 🎯 Goals
- Build a consistent routine around planning and reviewing trades

- Eliminate emotion by pre-defining trade logic

- Streamline workflow to spend less time tracking and more time executing high-quality setups