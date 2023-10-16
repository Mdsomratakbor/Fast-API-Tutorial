from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel

import requests
import json
 
# Create the FastAPI app
app= FastAPI()

class Person(BaseModel):
    name: str
    age: int

infos = {
    1: {
        "name": "John",
        "age": 20
    },
    2: {
        "name": "Jane",
        "age": 25
    },
    3: {
        "name": "Bob",
        "age": 30
    },
    4: {
        "name": "Alice",
        "age": 35
    }
}

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/about")
def home():
    return {"about": "This is a simple API created using FastAPI"}

@app.get("/get-info/{id}")

def get_info(id: int ):
    return infos[id]


@app.get("/get-by-name")
def get_name(name: str):
    for i in infos:
        if infos[i]["name"] == name:
            return infos[i]
    raise HTTPException(status_code=404, detail="Name not found")


@app.post("/create-info")
def create_info(person_id: int, person: Person):
    if person_id in person:
        return {"Error": "Person already exists"}
    
    infos[person_id] = person
    return infos[person_id]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)
# run the app with uvicorn
# uvicorn main:app --reload



subdomain = "scienceoncall"
# Define your account details and endpoint
email = 'ken@scienceoncall.com'
api_token = 'WsFCkilvqpvIZgcEECaiQs76eiHUtU5RoJADbNt0'  # Replace with your actual API token
endpoint_1 = f'https://{subdomain}.zendesk.com/api/v2/search.json?query=gget,online_ordering__pause_online_ordering'
endpoint_2 = f'https://{subdomain}.zendesk.com/api/v2/search.json?query=gget,networking__outage'
endpoint_3 = f'https://{subdomain}.zendesk.com/api/v2/search.json?query=gget,toast,printer'
 
# Set up the HTTP basic authentication
auth = (f'{email}/token', api_token)
 
@ app.get("/get-tickets")
def get_tickets():
    # Make the HTTP GET request to the Zendesk API
    response = requests.get(endpoint_3, auth=auth)
    # Check for a valid response
    if response.status_code != 200:
        print(f'Failed to retrieve tickets: {response.content}')
        return None
    # Parse the JSON response
    tickets_data = response.json()
    return tickets_data
 
# if __name__ == '__main__':
#     tickets = get_tickets()
#     if tickets:
#         print(json.dumps(tickets, indent=2))