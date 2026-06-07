import logging

from graph.graph import review_graph
from graph.state import PRReviewState

logger = logging.getLogger(__name__)


async def handle_pr_event(repo: str, pr_number: int) -> None:
    """
    Runs in a background task — FastAPI has already returned 200 before this.
    """
    logger.info("Starting review: %s #%d", repo, pr_number)

    initial_state: PRReviewState = {
        "repo": repo,
        "pr_number": pr_number,
        "pr_branch": "",
        "diff": None,
        "full_files": None,
        "lint_results": None,
        "llm_review": None,
        "test_results": None,
    }

    try:
        final_state = await review_graph.ainvoke(initial_state)
        logger.info("Review done: %s #%d", repo, pr_number)
    except Exception:
        logger.exception("Pipeline failed: %s #%d", repo, pr_number)