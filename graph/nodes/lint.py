import logging
from graph.state import PRReviewState
from graph.tools.ruff_tool import run_ruff

logger = logging.getLogger(__name__)


async def lint(state: PRReviewState) -> dict:
    full_files = state.get("full_files")

    if not full_files:
        logger.warning("No full files in state, skipping lint")
        return {"lint_results": []}

    results = run_ruff(full_files)
    logger.info("Lint complete — %d issues found", len(results))
    for issue in results:
        logger.info("  [%s] %s line %d — %s", issue["code"], issue["file"], issue["line"], issue["message"])

    return {"lint_results": results}