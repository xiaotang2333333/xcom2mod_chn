import os

def convert_encoding_and_rename(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            # Only process files (skip directories)
            if os.path.isfile(file_path):
                # Read with utf-16le
                with open(file_path, 'r', encoding='utf-16le', errors='ignore') as f:
                    content = f.read()
                # Write with utf-8 and change extension to .txt
                new_file = os.path.splitext(file_path)[0] + '.txt'
                with open(new_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                # Optionally, remove the old file
                os.remove(file_path)

if __name__ == "__main__":
    for folder in ['CHN', 'INT']:
        if os.path.isdir(folder):
            convert_encoding_and_rename(folder)