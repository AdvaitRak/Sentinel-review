import logging

from fastapi import FastAPI

from api.webhook.router import router as webhook_router
from api.health.router import router as health_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)

app = FastAPI(title="CodeReviewAgent")

app.include_router(webhook_router)
app.include_router(health_router)