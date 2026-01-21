def config_loader(file_path: str) -> set:
    with open(file_path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())