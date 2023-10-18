from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
import csv
import requests
import json
 
# Create the FastAPI app
app= FastAPI()




subdomain = "scienceoncall"
# Define your account details and endpoint
email = 'ken@scienceoncall.com'
api_token = 'WsFCkilvqpvIZgcEECaiQs76eiHUtU5RoJADbNt0'  # Replace with your actual API token
endpoint_1 = f'https://{subdomain}.zendesk.com/api/v2/search.json?query=gget,online_ordering__pause_online_ordering'
endpoint_2 = f'https://{subdomain}.zendesk.com/api/v2/search.json?query=gget,networking__outage'
endpoint_3 = f'https://{subdomain}.zendesk.com/api/v2/search.json?query=gget,toast,printer'
 
# Set up the HTTP basic authentication
auth = (f'{email}/token', api_token)
 
@ app.get("/get-tickets-others")
def get_tickets_others():
    # Make the HTTP GET request to the Zendesk API
    response = requests.get(endpoint_3, auth=auth)
    # Check for a valid response
    if response.status_code != 200:
        print(f'Failed to retrieve tickets: {response.content}')
        return None
    # Parse the JSON response
    tickets_data = response.json()
    convert_csv(tickets_data, "others_outout.csv")
    return tickets_data

@ app.get("/get-tickets-networking")
def get_tickets_networking():
    # Make the HTTP GET request to the Zendesk API
    response = requests.get(endpoint_2, auth=auth)
    # Check for a valid response
    if response.status_code != 200:
        print(f'Failed to retrieve tickets: {response.content}')
        return None
    # Parse the JSON response
    tickets_data = response.json()
    convert_csv(tickets_data, "networking_outout.csv")
    return tickets_data
 
 
@ app.get("/get-tickets-ordering")
def get_tickets_ordering():
    # Make the HTTP GET request to the Zendesk API
    response = requests.get(endpoint_1, auth=auth)
    # Check for a valid response
    if response.status_code != 200:
        print(f'Failed to retrieve tickets: {response.content}')
        return None
    # Parse the JSON response
    tickets_data = response.json()
    # print(json.dumps(tickets_data, indent=2))
    convert_csv(tickets_data, "ordering_outout.csv")
    return tickets_data
# if __name__ == '__main__':
#     tickets = get_tickets_ordering()
#     if tickets:
#         print(json.dumps(tickets, indent=2))




# Define custom labels for the CSV columns
field_names = ["ticket_id", "subject", "description", "tags"]

def convert_csv(json_data, file_name):
    # Open a CSV file for writing
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)

        # Write the header row with custom labels
        writer.writeheader()

        # Write the data from the JSON object
        for item in json_data["results"]:
            # Map the JSON keys to custom labels for the CSV file
            custom_row = {
                 "ticket_id": item["id"],
                 "subject": item["subject"],
                 "description": item["description"],
                 "tags": ", ".join(item["tags"])
            }
            writer.writerow(custom_row)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)
# run the app with uvicorn
# uvicorn main:app --reload
