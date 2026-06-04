from graph.state import PRReviewState
from graph.tools import github_pr_tool

async def fetch_pr(state: PRReviewState) -> dict:

    repo = state["repo"]
    pr_number = state["pr_number"]

    files = await github_pr_tool.get_pr_files(
        repo=repo,
        pr_number=pr_number,
    )

    diff_parts = []

    for file in files:
        patch = file.get("patch")

        if patch:
            diff_parts.append(
                f"\nFILE: {file['filename']}\n{patch}\n"
            )

    diff = "\n".join(diff_parts)
    print("diff................")
    print(diff)
    return {
        "diff": diff,
    }