import logging
import re
from collections import Counter
from datetime import datetime, timedelta
from typing import List

import pandas as pd
import requests
from openpyxl.utils import get_column_letter
from RPA.Browser.Selenium import By

from src.application.common.models.post import Post
from src.application.common.utils.locators import Locators


class Helper:
    @staticmethod
    def search_text(search_text, title, description):
        try:
            text = title + " " + description
            words = re.findall(r"\b\w+\b", text.lower())
            words_counter = Counter(words)

            search_words = search_text.split(" ")
            total_occurrences = 0
            for search_word in search_words:
                if len(search_word) > 1:
                    total_occurrences += words_counter[search_word.lower()]

            return total_occurrences
        except:
            logging.error(f"... ERROR SEARCHING WORDS OCCURRENCES ...")

    @staticmethod
    def has_money(title, description):
        pattern = r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)|\b(\d+)\s*(?:dollars|USD)\b"

        return bool(re.findall(pattern, title)) or bool(
            re.findall(pattern, description)
        )

    @staticmethod
    def excel_generator(posts: List[Post]) -> None:
        try:
            logging.info("... BUILDING EXCEL FILE 📝 ...")
            data = [
                {
                    "Title": post.title,
                    "Description": post.description,
                    "Date": post.date,
                    "Search Phrase Total": post.search_text_total,
                    "Has Money": str(post.has_money),
                }
                for post in posts
            ]

            df = pd.DataFrame(data)
            filename = "posts-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".xlsx"
            filepath = f"./output/{filename}"
            df.to_excel(filepath, index=False)

            with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Sheet1")

                worksheet = writer.sheets["Sheet1"]

                for column in worksheet.columns:
                    max_length = 0
                    column_letter = get_column_letter(column[0].column)

                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass

                    adjusted_width = max_length + 2
                    worksheet.column_dimensions[column_letter].width = adjusted_width

            logging.info("... EXCEL FILE BUILT 🗳️ ...")

        except Exception as ex:
            logging.error("... ERROR BUILDING EXCEL FILE 😢...")

    @staticmethod
    def convert_to_datetime(date_str):
        try:
            if "yesterday" in date_str.lower():
                return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

            to_find = ["min", "mins", "hour", "hours"]
            today_post = False
            for str in to_find:
                today_post = str in date_str
                if today_post:
                    return datetime.now().strftime("%Y-%m-%d")
            else:
                if Helper.check_dateformat(date_str):
                    return date_str

                date_str = date_str.split(",")
                year = None

                if len(date_str) > 1:
                    year = date_str[1]

                if year is None:
                    year = datetime.now().year

                date = f"{date_str[0]} {year}"
                date = date.strip().lower()
                date_obj = datetime.strptime(date, "%B %d %Y")
                formatted_datetime = date_obj.strftime("%Y-%m-%d")

            return formatted_datetime
        except:
            logging.error(f"... ERROR CONVERTING POST DATE - DATE_STR: {date_str} ...")

    @staticmethod
    def get_image(post, title):
        try:
            logging.info(f"... GET IMAGE FROM POST - TITLE: {title} ...")
            img_available = post.find_element(By.CLASS_NAME, Locators.POST_IMG)
            if img_available:
                image_url = img_available.get_attribute("src")
                filename = Helper.filename(title)
                with open(f"output/{filename}", "wb") as file:
                    file.write(requests.get(image_url).content)

                return filename
            else:
                return None

        except:
            logging.error(f"... UNABLE TO GET IMAGE FROM POST - TITLE: {title} ...")

    @staticmethod
    def filename(text, extension=".jpg"):
        filename = re.sub(r"[^\w\s]", "", text).replace(" ", "_").strip().lower()

        return filename + extension

    @staticmethod
    def check_dateformat(date_str):
        return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date_str))
