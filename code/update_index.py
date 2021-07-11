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

    updated_index_data = []
    new_file, modified_file = [], []

    for fpath in folder_path.glob("*.md"):
        fname = fpath.stem
        title = fname.replace("-", " ")
        title = title.replace("_", "-")
        formatted_date = get_formatted_today_date()
        file_md5 = calc_file_md5(fpath)

        if fname not in index_data.keys():
            print(f"New file: {fname}")
            index_data[fname] = {
                "title": title,
                "file_name": str(fpath.name),
                "folder": str(folder_path.as_posix()),
                "path": str(fpath.as_posix()),
                "created_date": formatted_date,
                "last_modified": formatted_date,
                "preview": markdown_text_preview(fpath, max_char=markdown_max_char),
                "md5": file_md5,
            }
            new_file.append(fname)

        elif file_md5 != index_data[fname]["md5"]:
            print(f"Modified file: {fname}")
            created_date = index_data[fname]["created_date"]
            index_data[fname] = {
                "title": title,
                "file_name": str(fpath.name),
                "folder": str(folder_path.as_posix()),
                "path": str(fpath.as_posix()),
                "created_date": created_date,
                "last_modified": formatted_date,
                "preview": markdown_text_preview(fpath, max_char=markdown_max_char),
                "md5": file_md5,
            }
            modified_file.append(fname)

        updated_index_data.append((fname, index_data[fname]))

    print(f"- Add {len(new_file)} new files.")
    print(f"- Modified {len(modified_file)} files.")
    print("=" * 25)

    return updated_index_data, new_file, modified_file


def get_deleted_files(index_data, updated_index_data):
    original_index = set(index_data.keys())
    updated_index = set(updated_index_data.keys())
    deleted_files = original_index.difference(updated_index)

    return deleted_files


def update_all(article_folder="articles"):
    index_file = "index.json"
    index_data = load_json(index_file, {})
    new_files, modified_files = [], []
    updated_index_data = []

    folders = [f for f in Path(article_folder).iterdir() if f.is_dir()]
    for folder in folders:
        updated_data, new_file, modified_file = update_single_folder(index_data, folder)
        new_files.extend(new_file)
        modified_files.extend(modified_file)
        updated_index_data.extend(updated_data)

    updated_index_data = dict(updated_index_data)
    deleted_files = get_deleted_files(index_data, updated_index_data)

    print("[All folders]")
    print(f"Add {len(new_files)} new files.")
    print(f"Modified {len(modified_files)} files.")
    print(f"Deleted {len(deleted_files)} files.")
    print("=" * 25)

    if len(new_files) + len(modified_files) + len(deleted_files) > 0:
        updated_index_data = dict(updated_index_data)
        with open(index_file, "w") as f:
            json.dump(updated_index_data, f, indent=4)
        print("> Updated Index Successfully")
    else:
        print("> No file is modified or added, skipping update index")

    return new_files, modified_files, deleted_files


if __name__ == "__main__":
    print("[Update Index]")
    update_all()
