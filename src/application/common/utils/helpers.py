import logging
import re

from typing import List

import pandas as pd
import requests
from RPA.Browser.Selenium import By

from src.application.common.models.post import Post
from src.application.common.utils.locators import Locators

from datetime import datetime, timedelta

from openpyxl.utils import get_column_letter


class Helper:
    @staticmethod
    def search_text(search_text, title, description):
        total_count = title.count(search_text) + description.count(search_text)

        return total_count

    @staticmethod
    def has_money(title, description):
        pattern = r"^(\$?\d{1,3}(?:,?\d{3})*(?:\.\d{1,2})?|(?:\d+ (?:dollars|USD)))$"

        return bool(re.match(pattern, title)) or bool(re.match(pattern, description))

    @staticmethod
    def excel_generator(posts: List[Post], filename: str = "posts.xlsx") -> None:
        try:
            logging.info("...BUILDING EXCEL...")
            data = [
                {
                    "Title": post.title,
                    "Description": post.description,
                    "Date": post.date,
                    "Search Phrase Total": post.search_text_total,
                    "Has Money": post.has_money,
                }
                for post in posts
            ]
    
            df = pd.DataFrame(data)
            filepath = f'./output/{filename}'
            df.to_excel(filepath, index=False)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')

                worksheet = writer.sheets['Sheet1']

                # Ajusta a largura das colunas
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = get_column_letter(column[0].column)  # Obter a letra da coluna

                    # Itera pelas células da coluna para encontrar o comprimento máximo
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    # Define a largura da coluna
                    adjusted_width = max_length + 2  # Adiciona um buffer
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
        except Exception as ex:
            logging.error("...BUILDING EXCEL...")

    @staticmethod
    def convert_to_datetime(date_str):
        if 'yesterday' in date_str:
            return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        to_find = ['min', 'mins', 'hour', 'hours']
        today_post = False
        for str in to_find:
            today_post = str in date_str
            if today_post:
                return datetime.now().strftime('%Y-%m-%d')
        else:
            if Helper.check_dateformat(date_str) :
                return date_str
            
            date_str = date_str.split(",")
            year = None

            if date_str.count() > 1:
                year = date_str[1]

            if year is None:
                year = datetime.now().year

            date = f"{date_str} {year}"
            date = date.strip()
            date_obj = datetime.strptime(date, "%b %d %Y")
            formatted_datetime = date_obj.strftime("%Y-%m-%d")

        return formatted_datetime

    @staticmethod
    def get_image(post, title):
        try:
            logging.info(f"...GET IMAGE FROM POST: {title}")
            img_available = post.find_element(By.XPATH, Locators.POST_IMG)
            if img_available:
                image = img_available.get_attribute("src")
                image_url = image.split(".jpg")[0] + ".jpg"
                filename = Helper.filename(title)
                with open(f"output/{filename}", "wb") as file:
                    file.write(requests.get(image_url).content)

                return filename
            else:
                return None
            
        except:
            logging.info("...ERROR GETTING IMAGE...")

    @staticmethod
    def filename(text, extension=".jpg"):
        filename = re.sub(r"[^\w\s]", "", text).replace(" ", "_").strip().lower()

        return filename + extension
    
    @staticmethod
    def check_dateformat(date_str):
        return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date_str))
