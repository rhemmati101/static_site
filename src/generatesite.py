import re
import os

from processmarkdown import markdown_to_html_node

def extract_title(markdown: str) -> str:
    matches: list[str] = re.findall(r"^# +([^\n]*)$", markdown, flags=re.MULTILINE)
    if matches:
        return matches[0].strip()

    raise Exception("no title found")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_text: str = get_file_contents(from_path)
    template_text: str = get_file_contents(template_path)

    from_text_html: str = markdown_to_html_node(from_text).to_html()

    title: str = extract_title(from_text)

    html_page: str = template_text.replace("{{ Title }}", title).replace("{{ Content }}", from_text_html)


    if not os.path.exists(os.path.dirname(dest_path)):
        print("Creating directory at " + dest_path)
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as file:
        file.write(html_page)
    




def get_file_contents(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise Exception(f"path {filepath} not found")
    
    with open(filepath) as file:
        return file.read()