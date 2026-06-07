from typing import Any, Optional
from typing_extensions import TypedDict


class PRReviewState(TypedDict):
    repo: str
    pr_number: int
    diff: Optional[str]
    lint_results: Optional[list[dict[str, Any]]]
    llm_review: Optional[dict[str, Any]]
    test_results: Optional[dict[str, Any]]