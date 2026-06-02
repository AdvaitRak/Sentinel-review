import json
import logging

from fastapi import APIRouter, BackgroundTasks, Depends, Request

from api.webhook.schema import WebhookPayload, WebhookResponse
from api.webhook.service import handle_pr_event
from core.security import verify_github_signature

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["webhook"])

TRIGGER_ACTIONS = {"opened", "synchronize", "reopened"}

@router.post("")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
) -> WebhookResponse:
    body = await verify_github_signature(request)  # raises 401 if invalid
    payload = WebhookPayload(**json.loads(body))

    if payload.action not in TRIGGER_ACTIONS:
        logger.debug("Ignored action: %s", payload.action)
        return WebhookResponse(
            accepted=False,
            pr_number=payload.pull_request.number,
            repo=payload.repository.full_name,
        )

    background_tasks.add_task(
        handle_pr_event,
        repo=payload.repository.full_name,
        pr_number=payload.pull_request.number,
    )

    return WebhookResponse(
        accepted=True,
        pr_number=payload.pull_request.number,
        repo=payload.repository.full_name,
    )