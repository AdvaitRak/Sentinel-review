import httpx
from core.config import settings


async def get_pr_files(repo: str, pr_number: int) -> list[dict]:
    """Returns changed files with patch/diff info → used to build diff string for Gemini."""
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=_headers())
        response.raise_for_status()
        return response.json()


async def get_pr_branch(repo: str, pr_number: int) -> str:
    """Returns the PR branch name."""
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=_headers())
        response.raise_for_status()
        return response.json()["head"]["ref"]


async def get_full_file(repo: str, filepath: str, branch: str) -> str:
    """Returns full file content at the PR branch → used for Ruff."""
    import base64
    url = f"https://api.github.com/repos/{repo}/contents/{filepath}?ref={branch}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=_headers())
        response.raise_for_status()
        content = response.json()["content"]
        return base64.b64decode(content).decode("utf-8")


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
    }