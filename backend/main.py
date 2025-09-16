from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache import FastAPICache
import contextlib

from database.db import create_db_and_tables
from domain.scale_plan.scale_plan_router import router as scale_plan_router
from domain.trade.trade_router import router as trade_router
from domain.annotation.annotation_router import router as annotation_router
from domain.execution.execution_router import router as execution_router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

    yield


app = FastAPI(
    title="Trading Journal API",
    description="API for managing trading journal",
    lifespan=lifespan,
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "PATCH", "DELETE", "PUT"],
    allow_headers=["*"],
)

app.include_router(trade_router, prefix="/api/trades", tags=["trades"])
app.include_router(scale_plan_router, prefix="/api/scale-plans", tags=["scale-plans"])
app.include_router(
    execution_router, prefix="/api/executions", tags=["trade-executions"]
)
app.include_router(annotation_router, prefix="/api/annotations", tags=["annotations"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
