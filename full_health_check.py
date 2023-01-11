import sys
from module_utils.net_tools import get_ssh_info
sys.path.insert(0,'/home/andreoss/Network Automation/module_utils/')
from net_tools import *

def main():
    hostname = ['csr']
    commands = [
        'show clock',
        'show version',
        'show platform',
        'show processes cpu history',
        'show interfaces',
        'show platform hardware qfp active statistics drop | ex _0_',
        'show platform hardware throughput level'
        ]

    devices = get_ssh_info(hostname)

    for device in devices:
        parsed_dic = {}
        net_connect = ConnectHandler(**device)
        for command in commands:
            
            parsed_output = net_connect.send_command(command, use_genie=True)
            parsed_dic[command] = parsed_output

        for key, value in parsed_dic.items():

            if key == 'show clock':
                output = net_connect.send_command(key)
                print('_'*80)
                print(' '*10 , '|', 'Report taken at:' , output ,'|')
                print('-'*80)
                #print(f'Report Initiated at: {output}')
                #print('-'*80)


            if key == 'show version':
                print('_'*80)
                print(' '*25 , '|',key,'|')
                print('-'*80)
                print(f" Device Hostname and chassis: {parsed_dic['show version']['version']['hostname']} and {parsed_dic['show version']['version']['rtr_type']}")
                print(f" Platform: {parsed_dic['show version']['version']['platform']}")
                print(f" Running IOS Version: {parsed_dic['show version']['version']['xe_version']}")
                print(f" Router SN: {parsed_dic['show version']['version']['chassis_sn']}")
                print(f" This Router has been up for: {parsed_dic['show version']['version']['uptime']}")
                print(f" Last reason for reload was: {parsed_dic['show version']['version']['last_reload_reason']}")
                print(f" Licenses Level is: {parsed_dic['show version']['version']['license_level']}")



            if key == 'show platform':
                print('_'*80)
                print(' '*25 , '|',key,'|')
                print('-'*80)                
                for slots, info in parsed_dic['show platform']['slot'].items():
                    for module, info in parsed_dic['show platform']['slot'][slots].items():

                        print( module ,':', '\n', 'State:' , info['CSR1000V']['state'],'\n','Insert Time:' , info['CSR1000V']['insert_time'] )

            if key == 'show processes cpu history':
                maximum_cpu_60s = []
                maximum_cpu_60m = []
                maximum_cpu_72h = []

                for ticks , cpu in parsed_dic['show processes cpu history']['60s'].items():
                    maximum_cpu_60s.append(cpu['maximum'])
                maximum_cpu_1min = max(maximum_cpu_60s)

                for ticks , cpu in parsed_dic['show processes cpu history']['60m'].items():
                    maximum_cpu_60m.append(cpu['maximum'])
                maximum_cpu_60min = max(maximum_cpu_60m)

                for ticks , cpu in parsed_dic['show processes cpu history']['72h'].items():
                    maximum_cpu_72h.append(cpu['maximum'])
                maximum_cpu_72hou = max(maximum_cpu_72h)
                print('_'*80)
                print(' '*25 , '|',key,'|')
                print('-'*80)
                print(f'Maximum CPU utilization in the last minute:     {maximum_cpu_1min} %')
                print(f'Maximum CPU utilization in the last hour:       {maximum_cpu_60min} %')
                print(f'Maximum CPU utilization in the last 72 hours:   {maximum_cpu_72hou} %')
                print('-'*80)


            if key == 'show interfaces':
                print('_'*80)
                print(' '*25 , '|',key,'|')
                print('-'*80)
                for interface , data in  parsed_dic['show interfaces'].items():
                    print(f"Interface {interface}")      
                    print(f"Description: {parsed_dic['show interfaces'][interface]['description']}")         
                    print(f"Line protocol: {parsed_dic['show interfaces'][interface]['line_protocol']}")
                    print(f"Oper Status: {parsed_dic['show interfaces'][interface]['oper_status']}")
                    print(f"Input Q drops: {parsed_dic['show interfaces'][interface]['queues']['input_queue_drops']}")
                    print(f"Total Output Drops: {parsed_dic['show interfaces'][interface]['queues']['total_output_drop']}")
                    print(f"CRC Errors: {parsed_dic['show interfaces'][interface]['counters']['in_crc_errors']}")
                    print(f"Input Errors: {parsed_dic['show interfaces'][interface]['counters']['in_errors']}")
                    print(f"Output Errors: {parsed_dic['show interfaces'][interface]['counters']['out_errors']}")
                    print('')


            if key == 'show platform hardware qfp active statistics drop | ex _0_':
                print('_'*80)
                print(' '*10 , '|',key,'|')
                print('-'*80)
                for feature, drops in  parsed_dic['show platform hardware qfp active statistics drop | ex _0_']['global_drop_stats'].items():
                    print(f"{feature}: {parsed_dic['show platform hardware qfp active statistics drop | ex _0_']['global_drop_stats'][feature]['packets']} packets")


    

main()