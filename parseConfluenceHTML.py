import os
import json
from bs4 import BeautifulSoup

def extract_content_from_html(html_content):
    """
    Extract content from HTML and format it into a hierarchical dictionary.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract title
    title = soup.title.string if soup.title else "No Title"

    # Extract headings and associated paragraphs
    content_structure = []
    current_section = {"heading": None, "subsections": []}
    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        if element.name.startswith('h'):
            if current_section["heading"] or current_section["subsections"]:
                content_structure.append(current_section)
            current_section = {"heading": element.get_text(strip=True), "subsections": []}
        elif element.name == 'p' and current_section:
            current_section["subsections"].append(element.get_text(strip=True))
    
    if current_section["heading"] or current_section["subsections"]:
        content_structure.append(current_section)

    # Extract links
    links = [{"text": a.get_text(strip=True), "href": a['href']} for a in soup.find_all('a', href=True)]

    # Construct the content dictionary
    content = {
        "title": title,
        "content_structure": content_structure,
        "links": links
    }
    
    return content

def process_directory(directory_path, output_file):
    """
    Process all HTML files in the directory and save the extracted content to a JSONL file.
    """
    jsonl_data = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    content = extract_content_from_html(html_content)
                    jsonl_data.append(content)
    
    # Write the extracted content to a JSONL file
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in jsonl_data:
            f.write(json.dumps(entry) + '\n')

if __name__ == "__main__":
    # Directory containing the unzipped HTML files
    input_directory = 'confluencePages'
    
    # Output JSONL file
    output_file = 'swarm_documentation_v2.jsonl'
    
    # Process the directory and extract content
    process_directory(input_directory, output_file)
    
    print(f"Content extracted and saved to {output_file}")
