
import os
import docx
import json
import csv
import cohere

# Initialize the Coher client with your API key
cohere_client = cohere.Client('IdlHWXxZ6LEt90RvFKvXKv4CYzrR8BCQLq63yriI')
def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"An error occurred: {e}"

def extract_project_details_cr_dox(text):
    response = cohere_client.generate(
        model='command-r-plus-08-2024',
        prompt=f"Extract following detailed information from the text:\n"
               f"Synthèse des éléments pertinents:\n"
               f"2. Actions à prendre par SEF (Stores et Fermetures):\n"
               f"Extract the following detailed information from the text:\n"
               f"1. Nom du projet\n"
               f"2. Numéro du RC\n"
               f"3. Description\n"
               f"4. Date limite de soumission\n"
               f"5. Adresse\n"
               f"6. Visites obligatoires\n"
               f"7. Objet de la consultation\n"
               f"8. Votre lot:\n"
               f"9. Durée des marchés:\n"
               f"10. Contact de l'acheteur (Nom, Titre, Téléphone, Courriel)\n"
               f"11. Acheteur:\n\n"
               f"Text:\n{text}"
               
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

def save_json_to_file(data, docx_path, suffix='_cr_synthes.json'):
    # Create the file name with the provided suffix
    base_name = os.path.basename(docx_path)
    json_name = f"{os.path.splitext(base_name)[0]}{suffix}"
    json_path = os.path.join(os.path.dirname(docx_path), json_name)

    # Write the data to a JSON file
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return json_path

def generate_numbered_todo_list_docx(text):
    response = cohere_client.generate(
        model='command-r-plus-08-2024',
        prompt=f'From the following text, generate a numbered list of To-Do items:\n\nText:\n{text}\n\nTo-Do List:\n1. ',
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

def save_numbered_todo_list_to_csv(todo_list, docx_path):
    base_name = os.path.basename(docx_path)
    csv_name = f"{os.path.splitext(base_name)[0]}_docx_todo_list.csv"
    csv_path = os.path.join(os.path.dirname(docx_path), csv_name)

    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["To-Do List"])
            for item in todo_list:
                writer.writerow([item])
    except Exception as e:
        return f"An error occurred while saving CSV file: {e}"

    return csv_path





def process_all_docx_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.docx'):
            docx_path = os.path.join(folder_path, file_name)
            docx_text = extract_text_from_docx(docx_path)

            # Extract CR details and save to JSON
            cr_details = extract_project_details_cr_dox(docx_text)
            cr_json_path = save_json_to_file(cr_details, docx_path)
            print(f"CR details saved to {cr_json_path}")

            # Generate and save To-Do list
            todo_list = generate_numbered_todo_list_docx(docx_text)
            csv_path = save_numbered_todo_list_to_csv(todo_list, docx_path)
            print(f"To-Do list saved to {csv_path}")
            









