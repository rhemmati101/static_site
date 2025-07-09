def markdown_to_blocks(markdown: str) -> list[str]:
    block_strings: list[str] = []
    
    text_lines: list[str] = markdown.split("\n\n")
    
    #remove whitespace and extra empty lines
    text_lines = list(filter(lambda line: line != "", map(lambda text: text.strip(), text_lines)))

    return block_strings