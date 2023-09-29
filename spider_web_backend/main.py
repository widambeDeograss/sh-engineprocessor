# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import requests
# from django.http import JsonResponse
# from django.views import View


class SearchView:
    def post(self, request, *args, **kwargs):
        # Get the user's search query from the request
        user_query = request

        # Prepare the prompt for the ChatGPT API
        prompt = f"User: {user_query}\nAI:"

        # Define API parameters
        api_url = "https://api.openai.com/v1/chat/completions"
        api_key = "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"

        # Make a request to the ChatGPT API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "system", "content": "You are a helpful assistant that provides search results."}, {"role": "user", "content": user_query}]
        }
        response = requests.post(api_url, headers=headers, json=data)

        # Get AI-generated response
        ai_response = response.json()

        # You can analyze the ai_response here to gather insights

        # Return AI-generated response to the user
        return ({"response": ai_response})


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')
    obl = SearchView()
    print(obl.post('data'))
    # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
