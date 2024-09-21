import os
import PyPDF2
import json
import csv
import cohere
import streamlit as st 
# Initialize Cohere client
cohere_client = cohere.Client('IdlHWXxZ6LEt90RvFKvXKv4CYzrR8BCQLq63yriI')

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
    response = cohere_client.generate(
        model='command-r-plus-08-2024',
        prompt= f"Extract following detailed information from the text:\n"
               f"1. Nom du projet\n"
               f"2. Numéro du RC\n"
               f"3. Description\n"
               f"4. Date limite de soumission\n"
               f"5. Adresse\n"
               f"6. Visites obligatoires \n"
               f"7. Objet de la consultation  \n"
               f"8. Votre lot :  \n"
               f"9. Durée des marchés:\n"
               f"10. Contact de l'acheteur (Nom, Titre, Téléphone, Courriel)\n"
               f"11. Acheteur : \n\n"
               f"Synthèse des éléments pertinents :\n"
               f"2.Actions à prendre par SEF (Stores et Fermetures) :\n"
               f"Extract the following detailed information from the text::\n"
               f"Text:\n{text}",

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
    response = cohere_client.generate(
        model='command-r-plus-08-2024',
        prompt=f'From the following text, generate a numbered list of To-Do items:\n\nText:\n{text}\n\nTo-Do List:\n1. ',
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

                # Optionally display the extracted data and To-Do list in the UI
            st.subheader(f"Extracted Details from {file_name}")
            st.json(cr_details)

            st.subheader(f"Generated To-Do List from {file_name}")
            st.write("\n".join(todo_list))
