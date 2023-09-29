import random
from datetime import datetime, timedelta


class RandomDateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Calculate a random date within the past three months
        today = datetime.now()
        three_months_ago = today - timedelta(days=90)  # 90 days in 3 months
        random_date = three_months_ago + timedelta(days=random.randint(0, 90))

        # Add the random date to the context
        request.random_date = random_date

        response = self.get_response(request)
        return response
