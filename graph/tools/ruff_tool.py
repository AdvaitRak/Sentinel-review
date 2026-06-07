import subprocess
import tempfile
import os
import json
import logging

logger = logging.getLogger(__name__)


def run_ruff(full_files: dict[str, str]) -> list[dict]:
    with tempfile.TemporaryDirectory() as tmpdir:
        _write_files(full_files, tmpdir)
        return _run_ruff_on_dir(tmpdir)


def _write_files(full_files: dict[str, str], tmpdir: str):
    for filename, content in full_files.items():
        filepath = os.path.join(tmpdir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)


def _run_ruff_on_dir(tmpdir: str) -> list[dict]:
    result = subprocess.run(
        ["ruff", "check", tmpdir, "--output-format=json"],
        capture_output=True,
        text=True,
    )

    if not result.stdout.strip():
        return []

    try:
        raw = json.loads(result.stdout)
        return [
            {
                "file": os.path.relpath(issue["filename"], tmpdir),
                "line": issue["location"]["row"],
                "col": issue["location"]["column"],
                "code": issue["code"],
                "message": issue["message"],
            }
            for issue in raw
        ]
    except Exception:
        logger.exception("Failed to parse ruff output")
        return []