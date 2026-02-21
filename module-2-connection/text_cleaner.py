import re 

def wash_dirty_text(raw_data: str) -> str:
    # We use a pattern to find anything that looks like an HTML tag.
    no_html = re.sub('<[^<]+?>', '', raw_data)
    # We crush multiple spaces/newlines down to a single space.
    crushed_spaces = re.sub(r'\s+', ' ', no_html)
    return crushed_spaces.strip()
