from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def save_to_file(content: str, path: str | Path) -> Path:
    """
    Write content to path, creating parent directories if needed.

    Returns:
        The resolved Path that was written.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    logger.info("Saved %d bytes to %s", len(content), target)
    return target
