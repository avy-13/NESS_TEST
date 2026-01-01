import re


def parse_price(text):
    match = re.search(r"([\d.]+)", text.replace(",", ""))
    return float(match.group(1)) if match else None
