def normalize_url(href: str, base_url: str) -> str:
    if not href:
        return None

    if href.startswith("//"):
        return "https:" + href

    if href.startswith("/"):
        return base_url.rstrip("/") + href

    return href
