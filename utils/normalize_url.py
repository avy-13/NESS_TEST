def normalize_url(href: str, base_url: str) -> str:
    if "punish" in href or "captcha" in href:
        return None

    if not href:
        return None

    if href.startswith("//"):
        return "https:" + href

    if href.startswith("/"):
        return base_url.rstrip("/") + href

    if not href.startswith("https"):
        href = "https:" + href

    if "punish" in href:
        return None

    return href
