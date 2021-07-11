import json
import shutil
from pathlib import Path

from code.utils import load_json


def update_all():
    index_file = "index.json"
    index_data = load_json(index_file, {})

    meta_folder = Path("index") / "meta"
    shutil.rmtree(meta_folder)
    meta_folder.mkdir(parents=True, exist_ok=True)

    for title_name, data in index_data.items():
        title_name = title_name.replace(" ", "-")
        out_path = meta_folder / f"{title_name}.json"

        with open(out_path, "w") as f:
            json.dump(data, f, indent=4)

    print(f"Save total of {len(index_data)} files.")


if __name__ == "__main__":
    print("[Update Meta]")
    update_all()
