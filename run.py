import json
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from markdown import markdown


def formatted_date():
    today = date.today()
    return today.strftime("%Y-%m-%d")


def markdown_path_preview(path, kwords=50):
    with open(path, "r") as f:
        md = f.read()
    return markdown_preview(md, kwords)


def markdown_preview(md, kwords):
    html = markdown(md)
    text = "".join(BeautifulSoup(html, "html.parser").findAll(text=True))
    return " ".join(text.split()[:50]) + "..."


def update_list(lst, save_name):
    folders = [f for f in Path("./").iterdir() if f.is_dir() and f.name[0] != "."]
    names = [item["name"] for item in lst]
    updated_files = []
    for folder in folders:
        for path in folder.glob("*.md"):
            name = path.stem
            name = name.replace("-", " ")
            if name not in names:
                lst.insert(
                    0,
                    {
                        "name": name,
                        "path": str(path.as_posix()),
                        "date": formatted_date(),
                        "preview": markdown_path_preview(path, 50),
                    },
                )
                updated_files.append(name)
    with open(save_name, "w") as ofile:
        json.dump(lst, ofile, indent=4)

    print(f"Updated {len(updated_files)} Files: {updated_files}")
    print("*Update Complete!")


def update_dict(dic, save_name):
    folders = [f for f in Path("./").iterdir() if f.is_dir() and f.name[0] != "."]
    updated_files = []
    for folder in folders:
        for path in folder.glob("*.md"):
            name = path.stem
            name = " ".join(name.split("-"))
            if name not in dic.keys():
                dic[name] = {
                    "name": name,
                    "path": str(path.as_posix()),
                    "date": formatted_date(),
                    "preview": markdown_path_preview(path, 50),
                }
                updated_files.append(name)

    with open(save_name, "w") as ofile:
        json.dump(dic, ofile, indent=4)

    print(f"Updated {len(updated_files)} Files: {updated_files}")
    print("*Update Complete!")


def update(fname, target="list"):
    print("-" * 5)
    print(f"*Updating {fname}")
    if Path(fname).exists():
        infile = open(fname, "r")
        try:
            jsn = json.load(infile)
            if target == "list":
                update_list(jsn, fname)
            elif target == "dict":
                update_dict(jsn, fname)
        except:
            print("*Broken file")
    else:
        if target == "list":
            update_list([], fname)
        elif target == "dict":
            update_dict({}, fname)


lfname = "list.json"
dfname = "dict.json"
if __name__ == "__main__":
    update(lfname, "list")
    update(dfname, "dict")
