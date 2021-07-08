import json
from pathlib import Path

from code.utils import (
    get_formatted_today_date,
    calc_file_md5,
    load_json,
    markdown_text_preview,
)


def update_single_folder(index_data, folder_path, markdown_max_char=250):
    print(f"[{folder_path}]")
    folder_path = Path(folder_path)
    assert folder_path.exists()

    new_file, modified_file = [], []
    for fname in folder_path.glob("*.md"):
        name = fname.stem
        name = name.replace("-", " ")
        formatted_date = get_formatted_today_date()
        file_md5 = calc_file_md5(fname)

        if name not in index_data.keys():
            print(f"New file: {fname.name}")
            index_data[name] = {
                "title": name,
                "file_name": str(fname.name),
                "folder": str(folder_path.as_posix()),
                "path": str(fname.as_posix()),
                "created_date": formatted_date,
                "last_modified": formatted_date,
                "preview": markdown_text_preview(fname, max_char=markdown_max_char),
                "md5": file_md5,
            }
            new_file.append(name)

        elif file_md5 != index_data[name]["md5"]:
            print(f"Modified file: {fname.name}")
            created_date = index_data[name]["created_date"]
            index_data[name] = {
                "title": name,
                "file_name": str(fname.name),
                "folder": str(folder_path.as_posix()),
                "path": str(fname.as_posix()),
                "created_date": created_date,
                "last_modified": formatted_date,
                "preview": markdown_text_preview(fname, max_char=markdown_max_char),
                "md5": file_md5,
            }
            modified_file.append(name)

    print(f"- Add {len(new_file)} new files.")
    print(f"- Modified {len(modified_file)} files.")
    print("=" * 25)

    return index_data, new_file, modified_file


def update_all(article_folder="articles"):
    index_file = "index.json"
    index_data = load_json(index_file, {})
    new_files, modified_files = [], []

    folders = [f for f in Path(article_folder).iterdir() if f.is_dir()]
    for folder in folders:
        index_data, new_file, modified_file = update_single_folder(index_data, folder)
        new_files.extend(new_file)
        modified_files.extend(modified_file)

    print("[All folders]")
    print(f"Add {len(new_files)} new files.")
    print(f"Modified {len(modified_files)} files.")
    print("=" * 25)

    if len(new_files) + len(modified_files) > 0:
        with open(index_file, "w") as f:
            json.dump(index_data, f, indent=4)
        print("> Updated Index Successfully")
    else:
        print("> No file is modified or added, skipping update index")

    return new_files, modified_files


if __name__ == "__main__":
    print("[Update Index]")
    update_all()
