import os
import PyPDF2
import json
import csv
import cohere
from src.prompt import get_prompt_1, get_prompt_2  # Import the prompts from prompt.py
# Initialize Cohere client
cohere_client = cohere.Client('bJUG8z3vdI97BogE8QJYyeyglJ5UtzpQYnxo3qh9')

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"An error occurred: {e}"

# Extract project details from CR text
def extract_project_details_cr_pdf(text):
    prompt1 = get_prompt_1(text)
    response = cohere_client.generate(
        model='command-r-plus-08-2024',
        prompt=f'From the following text, generate a numbered list of To-Do items:\n\nText:\n{text}\n\nTo-Do List:\n1. ',
    )
    
    extracted_data = response.generations[0].text.strip()
    project_info = {}

    try:
        for line in extracted_data.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                project_info[key.strip()] = value.strip()
    except Exception as e:
        return f"An error occurred during parsing: {e}"

    return project_info

# Save data to JSON file
def save_json_to_file(data, pdf_path):
    base_name = os.path.basename(pdf_path)
    json_name = f"{os.path.splitext(base_name)[0]}_pdf_cr_synthes.json"
    json_path = os.path.join(os.path.dirname(pdf_path), json_name)

    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return json_path

# Generate numbered To-Do list
def generate_numbered_todo_list_pdf(text):
    prompt2 = get_prompt_2(text)
    response = cohere_client.generate(
        model='command-r-plus-08-2024',
        prompt=f"Extract following detailed information from the text:\n"
               f"Synthèse des éléments pertinents :\n"
               f"2.Actions à prendre par SEF (Stores et Fermetures) :\n"
               f"Text:\n{text}",
        temperature=0.7,
        max_tokens=1500
    )

    todo_list = response.generations[0].text.strip()
    formatted_todo_list = [
        f"{i+1}. {item.strip()}"
        for i, item in enumerate(todo_list.split('\n'))
        if item.strip()
    ]
    return formatted_todo_list

# Save numbered To-Do list to CSV
def save_numbered_todo_list_to_csv(todo_list, pdf_path):
    base_name = os.path.basename(pdf_path)
    csv_name = f"{os.path.splitext(base_name)[0]}_pdf_todo_list.csv"
    csv_path = os.path.join(os.path.dirname(pdf_path), csv_name)

    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["To-Do List"])
            for item in todo_list:
                writer.writerow([item])
    except Exception as e:
        return f"An error occurred while saving CSV file: {e}"

    return csv_path

# Process all PDFs in a folder
def process_all_pdfs_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            pdf_text = extract_text_from_pdf(pdf_path)


            # Extract and save CR details
            cr_details = extract_project_details_cr_pdf(pdf_text)
            cr_json_path = save_json_to_file(cr_details, pdf_path)
            print(f"CR details saved to {cr_json_path}")

            # Generate and save To-Do list
            todo_list = generate_numbered_todo_list_pdf(pdf_text)
            csv_path = save_numbered_todo_list_to_csv(todo_list, pdf_path)
            print(f"To-Do list saved to {csv_path}")

