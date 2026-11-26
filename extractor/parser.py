import re

def extract_script_url(loader_code: str) -> str:
    """
    Extract the actual script URL from a Luarmor loader.
    Luarmor loaders typically contain a URL like:
    https://api.luarmor.net/files/v3/l/<hash>.lua
    """
    pattern = r"https?://api\.luarmor\.net/files/[^\s\"']+"
    match = re.search(pattern, loader_code)
    if match:
        return match.group(0)
    raise ValueError("No Luarmor script URL found in loader code.")
