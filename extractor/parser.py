from __future__ import annotations

import re

_SCRIPT_URL_RE = re.compile(
    r"https?://api\.luarmor\.net/files/v\d+/l/[A-Za-z0-9_\-./]+\.lua",
    re.IGNORECASE,
)

_ANY_LUA_URL_RE = re.compile(
    r"https?://[^\s\"'()]+\.lua",
    re.IGNORECASE,
)

def extract_script_url(loader_code: str) -> str:
    """
    Extract the Luarmor script URL from loader source.

    Raises:
        ValueError: If loader_code is empty or no match found.
    """
    if not loader_code:
        raise ValueError("Loader code is empty.")

    match = _SCRIPT_URL_RE.search(loader_code)
    if not match:
        raise ValueError("No Luarmor script URL found in loader code.")

    return match.group(0)

def extract_all_lua_urls(loader_code: str) -> list[str]:
    """Return every unique .lua URL found in loader source, preserving order."""
    if not loader_code:
        return []
    return list(dict.fromkeys(_ANY_LUA_URL_RE.findall(loader_code)))
