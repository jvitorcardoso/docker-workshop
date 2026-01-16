from pathlib import Path

current_directory = Path.cwd()
current_file = Path(__file__).name

print(f"Files in the current directory ({current_directory}):")

for file in current_directory.iterdir():
    if file.name == current_file:
        continue

    print(f"    - {file.name}")

    if file.is_file():
        content = file.read_text(encoding='utf-8')
        print(f"Content: {content}\n")