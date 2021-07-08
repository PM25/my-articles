import json
import hashlib
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from markdown import markdown


def calc_file_md5(fname):
    with open(fname, "rb") as f:
        data = f.read()
    file_md5 = hashlib.md5(data).hexdigest()

    return file_md5


def load_json(fname, default=None):
    if Path(fname).exists():
        with open(fname, "r") as f:
            data = json.load(f)
    else:
        data = default

    return data


def get_formatted_today_date():
    today = datetime.now()
    return today.strftime("%Y/%m/%d %H:%M:%S")


def markdown_text_preview(path, max_char=100):
    with open(path, "r") as f:
        md = f.read()

    html = markdown(md)
    # text = "".join(BeautifulSoup(html, "html.parser").findAll(text=True))
    text = ""
    for element in BeautifulSoup(html, "html.parser").findAll("p"):
        text += "".join(element.findAll(text=True))

    curr_text_len = 0
    preview_text = ""
    for word in text.split():
        if curr_text_len + len(word) > max_char:
            break

        preview_text += word + " "
        curr_text_len += len(word) + 1

    preview_text = preview_text[:-1] + "..."

    return preview_text


if __name__ == "__main__":
    preview_text = markdown_text_preview(
        "Computer-Science/A-Survey-of-Mixup-Based-Data-Augmentation-Strategies.md", 250,
    )
    print(len(preview_text))
    print(preview_text)
