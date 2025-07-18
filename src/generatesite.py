import re

def extract_title(markdown: str) -> str:
    matches: list[str] = re.findall(r"^# +([^\n]*)$", markdown, flags=re.MULTILINE)
    if matches:
        return matches[0].strip()

    raise Exception("no title found")