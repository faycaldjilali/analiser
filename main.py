import os
import streamlit as st
from src.zip_extractor import save_uploaded_file, extract_zip, delete_zip_files
from src.rc_handler import copy_r_files, copy_rc_files, create_zip_from_folder
from src.pdfreader import extract_text_from_pdf, extract_project_details_cr_pdf, generate_numbered_todo_list_pdf, save_json_to_file, save_numbered_todo_list_to_csv 
from src.pdfreader import process_all_pdfs_in_folder
# Streamlit Interface for uploading ZIP files
st.title("ZIP File Processor with PDF LLM Extraction")

# Directory paths (you may adjust these based on your environment)
zip_file_location = "./uploaded_zips/"
unzip_file_location = "./unzipped_files/"
rc_file_location = "./rc_files/"

# Ensure folders exist
os.makedirs(zip_file_location, exist_ok=True)
os.makedirs(unzip_file_location, exist_ok=True)
os.makedirs(rc_file_location, exist_ok=True)

# Upload ZIP file using Streamlit's file uploader
uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

# Main application logic
if uploaded_file is not None:
    # Save uploaded ZIP file
    zip_file_path = save_uploaded_file(uploaded_file, zip_file_location)

    # Extract uploaded ZIP file
    extract_zip(zip_file_path, unzip_file_location)

    # Delete ZIP files after extraction
    delete_zip_files(unzip_file_location)

    # Copy specific files based on keywords (Règlement de la consultation)
    keywords = ["Règlement de la consultation", "Reglement de consultation"]
    copy_r_files(unzip_file_location, rc_file_location, keywords)

    # Copy files matching 'rc' pattern
    copy_rc_files(unzip_file_location, rc_file_location)

    st.success("File processing completed!")
    # Process PDFs in rc_files directory
    if os.path.exists(rc_file_location):
        process_all_pdfs_in_folder(rc_file_location)
        st.success("PDF files processed successfully!")
    # Process PDFs
    for root, dirs, files in os.walk(unzip_file_location):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                pdf_text = extract_text_from_pdf(pdf_path)

                # Extract CR details using LLM
                cr_details = extract_project_details_cr_pdf(pdf_text)
                cr_json_path = save_json_to_file(cr_details, pdf_path)
                st.write(f"CR details saved to {cr_json_path}")

                # Generate and save To-Do list using LLM
                todo_list = generate_numbered_todo_list_pdf(pdf_text)
                csv_path = save_numbered_todo_list_to_csv(todo_list, pdf_path)
                st.write(f"To-Do list saved to {csv_path}")

                # Optionally display the extracted data and To-Do list in the UI
                st.subheader(f"Extracted Details from {file}")
                st.json(cr_details)

                st.subheader(f"Generated To-Do List from {file}")
                st.write("\n".join(todo_list))

    # Create ZIP files for download
    unzip_zip_buffer = create_zip_from_folder(unzip_file_location)
    rc_zip_buffer = create_zip_from_folder(rc_file_location)

    st.download_button(
        label="Download Unzipped Files",
        data=unzip_zip_buffer,
        file_name="unzipped_files.zip",
        mime="application/zip"
    )

    st.download_button(
        label="Download RC Files",
        data=rc_zip_buffer,
        file_name="rc_files.zip",
        mime="application/zip"
    )
else:
    st.info("Please upload a ZIP file to begin processing.")

