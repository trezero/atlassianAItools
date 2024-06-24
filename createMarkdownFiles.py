import json

def parse_jsonl(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [json.loads(line) for line in lines]

def json_to_markdown(json_obj):
    markdown = f"# {json_obj.get('title', 'No Title')}\n\n"
    
    for section in json_obj.get('content_structure', []):
        markdown += f"## {section['heading']}\n\n"
        for subsection in section.get('subsections', []):
            markdown += f"- {subsection}\n"
        markdown += "\n"
    
    for link in json_obj.get('links', []):
        markdown += f"[{link['text']}]({link['href']})\n"
    
    return markdown

def save_markdown_docs(markdown_docs, output_dir):
    for i, doc in enumerate(markdown_docs):
        with open(f"{output_dir}/document_{i+1}.md", 'w') as file:
            file.write(doc)

def save_combined_markdown(markdown_docs, output_file):
    with open(output_file, 'w') as file:
        for doc in markdown_docs:
            file.write(doc + "\n\n")

# Parse the JSONL file
jsonl_data = parse_jsonl('swarm_documentation_v2.jsonl')  # replace with your actual JSONL file path

# Convert each JSON object to Markdown
markdown_docs = [json_to_markdown(obj) for obj in jsonl_data]

# Save each document separately
save_markdown_docs(markdown_docs, 'output')  # replace with your desired output directory

# OR Save all documents combined into a single Markdown file
save_combined_markdown(markdown_docs, 'combined_document.md')
