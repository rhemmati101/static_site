import re
import os

from processmarkdown import markdown_to_html_node

def extract_title(markdown: str) -> str:
    matches: list[str] = re.findall(r"^# +([^\n]*)$", markdown, flags=re.MULTILINE)
    if matches:
        return matches[0].strip()

    raise Exception("no title found")

def get_file_contents(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise Exception(f"path {filepath} not found")
    
    with open(filepath) as file:
        return file.read()

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_text: str = get_file_contents(from_path)
    template_text: str = get_file_contents(template_path)

    from_text_html: str = markdown_to_html_node(from_text).to_html()

    title: str = extract_title(from_text)

    html_page: str = template_text.replace("{{ Title }}", title).replace("{{ Content }}", from_text_html)
    html_page = html_page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')


    if not os.path.exists(os.path.dirname(dest_path)):
        print("Creating directory at " + dest_path)
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as file:
        file.write(html_page)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    if not os.path.exists(dir_path_content):
        raise ValueError("invalid content path passed as input")
    if not os.path.exists(template_path):
        raise ValueError("invalid template path passed as input")

    contents: list[str] = os.listdir(dir_path_content)
    print(f"contents of {dir_path_content}: {contents}")

    for c in contents:
        c_path = os.path.join(dir_path_content, c)
        dest_c_path = os.path.join(dest_dir_path, c)

        if os.path.isfile(c_path):
            dest_html_path: str = os.path.splitext(dest_c_path)[0] + ".html"
            generate_page(c_path, template_path, dest_html_path, basepath)
        elif os.path.isdir(c_path):
            generate_pages_recursive(c_path, template_path, dest_c_path, basepath)
        else:
            raise NotImplementedError()