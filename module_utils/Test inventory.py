import yaml


def get_inventory_dic():
    with open('/home/andreoss/network_automation/Python Scripts/Network Automation/inventory.yml', 'r') as inventory_dic:
        try:
        # Converts yaml document to python object
            invent_dic=yaml.safe_load(inventory_dic)
        
        # Printing dictionary
            #print(d)
        except yaml.YAMLError as e:
            print(e)
    
    return invent_dic  


# Finds IP and IOS code for given hostname 
def get_ip_code(hostname:list, **invent_dic):
    devices = []
    device = {}
    for num_hn in hostname:
        for platform, value in invent_dic['devices'].items():
            for hn in invent_dic['devices'][platform].keys():
                if hn == num_hn:

                    host = invent_dic['devices'][platform][hn]['host']
                    device_type = invent_dic['devices'][platform][hn]['device_type']

                    device = {
                        'device_type' : device_type,
                        'host' : host,
                        'username' : 'agarcia',
                        'password' : 'cisco123',
                         }

                    devices.append(device)
                

    return devices

def main():

    hostname= ['csr', 'sleaf-01', 'sleaf-02']
    invent_dic = get_inventory_dic()
    devices = get_ip_code(hostname, **invent_dic)
    print(devices)


main()
