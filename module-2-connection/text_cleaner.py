import re # We import the regular expression library to find and replace text patterns.

def wash_dirty_text(raw_data: str) -> str:
    # We use a pattern to find anything that looks like an HTML tag and replace it with nothing.
    no_html = re.sub('<[^<]+?>', '', raw_data)
    
    # We find any spot with multiple spaces or newlines and crush them down to a single space.
    crushed_spaces = re.sub(r'\s+', ' ', no_html)
    
    # We strip any leftover empty space from the very beginning and the very end of the text.
    clean_text = crushed_spaces.strip()
    
    return clean_text

# We create a fake, messy input exactly like you would get from a bad web scraper.
disgusting_input = "<html>   <body> Hello! \n\n\n This is   a terrible string. <script>ignore</script> </body> </html>"

# We run the wash function.
ready_for_llm = wash_dirty_text(disgusting_input)
print(ready_for_llm)
