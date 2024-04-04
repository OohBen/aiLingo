import os

def merge_text_files(folder_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as output:
        for root, dirs, files in os.walk(folder_path):
            if 'node_modules' in dirs:
                dirs.remove('node_modules')  # Skip 'node_modules' folder
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as input_file:
                        content = input_file.read()
                        output.write(f"------------------------\n")
                        output.write(f"File: {file_path}\n")
                        output.write(f"------------------------\n")
                        output.write(content)
                        output.write("\n\n")
                except (UnicodeDecodeError, PermissionError, IOError):
                    print(f"Skipping unreadable file: {file_path}")
                    continue

# Example usage
folder_path = "ailingo-frontend\\src"
output_file = "merged_text_files.txt"
merge_text_files(folder_path, output_file)