import os

def delete_files_with_same_size(directory):
    file_sizes = {}
    files_to_delete = set()

    # Iterate over files in the directory
    for file_name in os.listdir(directory):
        if file_name.lower().endswith('.pdf'):
            file_path = os.path.join(directory, file_name)
            try:
                # Get file size
                size = os.path.getsize(file_path)

                # Check if this size is already seen
                if size in file_sizes:
                    # If size is the same, add the new file to delete list
                    files_to_delete.add(file_path)
                else:
                    # If size is not seen, add the existing file to delete list
                    if file_sizes.get(size):
                        files_to_delete.add(file_sizes[size])
                    file_sizes[size] = file_path

            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    # Delete files
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
