import json
from pathlib import Path
from datetime import datetime

from code.utils import load_json


def update_single_folder(data, folder, k=10):
    print(f"[{folder}]")
    out_folder = Path("index") / folder
    out_folder.mkdir(parents=True, exist_ok=True)

    data = sorted(data, key=lambda d: d["created_date"], reverse=True)

    out = []
    for datum in data:
        created_time = datum["created_date"]
        date_time_obj = datetime.strptime(created_time, "%Y/%m/%d %H:%M:%S")
        created_date = date_time_obj.strftime("%Y/%m/%d")
        out.append(
            {
                "name": datum["title"],
                "created_date": created_date,
                "preview": datum["preview"],
            }
        )

    # split "out" by each part has at most k element
    num_split = (len(out) - 1) // k + 1
    for idx in range(num_split):
        fname = out_folder / f"list_{idx}.json"
        out_slice = out[idx * k : min((idx + 1) * k, len(out))]

        with open(fname, "w") as f:
            json.dump(out_slice, f, indent=4)

    with open(out_folder / "meta.json", "w") as f:
        json.dump({"num_files": num_split}, f, indent=4)

    print(f"- Save total of {len(out)} articles to {num_split} files.")
    print(f"- Files: list_0.json ~ list_{num_split-1}.json")
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
        update_single_folder(data, Path(folder).stem)


if __name__ == "__main__":
    print("[Update List]")
    update_all()
