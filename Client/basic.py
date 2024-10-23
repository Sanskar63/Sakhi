import requests


# endpoint = "http://127.0.0.1:8000/doctors/categories"
# endpoint = "http://127.0.0.1:8000/doctors/all/"
endpoint = "http://127.0.0.1:8000/doctors/1/"


# get_response = requests.get(endpoint) # This is without location
# get_response = requests.get(endpoint, params={"location": "Una"}) #This is with location
get_response = requests.get(endpoint)

# print(get_response.text) #Print raw text response
# print(get_response.status_code)
# print(get_response.json()) #get json response sent from endpoint
print(get_response.json())