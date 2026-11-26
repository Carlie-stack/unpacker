import requests

def capture_loader(loader_url: str) -> str:
    """
    Simulate fetching a Luarmor loader script.
    This does not execute the script, but captures the raw response.
    """
    headers = {
        "User-Agent": "Roblox/WinInet",
        "Accept": "*/*"
    }
    try:
        response = requests.get(loader_url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch loader: {e}")
