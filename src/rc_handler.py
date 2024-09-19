# src/rc_files.py

import os
import shutil
import re
import streamlit as st
import zipfile
import io
def copy_r_files(source_dir, target_dir, keywords):
    os.makedirs(target_dir, exist_ok=True)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if any(keyword.lower() in file.lower() for keyword in keywords):
                file_path = os.path.join(root, file)
                destination_file_path = os.path.join(target_dir, file)

                if os.path.exists(destination_file_path):
                    file_name, file_extension = os.path.splitext(file)
                    new_file_name = f"{file_name}_2{file_extension}"
                    destination_file_path = os.path.join(target_dir, new_file_name)

                shutil.copy(file_path, destination_file_path)
                st.write(f"Copied {file_path} to {destination_file_path}")

def copy_rc_files(source_dir, target_dir):
    os.makedirs(target_dir, exist_ok=True)

    pattern = r'(^|[_\.\s])rc([_\.\s]|$)'
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if re.search(pattern, os.path.splitext(file)[0], re.IGNORECASE):
                file_path = os.path.join(root, file)
                destination_file_path = os.path.join(target_dir, file)

                if os.path.exists(destination_file_path):
                    file_name, file_extension = os.path.splitext(file)
                    new_file_name = f"{file_name}_2{file_extension}"
                    destination_file_path = os.path.join(target_dir, new_file_name)

                shutil.copy(file_path, destination_file_path)
                st.write(f"Copied {file_path} to {destination_file_path}")

def create_zip_from_folder(folder_path):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname)
    buffer.seek(0)
    return buffer
