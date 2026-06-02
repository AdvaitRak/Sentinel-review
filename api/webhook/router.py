import json
import logging

from fastapi import APIRouter, BackgroundTasks, Request

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
    body = await verify_github_signature(request)

    event_type = request.headers.get("X-GitHub-Event")
    if event_type != "pull_request":
        logger.debug("Ignored event type: %s", event_type)
        return WebhookResponse(accepted=False, pr_number=0, repo="")

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

    logger.info("Queued: %s #%d", payload.repository.full_name, payload.pull_request.number)
    return WebhookResponse(
        accepted=True,
        pr_number=payload.pull_request.number,
        repo=payload.repository.full_name,
    )