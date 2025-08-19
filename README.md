# 📈 Personal Trading Journal App

A full-stack application for capturing swing-trading ideas and managing live trades.

## 📌 Purpose

Provide a focused workspace to plan, execute and review trades without distraction.

## ✨ Features

### Watchlist & Trade Ideas
- Log setups with entry range, stop, targets, rating, catalysts and notes.
- Search, filter by status and convert ideas into live trades when a setup triggers.

### Live Trade Management
- Track open positions with current price, remaining shares and realized P&L.
- Attach annotations for catalysts, trade notes and management notes.
- Plan partial exits or adds with per-target scale plans.
- Record trade executions and automatically compute R/R metrics.

### Real-Time Market Data
- Display live prices via the [Finnhub](https://finnhub.io/) API.

## 🏗️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Vue 3, Vite, TailwindCSS, shadcn/vue, TypeScript |
| State Mgmt | Pinia / Composition API |
| Backend | FastAPI, SQLModel, Alembic |
| Database | SQLite (dev) |
| Live Data API | Finnhub |

## 🗂️ Project Structure

```
.
├── backend        # FastAPI application
│   ├── core       # configuration and dependencies
│   ├── database   # SQLModel models and session
│   └── domain     # trade_idea, live_trade, scale_plan, annotation modules
└── frontend       # Vue 3 SPA
    └── src
        ├── components
        ├── pages
        └── composables
```

## 🧪 Development Setup

### Backend

```bash
cd backend
poetry install
# optional: poetry shell
alembic upgrade head  # run database migrations
poetry run uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 🔮 Roadmap

- Price alerts (email/SMS)
- Trade review dashboard with statistics
- Tagging & filtering
- Export to CSV / PDF

