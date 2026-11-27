
from __future__ import annotations

import re
from urllib.parse import urlparse


SUPPORTED_HOSTS = {
    "api.luarmor.net",
    "cdn.luarmor.net",
}


LOADER_PATH_RE = re.compile(
    r"^/files/v\d+/(?:loaders|l)/[A-Za-z0-9_.\-/]+\.lua$",
    re.IGNORECASE,
)


CDN_PATH_RE = re.compile(
    r"^/[A-Za-z0-9_.\-/]+\.lua$",
    re.IGNORECASE,
)


URL_RE = re.compile(
    r"https?://[^\s\"'<>]+",
    re.IGNORECASE,
)


TRAILING_CHARS = ".,;:!?)]}"


def clean_url(url: str) -> str:
    """
    Remove trailing punctuation from a URL.
    """
    return url.strip().rstrip(TRAILING_CHARS)


def parse_url(url: str):
    """
    Parse and validate a Luarmor URL.

    Only supported Luarmor hosts are accepted.
    """
    if not url:
        return None

    try:
        parsed = urlparse(url)

        # Accessing parsed.port may raise ValueError
        # when the port is malformed.
        port = parsed.port

    except ValueError:
        return None

    if parsed.scheme.lower() not in ("http", "https"):
        return None

    if not parsed.hostname:
        return None

    hostname = parsed.hostname.lower()

    if hostname not in SUPPORTED_HOSTS:
        return None

    if parsed.username or parsed.password:
        return None

    if port not in (None, 80, 443):
        return None

    if not parsed.path.lower().endswith(".lua"):
        return None

    return parsed


def is_loader_url(url: str) -> bool:
    """
    Check whether a URL is a supported Luarmor loader URL.
    """
    parsed = parse_url(url)

    if parsed is None:
        return False

    if parsed.hostname.lower() != "api.luarmor.net":
        return False

    return bool(
        LOADER_PATH_RE.fullmatch(parsed.path)
    )


def is_cdn_url(url: str) -> bool:
    """
    Check whether a URL is a supported Luarmor CDN URL.
    """
    parsed = parse_url(url)

    if parsed is None:
        return False

    if parsed.hostname.lower() != "cdn.luarmor.net":
        return False

    return bool(
        CDN_PATH_RE.fullmatch(parsed.path)
    )


def extract_all_lua_urls(loader_code: str) -> list[str]:
    """
    Extract all unique supported Luarmor .lua URLs.

    Loader and CDN URLs are included.
    The original order is preserved.
    """
    if not loader_code:
        return []

    results = []
    seen = set()

    for match in URL_RE.findall(loader_code):
        url = clean_url(match)

        if not (
            is_loader_url(url)
            or is_cdn_url(url)
        ):
            continue

        if url not in seen:
            seen.add(url)
            results.append(url)

    return results


def extract_loader_urls(loader_code: str) -> list[str]:
    """
    Extract only supported Luarmor loader URLs.
    """
    return [
        url
        for url in extract_all_lua_urls(loader_code)
        if is_loader_url(url)
    ]


def extract_cdn_urls(loader_code: str) -> list[str]:
    """
    Extract only supported Luarmor CDN URLs.
    """
    return [
        url
        for url in extract_all_lua_urls(loader_code)
        if is_cdn_url(url)
    ]


def extract_script_url(loader_code: str) -> str:
    """
    Extract the first supported Luarmor loader URL.

    Raises:
        ValueError: If loader_code is empty or no supported
                    loader URL is found.
    """
    if not loader_code:
        raise ValueError("Loader code is empty.")

    urls = extract_loader_urls(loader_code)

    if not urls:
        raise ValueError("No supported loader URL found.")

    return urls[0]
