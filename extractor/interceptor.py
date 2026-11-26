from __future__ import annotations

import logging
from typing import Mapping

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

DEFAULT_HEADERS: Mapping[str, str] = {
    "User-Agent": "Roblox/WinInet",
    "Accept": "*/*",
}

def _build_session(retries: int = 3, backoff: float = 0.5) -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_url(
    url: str,
    *,
    timeout: float = 10.0,
    headers: Mapping[str, str] | None = None,
    session: requests.Session | None = None,
) -> str:
    """
    Fetch a URL and return its body as text (no execution).

    Raises:
        ValueError: If URL is empty or not http(s).
        RuntimeError: On network or HTTP failure.
    """
    if not url or not url.startswith(("http://", "https://")):
        raise ValueError(f"Invalid URL: {url!r}")

    sess = session or _build_session()
    merged_headers = {**DEFAULT_HEADERS, **(headers or {})}

    logger.debug("Fetching: %s", url)
    try:
        resp = sess.get(url, headers=merged_headers, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch {url!r}: {exc}") from exc

    return resp.text

capture_loader = fetch_url
