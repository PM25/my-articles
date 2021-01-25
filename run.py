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
    return " ".join(text.split()[:50])


def update(lst, save_name):
    folders = [f for f in Path("./").iterdir() if f.is_dir() and f.name[0] != "."]
    names = [item["name"] for item in lst]
    updated_files = []
    for folder in folders:
        for path in folder.glob("*.md"):
            name = path.stem
            name = " ".join(name.split("-"))
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


fname = "list.json"
if __name__ == "__main__":
    if Path(fname).exists():
        with open("list.json", "r") as infile:
            try:
                lst = json.load(infile)
                update(lst, fname)
            except:
                print("*Broken file")
    else:
        update([], fname)
