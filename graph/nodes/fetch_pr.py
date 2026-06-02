from graph.state import PRReviewState


async def fetch_pr(state: PRReviewState) -> dict:
    return {"diff": None}