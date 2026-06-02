from pydantic import BaseModel


class PRUser(BaseModel):
    login: str


class PRHead(BaseModel):
    ref: str  # branch name e.g. "feature/add-auth"


class PullRequest(BaseModel):
    number: int
    title: str
    user: PRUser
    head: PRHead


class Repository(BaseModel):
    full_name: str  # "owner/repo"


class WebhookPayload(BaseModel):
    action: str  # "opened", "synchronize", "reopened", "closed" etc.
    pull_request: PullRequest
    repository: Repository


class WebhookResponse(BaseModel):
    accepted: bool
    pr_number: int
    repo: str