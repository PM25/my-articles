import json
import hashlib
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from markdown import markdown


def get_formatted_date():
    today = date.today()
    return today.strftime("%Y-%m-%d")


def markdown_text_preview(path, kwords=50):
    with open(path, "r") as f:
        md = f.read()

    html = markdown(md)
    text = "".join(BeautifulSoup(html, "html.parser").findAll(text=True))
    preview_text = " ".join(text.split()[:kwords]) + "..."

    return preview_text


def calc_file_md5(fname):
    with open(fname, "rb") as f:
        data = f.read()
    file_md5 = hashlib.md5(data).hexdigest()

    return file_md5


def update_single_folder(folder_path):
    folder_path = Path(folder_path)
    assert folder_path.exists()

    Path("index").mkdir(parents=True, exist_ok=True)
    index_file = Path("index") / f"{folder_path}.json"
    minified_index_file = Path("index") / f"{folder_path}-minified.json"

    if index_file.exists():
        with open(index_file, "r") as f:
            index_data = json.load(f)
    else:
        index_data = {"sort-by-date": []}

    hash_file = Path("index") / "hash.json"
    if hash_file.exists():
        with open(hash_file, "r") as f:
            hash_data = json.load(f)
    else:
        hash_data = {}

    new_file, modified_file = [], []
    for fname in folder_path.glob("*.md"):
        name = fname.stem
        name = name.replace("-", " ")
        formatted_date = get_formatted_date()
        file_md5 = calc_file_md5(fname)

        if name not in index_data.keys():
            print(f"New file: {fname}")
            index_data[name] = {
                "path": str(fname.as_posix()),
                "created_date": formatted_date,
                "last_modified": formatted_date,
                "preview": markdown_text_preview(fname, kwords=50),
            }
            hash_data[name] = file_md5
            index_data["sort-by-date"].append(name)
            new_file.append(name)

        elif file_md5 != hash_data[name]:
            print(f"Modified file: {fname}")
            created_date = index_data[name]["created_date"]
            index_data[name] = {
                "path": str(fname.as_posix()),
                "created_date": created_date,
                "last_modified": formatted_date,
                "preview": markdown_text_preview(fname, kwords=50),
            }
            hash_data[name] = file_md5
            modified_file.append(name)

    if len(new_file) + len(modified_file) > 0:
        with open(index_file, "w") as f:
            json.dump(index_data, f, indent=4)

        with open(minified_index_file, "w") as f:
            json.dump(index_data, f, separators=(",", ":"))

        with open(hash_file, "w") as f:
            json.dump(hash_data, f, indent=4)

    print(f"Add {len(new_file)} new files.")
    print(f"Modified {len(modified_file)} files.")


def update_all():
    folders = [
        f
        for f in Path("./").iterdir()
        if f.is_dir() and f.name[0] != "." and f.stem != "index"
    ]
    for folder in folders:
        update_single_folder(folder)


if __name__ == "__main__":
    update_all()
