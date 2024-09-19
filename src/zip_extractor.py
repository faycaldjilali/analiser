
import os
import zipfile
import streamlit as st

def save_uploaded_file(uploaded_file, zip_file_location):
    file_path = os.path.join(zip_file_location, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def extract_zip(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        st.write(f"Extracted: {zip_path} to {extract_to}")

        # Recursively extract nested ZIP files
        for root, dirs, files in os.walk(extract_to):
            for file in files:
                if file.endswith('.zip'):
                    file_path = os.path.join(root, file)
                    st.write(f"Found sub-ZIP file: {file_path}")
                    sub_extract_to = os.path.join(extract_to, os.path.splitext(file)[0])
                    extract_zip(file_path, sub_extract_to)
    except zipfile.BadZipFile:
        st.error(f"Error: '{zip_path}' is not a valid ZIP file or it is corrupted.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def delete_zip_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".zip"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                st.write(f"Deleted: {file_path}")
