from typing import Any, Optional
from typing_extensions import TypedDict


class PRReviewState(TypedDict):
    repo: str
    pr_number: int
    pr_branch: str                        # PR branch name
    diff: Optional[str]                   # diff only → Gemini
    full_files: Optional[dict[str, str]]  # {filename: content} → Ruff
    lint_results: Optional[list[dict[str, Any]]]
    llm_review: Optional[dict[str, Any]]
    test_results: Optional[dict[str, Any]]