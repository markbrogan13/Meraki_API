'''
    Simple call to update Org/Network ID to settings.json
    If settings.json does not exist in the immediate location, one will be created with fields:
    API Key, Org ID, Network ID(s) (in CSV)
    settings.json will not be tracked on git
'''
import os
import meraki
import json

def settings_json(org_dict, file):
        file.write(json.dumps(org_dict, indent = 4))

'''
    Metod to get all org data needed for other API calls
    @params API_KEY: API_KEY of the org admin getting data from all dashboard orgs they are associated with
    @returns org_map: map of all orgs and network IDs mapped for use in settings.json
'''
def get_org_data(API_KEY):
    dashboard = meraki.DashboardAPI(API_KEY) # forms API call and link to the Meraki API
    response = dashboard.organizations.getOrganizations() # gets all orgs within a network
    org_dict = {}
    org_dict['API_KEY'] = API_KEY
    org_dict['BASE_URL'] = "https://api.meraki.com/api/v1/organizations/" # extraneous, however still may be needed for V1 API calls only

    for org in response:
        network_response = dashboard.organizations.getOrganizationNetworks(org["id"])
        org_dict[org["name"]] = org["id"]
        org_dict[org["id"]] = []

        for net_id in network_response:
            org_dict[org["id"]].append([net_id["name"], net_id["id"]])
    
    return org_dict

if __name__ == "__main__":
    if not os.path.exists('./settings.json'):
        file = open("settings.json", "w")
        org_dict = get_org_data(input("API_KEY:"))
        settings_json(org_dict, file)
        file.close()

