import os
import json

# 👇 Change these to your actual paths
ROOT_DIR = r"C:\Users\Owner\Desktop\System-Prompts\system-prompts-and-models-of-ai-tools-main"
OUTPUT_FILE = r"C:\Users\Owner\Desktop\System-Prompts\system-prompts-and-models-of-ai-tools-main\mega_schema.json"

# Only include these extensions
VALID_EXTENSIONS = {".md", ".txt", ".json"}


def collect_files(root, extensions):
    """Recursively yield file paths matching extensions."""
    for dirpath, _, filenames in os.walk(root):
        for file in filenames:
            if any(file.lower().endswith(ext) for ext in extensions):
                yield os.path.join(dirpath, file)


def build_schema(root_dir):
    """Build schema { IDE: { system_prompts: { file_name: content } } }"""
    schema = {}

    for filepath in collect_files(root_dir, VALID_EXTENSIONS):
        # Relative path (to preserve folder structure inside each IDE)
        rel_path = os.path.relpath(filepath, start=root_dir)
        parts = rel_path.split(os.sep)

        ide_name = parts[0]             # IDE folder (e.g. Bolt, Cline, etc.)
        file_name = "/".join(parts[1:]) # Subfolder/file name

        if ide_name not in schema:
            schema[ide_name] = {"system_prompts": {}}

        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            schema[ide_name]["system_prompts"][file_name] = content
        except Exception as e:
            schema[ide_name]["system_prompts"][file_name] = f"[Error reading {filepath}: {e}]"

    return schema


if __name__ == "__main__":
    print(f"🔍 Scanning: {ROOT_DIR}")
    schema = build_schema(ROOT_DIR)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        json.dump(schema, outfile, indent=2, ensure_ascii=False)

    print(f"✅ JSON schema written to: {OUTPUT_FILE}")
