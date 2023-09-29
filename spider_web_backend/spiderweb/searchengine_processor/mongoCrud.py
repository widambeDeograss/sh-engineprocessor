import pymongo
from datetime import datetime, timedelta
import random


class MongoDB:
    def __init__(self):
        self.myClient = pymongo.MongoClient("mongodb://localhost:27017/", connect=False)
        self.db = self.myClient["spiderWeb"]


    def generate_dates(self):
        today = datetime.now()
        three_months_ago = today - timedelta(days=90)  # 90 days in 3 months
        random_date = three_months_ago + timedelta(days=random.randint(0, 90))

        # Add the random date to the context
        random_date = random_date
        return random_date

    def get_contents(self, collection, search_word):
        data = self.db[collection]
        results = []
        for item in data.find({"$text": {"$search": search_word}}):
            item.pop('_id')
            item['reference_date'] = self.generate_dates()
            results.append(item)
        return results

    def get_keywords(self, collection, search_word):
        data = self.db[collection]
        results = []
        for item in data.find({"$text": {"$search": search_word}}):
            item.pop('_id')
            item['reference_date'] = self.generate_dates()
            results.append(item)
        return results

    def get_pdfs(self, collection, search_word):
        pdf_data = self.db[collection]
        pdf_results = []
        for item in pdf_data.find({"$text": {"$search": search_word}}):
            item.pop('_id')
            item['reference_date'] = self.generate_dates()
            pdf_results.append(item)
        return pdf_results

    def get_image(self, collection, search_word):
        data = self.db[collection]
        results = []
        for item in data.find({"$text": {"$search": search_word}}):
            item.pop('_id')
            item['reference_date'] = self.generate_dates()
            results.append(item)
        return results


# obj = MongoDB()
# print(obj.get_contents('contents', 'd'))