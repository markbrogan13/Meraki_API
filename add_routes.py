'''
This is a sample API script that serves as a very basic intro to using the Meraki Dashboard API
directly with the requests library.
Written by Josh Corlin - 20230222

Warning:
- This is a very basic script that doesn't really have a real world purpose, in fact, it demonstrates a number of
  bad practices.  This should only be used as a basic API intro exercise.

Goal:
- This script will load a CSV file representing static route data
- The script will then parse the data and create a JSON payload in the format required by the dashboard API to
  create routes.
- This data will be passed to a function that uses a POST endpoint to create a static route, saving the resulting
  route IDs to a basic list
- If desired, the commented-out function 'get_static_route' can be used to loop over the resulting list and use
  the GET MX static route endpoint to return the created route and print the API response to console.

Prerequisites:
- A Meraki Dashboard account with an appliance network
- The appliance network must be configured to use VLANs and must have a 169.254.255.0/30 subnet


'''

import json
import requests
from csv import DictReader

# Update this to your API key
API_KEY = 'API_KEY_HERE'

headers = {
    'X-Cisco-Meraki-API-Key': API_KEY,
    'Content-Type': 'application/json'
           }

# Update this to your network ID
network_id = 'N_0000111122223333'

#
route_id_list = []


'''
Example API Call - GET
'''
'''
def get_static_route(route_id):
    print("GET")
    base_url = f'https://api.meraki.com/api/v1/networks/{network_id}/appliance/staticRoutes/{route_id}'
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        print('success')
        print(response.json())
    else:
        print('start failure')
        print('status code: ' + str(response.status_code))
        print(response.json())
        print('end failure')
'''

'''
Example API Call - POST
'''
def create_static_route(request_data):
    print("POST")
    #
    base_url = f'https://api.meraki.com/api/v1/networks/{network_id}/appliance/staticRoutes'
    #
    response = requests.post(base_url, headers=headers, data=request_data)
    #
    if response.status_code == 201:
        print('success')
        #
        response_data = response.json()
        #
        static_route_id = response_data.get("id")
        #
        route_id_list.append(static_route_id)
        print(static_route_id)
    else:
        print('start failure')
        #
        print(request_data)
        #
        print('status code: ' + str(response.status_code))
        #
        print(response.json())
        print('end failure')

'''
CSV Parser - baked into main
'''
if __name__ == "__main__":
    with open('krk07-routes.csv', 'r') as input_file:
        print("start file")
        #
        csv = DictReader(input_file)
        #
        for row in csv:
            print("---LOOP---")
            print("ROW data " + str(row))
            #
            route_data = {
                #
                "name": row.get('name'),
                #
                "subnet": row.get('subnet'),
                #
                "gatewayIp": row.get('next_hop'),
                #
                "enabled": True
                }
            print("DICT data " + str(route_data))
            #
            json_data = json.dumps(route_data)
            print("JSON data " + str(json_data))
            #
            create_static_route(json_data)
        #
        print(route_id_list)
        print("end file")
        # # call get endpoint on all routes
        # for route_id in route_id_list:
        #     get_static_route(route_id)
