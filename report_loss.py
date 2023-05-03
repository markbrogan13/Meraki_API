import meraki, json, os
import pandas as pd
import matplotlib.pyplot as plt

'''
    load_settings will take the Org Name and extract this data from the JSON file './settings.json'
    @params str: "org_name"
    @returns non-mutable str: API_KEY, ORG_ID, NETWORK_ID
'''
def load_settings(org_name):
    json_file = open('./settings.json') # opens file
    json_data = json.load(json_file) # load json object into mutable dict for python
    json_file.close() # close file (no mem leaks pls)

    API_KEY = json_data['API_KEY']
    ORG_ID = json_data[org_name]
    NETWORK_IDS = json_data[ORG_ID]
    HYPERION_ID = NETWORK_IDS[0][1]

    return API_KEY, ORG_ID, HYPERION_ID # return needed data for helper functions

'''
    report_loss_latency will take in a Serial, IP address with default to twitch.tv
'''
def report_loss_latency(network_id, serial, ip_addr='151.101.130.167'):
    result = dashboard.devices.getDeviceLossAndLatencyHistory(serial, ip_addr, timespan=300, resolution=60)

    try:
        for data in result:
            del data['goodput']

        json_data_query = open('./dashboard_report.json', 'w')
        json_data_query.write(json.dumps(result, indent = 4))
        json_data_query.close()
    except KeyError:
        print("Null Data -- Check API log")

'''
    Moving Graphing data to a new file for the ability to have live data get collected from the org loss/latency
    Keeping in this file for visibility and later debugging

    def graph_data(json_data):
        data_frame = pd.read_json(json_data)
        data_frame.plot()
        plt.xlabel('Duration (minutes)')
        plt.ylabel('Latency/Percent (ms/%)')
        plt.show()
'''

def remove_api_logs(num_logs_keep):
    file_dir = os.listdir()
    api_log_counter = 0
    api_log_dict = []
    for file in file_dir:
        if str(file).__contains__("meraki_api__log"):
            api_log_counter += 1
            api_log_dict.append(str(file))
    
    if api_log_counter > num_logs_keep:
        remove_num = api_log_counter - num_logs_keep
        for i in range(0, remove_num):
            os.remove(api_log_dict[i])


if __name__ == "__main__":
    api_key, org_id, hyperion_id = load_settings("Cisco")
    dashboard = meraki.DashboardAPI(api_key)
    response = dashboard.networks.getNetworkDevices(hyperion_id)

    serial_of_MX = ''
    for res in response:
        try:
            if res['name'] == 'MX67 - Home':
                serial_of_MX = res['serial']
        except KeyError:
            print(f'No Name -- null value: {res}')
    
    print(serial_of_MX) # remove later
    report_loss_latency(hyperion_id, serial_of_MX)
    remove_api_logs(num_logs_keep=5)


    