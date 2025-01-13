import hashlib
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from retrievers.abstract_retriever import AbstractRetriever


def get_webpage_title(content):
    soup = BeautifulSoup(content, "html.parser")
    title_tag = soup.title
    return title_tag.string if title_tag else "No Title"


def compute_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def fetch_webpage(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


class WebpageRetriever(AbstractRetriever):
    def __init__(self):
        super().__init__()

    def process(self):
        urls = os.environ["WEBPAGE_URLS"].split(",")
        for url in urls:
            url = url.strip()
            message = ""
            title = ""
            try:
                content = fetch_webpage(url)
                title = get_webpage_title(content)
                self.save_service.update_filename(f"{title}.txt")
                soup = BeautifulSoup(content, "html.parser")
                body_content = soup.body.get_text() if soup.body else ""
                new_hash = compute_hash(body_content)
                previous_hash = self.save_service.read()
                if previous_hash is None:
                    message = f"No previous hash found for {url}. Storing the current hash."
                    self.save_service.save(new_hash)
                elif new_hash != previous_hash:
                    message = f"The webpage has changed! {url}"
                    self.save_service.save(new_hash)
                else:
                    message = f"The webpage has not changed: {url}"
            except Exception as e:
                message = f"An error occurred with {url}: {e}"
            finally:
                self.create_response([title, message])

    def create_response(self, value):
        title, message = value
        if (
            "M.O.D.A" in title
            and "not" in message
            and datetime.today().weekday() == 0
            and datetime.today().hour == 10
            and datetime.today().minute == 20
        ):
            self.notification_service.send_message(title, message)
