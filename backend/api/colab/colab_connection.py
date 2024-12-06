import requests

# Django API URL
django_url = "http://127.0.0.1:8000/api/generate_explanation_colab/"

# Send POST request to Django
response = requests.post(django_url)

# Print the response from Django
if response.status_code == 200:
    print("Response from Django:", response.json())
else:
    print("Error:", response.status_code, response.text)
