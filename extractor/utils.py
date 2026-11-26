def save_to_file(content: str, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
