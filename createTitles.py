import json
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Function to parse the JSONL file
def parse_jsonl(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [json.loads(line) for line in lines]

# Function to generate a title using the LLM
def generate_title(content_structure):
    # Prepare the prompt for the LLM based on content_structure
    prompt = "Based on the following content structure, generate a concise and relevant title:\n\n"
    for section in content_structure:
        prompt += f"Section: {section['heading']}\n"
        for subsection in section.get('subsections', []):
            prompt += f"  - {subsection}\n"
    
    # Send the prompt to the local LLM
    completion = client.chat.completions.create(
        model="lmstudio-community/Llama3-ChatQA-1.5-70B-GGUF",
        messages=[
            {"role": "system", "content": "Generate a concise and relevant title for the given content structure."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    
    # Access the content properly
    return completion.choices[0].message.content.strip()

# Function to update the JSON objects
def update_titles(jsonl_data):
    for obj in jsonl_data:
        if obj.get('title') == "No Title":
            obj['title'] = generate_title(obj['content_structure'])
    return jsonl_data

# Function to save the updated JSON objects back to JSONL file
def save_jsonl(jsonl_data, file_path):
    with open(file_path, 'w') as file:
        for obj in jsonl_data:
            file.write(json.dumps(obj) + '\n')

# Main script
def main():
    input_file = 'swarm_documentation_v2.jsonl'  # Replace with your JSONL file path
    output_file = 'updatedTitles.jsonl'  # Replace with your desired output file path

    jsonl_data = parse_jsonl(input_file)
    updated_data = update_titles(jsonl_data)
    save_jsonl(updated_data, output_file)

if __name__ == "__main__":
    main()
