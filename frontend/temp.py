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

# Function to check if a directory is blacklisted
def is_blacklisted(directory):
    blacklist = ["node_modules", "__pycache__", ".venv",".next"]
    return any(blacklisted_dir in directory for blacklisted_dir in blacklist)

# Function to traverse the subdirectories and merge file contents
def traverse_subdirectories(subdirectories, output_file_path):
    combined_content = ""

    for subdir in subdirectories:
        if os.path.isdir(subdir):
            for root, dirs, files in os.walk(subdir):
                # Skip blacklisted directories
                dirs[:] = [d for d in dirs if not is_blacklisted(d)]

                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path.find("package-lock.json") == -1 and file_path.find("test.py") == -1:
                        file_content = read_file(file_path)
                        if file_content:
                            combined_content += f"### {file_path} ###\n{file_content}\n\n"

    # Write the combined content to the output file
    write_to_file(output_file_path, "")  # Clear the file
    write_to_file(output_file_path, combined_content)

    print("Files merged successfully!")

# List of subdirectories to traverse
subdirectories = ["/home/oohben/aiLingo/frontend/ailingo"]

# Output file path
output_file_path = "merged_files.txt"

# Traverse the subdirectories and merge file contents
traverse_subdirectories(subdirectories, output_file_path)