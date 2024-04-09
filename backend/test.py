import os

# Function to read a file and return its contents
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception:
        return ""

# Function to write contents to a file
def write_to_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception:
        pass

# Function to traverse the folder and subfolders
def traverse_folder(folder_path, combined_content):
    # Loop through all files and folders in the current folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        # If the item is a folder, recursively traverse it
        if os.path.isdir(item_path) and not item.startswith("node_modules") and not item.startswith('migrations') and not item.startswith('.'):
            combined_content = traverse_folder(item_path, combined_content)
        # If the item is a file, read its contents and add them to the combined content
        elif os.path.isfile(item_path) and item_path.find("package-lock.json")==-1 and item_path.find("test.py") == -1:
            file_content = read_file(item_path)
            if file_content:
                combined_content += f"### {os.path.join(folder_path, item)} ###\n{file_content}\n\n"
    
    return combined_content

# Get the folder path from the user
folder_path = "."

# Initialize an empty string to store the combined contents
combined_content = ""
output_file_path = "codebase.txt"

# Traverse the folder and subfolders
combined_content = traverse_folder(folder_path, combined_content)
# Get the output file path from the user

# Write the combined content to the output file
#clear the file
write_to_file(output_file_path, "")
write_to_file(output_file_path, combined_content)

print("Files combined successfully!")