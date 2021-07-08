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
    return today.strftime("%Y-%m-%d-%H-%M-%S")


def markdown_text_preview(path, kwords=50):
    with open(path, "r") as f:
        md = f.read()

    html = markdown(md)
    text = "".join(BeautifulSoup(html, "html.parser").findAll(text=True))
    preview_text = " ".join(text.split()[:kwords]) + "..."

    return preview_text
