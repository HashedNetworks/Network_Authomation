from ipaddress import ip_network
from netmiko import SSHDetect, ConnectHandler
from netmiko import ConnectHandler
from getpass import getpass
from netaddr import *
import yaml


#Takes dictionary with devices info 
def ssh_connection(device):
    net_connect = ConnectHandler(**device)
    net_connect.enable()
    return net_connect



def autodetec(device):

    guesser = SSHDetect(**device)
    best_match = guesser.autodetect()
    print(best_match)                    # Name of the best device_type to use further
    print(guesser.potential_matches)     # Dictionary of the whole matching result
    # Update the 'device' dictionary with the device_type
    device["device_type"] = best_match

    with ConnectHandler(**device) as connection:
        print(connection.find_prompt())



def check_valid_ip_addr(ip_addr):
    try:
        input_address = ip_network(ip_addr)
   
        address = input_address.ip
        network = input_address.network
        netmask = input_address.netmask
        netmask_len = input_address.prefixlen
        is_private = input_address.is_private()
        is_unicast = input_address.is_unicast()

        
        return [str(address), netmask_len, str(netmask), str(network), bool(is_private), bool(is_unicast)]
        
    except AddrFormatError:
        return 'Invalid'  ,  ip_addr


# Converts inventory.yml file to python list. 
# No args: None
# Returns: python list 'invent_list' 
def yaml_to_dic():
    with open('/home/andreoss/Network Automation/inventory/inventory.yml', 'r') as stream:
        try:
        # Converts yaml document to python object
            invent_list=yaml.safe_load(stream)
        
        # Printing dictionary
            #print(d)
        except yaml.YAMLError as e:
            print(e)
    
    return invent_list  


# Finds IP and IOS code for given hostname 
def get_ip_code(item, **invent_list):
        vendor = invent_list['devices']
        for vendor, hostname in vendor.items():
            for hostname , info in hostname.items():
                if hostname == item:
                    host = info['host']
                    device_type = info['device_type']

                    device = {
                        'device_type' : device_type,
                        'host' : host,
                        'username' : 'agarcia',
                        'password' : 'cisco123',
                        }
        return device



def parsed_file_to_yaml(parsed_file, file_to_yml):
    file2 = open(file_to_yml,"w")
    yml_dump = yaml.dump(parsed_file)
    file2.write(yml_dump)



# Parses given command to all hostnames in list. Returns parsed command by Textfms for Arista and Genie for Cisco (IOS and NxOS)
# args: (command: 'show ip int brief'  , input_hostname = ['devices_1' , 'devices_2']) 
# Returns: python list/dic 'parsed_file' 
def send_command(command, input_hostname):

    # Initial Variables
    invent_list = yaml_to_dic()       # Converting inventory yaml file to python list  


    # For each hostname, find IP and IOS-CODE, and run specifc code
    for hostname in input_hostname:                          
        device = get_ip_code(hostname, **invent_list)       # Passing hostnames and inventory Dic to get_ip_code()
        print('')
        print('Connecting to host:', device['host'])         # When host name in found, SSH to it

        if device['device_type'] == 'cisco_ios':

            # SSH Netmiko Connection to Cisco IOS
            ssh_session = ssh_connection(device)                                 
            print(ssh_session.find_prompt())


            # Parsing command with Genie
            parsed_file = ssh_session.send_command(command, use_genie=True)      
            ssh_session.disconnect()
            # Closing SSH session                                              


        if device['device_type'] == 'cisco_nxos':

            # SSH Netmiko Connection To Cisco NXoS
            ssh_session = ssh_connection(device)                                 
            print(ssh_session.find_prompt())


            parsed_file = ssh_session.send_command(command, use_genie=True)      
            ssh_session.disconnect()
            # Closing SSH session


        if device['device_type'] == 'arista_eos':


            # SSH Netmiko Connection To Arista
            ssh_session = ssh_connection(device)                                 
            print(ssh_session.find_prompt())                                   


            parsed_file = ssh_session.send_command(command, use_textfsm=True)      
            ssh_session.disconnect()
            # Closing SSH session



        return (parsed_file)




# Finds IP and IOS code for given hostname 
def get_ssh_info(hostname:list):

    # Converitng inventory YML file to python list.
    #=====================================================================================================================
    with open('/home/andreoss/Network Automation/inventory/inventory.yml', 'r') as inventory_dic:
        try:
        # Converts yaml document to python object
            invent_dic=yaml.safe_load(inventory_dic)
        
        # Printing dictionary
            #print(d)
        except yaml.YAMLError as e:
            print(e)
    
    #Getting hostame info: IP and DEvice-Type for SSH conenction
    #=====================================================================================================================
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
