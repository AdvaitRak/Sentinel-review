import asyncio
import logging
from graph.state import PRReviewState
from graph.tools import github_pr_tool

logger = logging.getLogger(__name__)


async def fetch_pr(state: PRReviewState) -> dict:
    repo = state["repo"]
    pr_number = state["pr_number"]

    # concurrent fetch of files and branch
    files, branch = await asyncio.gather(
        github_pr_tool.get_pr_files(repo=repo, pr_number=pr_number),
        github_pr_tool.get_pr_branch(repo=repo, pr_number=pr_number),
    )

    # build diff string for Gemini
    diff_parts = []
    for file in files:
        patch = file.get("patch")
        if patch:
            diff_parts.append(f"\nFILE: {file['filename']}\n{patch}\n")
    diff = "\n".join(diff_parts)

    # filter only changed python files that weren't deleted
    py_files = [
        f for f in files
        if f["filename"].endswith(".py") and f.get("status") != "removed"
    ]

    # fetch all full file contents concurrently
    contents = await asyncio.gather(*[
        github_pr_tool.get_full_file(repo=repo, filepath=f["filename"], branch=branch)
        for f in py_files
    ])

    # zip filenames with contents
    full_files = dict(zip([f["filename"] for f in py_files], contents))

    logger.info(
        "Fetched %d full files for ruff, diff ready for Gemini — branch: %s",
        len(full_files),
        branch,
    )

    return {
        "diff": diff,
        "full_files": full_files,
        "pr_branch": branch,
    }