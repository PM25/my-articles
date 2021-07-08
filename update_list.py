import json
from pathlib import Path

from utils import load_json


def update_single_folder(data, folder, k=10):
    print(f"[{folder}]")
    out_folder = Path("index") / folder
    out_folder.mkdir(parents=True, exist_ok=True)

    out = []
    for datum in data:
        out.append(
            {
                "name": datum["title"],
                "created_date": datum["created_date"],
                "preview": datum["preview"],
            }
        )

    out = sorted(out, key=lambda d: d["created_date"])

    # split "out" by each part has at most k element
    for idx in range((len(out) - 1) // k + 1):
        fname = out_folder / f"list_{idx}.json"
        out_slice = out[idx * k : min((idx + 1) * k, len(out))]

        with open(fname, "w") as f:
            json.dump(out_slice, f, indent=4)

    print("=" * 25)


def update_all():
    index_file = "index.json"
    index_data = load_json(index_file, {})

    folders = {}
    for title_name, data in index_data.items():
        folder = data["folder"]
        data["title"] = title_name

        if folder not in folders:
            folders[folder] = []

        folders[folder].append(data)

    for folder, data in folders.items():
        update_single_folder(data, folder)


if __name__ == "__main__":
    update_all()
