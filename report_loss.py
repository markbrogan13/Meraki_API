import meraki
import json
import os

def load_settings(org_name):
    json_file = open('./settings.json')
    json_data = json.load(json_file)

    API_KEY = json_data['API_KEY']
    ORG_ID = json_data[org_name]
    NETWORK_IDS = json_data[ORG_ID]
    HYPERION_ID = NETWORK_IDS[0][1]

    return API_KEY, ORG_ID, HYPERION_ID

def report_loss_latency(network_id, serial, ip_addr='151.101.130.167'):

    result = dashboard.devices.getDeviceLossAndLatencyHistory(serial, ip_addr, timespan=300, resolution=60)
    print(result)

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


    