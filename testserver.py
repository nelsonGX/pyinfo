#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

##########################################################################################
#                             PyThon system INFO script                                  #
#                               PyThon 系統配置訊息腳本                                   #
#                                                                                        #
# credit: https://www.thepythoncode.com/article/get-hardware-system-information-python   #
# edit: Nelson (https://www.nelsongx.com)                                                #
#                                                                                        #
##########################################################################################


#import packages
import subprocess
import sys
import importlib.util
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print('# 安裝套件 ' + package + ' 中...')
if 'psutil' not in sys.modules:
    install(package='psutil')
if 'GPUtil' not in sys.modules:
    install(package='GPUtil')
if 'py-cpuinfo' not in sys.modules:
    install(package='py-cpuinfo')
import psutil
import platform
from datetime import datetime
import GPUtil
import cpuinfo
import re

# -h
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
#start
print('\n'*5)
print('  _____       _____        __                                   ')
print(' |  __ \     |_   _|      / _|        Credit:  Abdou Rockikz    ')
print(' | |__) |   _  | |  _ __ | |_ ___     Edit:    Nelson           ')
print(' |  ___/ | | | | | | |_ \|  _/ _ \                              ')
print(' | |   | |_| |_| |_| | | | || (_) |                             ')
print(' |_|    \__, |_____|_| |_|_| \___/   https://pyinfo.nelsongx.com')
print('         __/ |                                                  ')
print('        |___/            v1.1.0                                 ')
print('\n\n')
print('# Please enter 1 for English, 請輸入 2 以使用中文')
a = 0
a = str(input())
while a!= '1' and a != '2':
    print('# Wrong input. Please try again. 輸入錯誤，請再試一次。')
    a = str(input())
    

if a == '1':
    print("="*40, "System Information", "="*40)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")
    # CPU info
    print("="*40, "CPU Info", "="*40)
    #cpu
    print("CPU: " + str(cpuinfo.get_cpu_info()['brand_raw']) + ' @' + str(cpuinfo.get_cpu_info()['hz_actual_friendly']))
    # number of cores
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    # CPU usage
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")
    # Memory Information
    print("="*40, "Memory Information", "="*40)
    # get the memory details
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    print("="*20, "SWAP", "="*20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}")
    print(f"Free: {get_size(swap.free)}")
    print(f"Used: {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")
    # Disk Information
    print("="*40, "Disk Information", "="*40)
    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total read: {get_size(disk_io.read_bytes)}")
    print(f"Total write: {get_size(disk_io.write_bytes)}")
    # Network information
    print("="*40, "Network Information", "="*40)
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
    # GPU information
    print("="*40, "GPU Details", "="*40)
    gpus = GPUtil.getGPUs()
    if len(str(gpus)) == 2:
        print('This server doesn\'t have any GPU installed.')
    else:
        list_gpus = []
        for gpu in gpus:
            # get the GPU id
            gpu_id = gpu.id
            # name of GPU
            gpu_name = gpu.name
            # get % percentage of GPU usage of that GPU
            gpu_load = f"{gpu.load*100}%"
            # get free memory in MB format
            gpu_free_memory = f"{gpu.memoryFree}MB"
            # get used memory
            gpu_used_memory = f"{gpu.memoryUsed}MB"
            # get total memory
            gpu_total_memory = f"{gpu.memoryTotal}MB"
            # get GPU temperature in Celsius
            gpu_temperature = f"{gpu.temperature} °C"
            gpu_uuid = gpu.uuid
            list_gpus.append((
                gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                gpu_total_memory, gpu_temperature, gpu_uuid
            ))
        print('Id: ' + str(gpu_id))
        print('Name: ' + gpu_name)
        print('Load: ' + gpu_load)
        print('Free Memory:' + gpu_free_memory)
        print('Used Memory: ' + gpu_used_memory)
        print('Total Memory: ' + gpu_total_memory)
        print('Temperature: ' + gpu_temperature)
        print('UUID: ' + gpu_uuid)

#CHINESE

if a == '2':
    print("="*40, "系統資訊", "="*40)
    uname = platform.uname()
    print(f"系統: {uname.system}")
    print(f"節點名稱: {uname.node}")
    print(f"發布: {uname.release}")
    print(f"版本: {uname.version}")
    print(f"主機: {uname.machine}")
    print(f"處理器: {uname.processor}")
    # CPU info
    print("="*40, "CPU 資訊", "="*40)
    #cpu
    print("CPU: " + str(cpuinfo.get_cpu_info()['brand_raw']) + ' @' + str(cpuinfo.get_cpu_info()['hz_actual_friendly']))
    # number of cores
    print("物理性邏輯處理核心:", psutil.cpu_count(logical=False))
    print("總共核心數:", psutil.cpu_count(logical=True))
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    print(f"最高頻率: {cpufreq.max:.2f}Mhz")
    print(f"最低頻率: {cpufreq.min:.2f}Mhz")
    print(f"目前頻率: {cpufreq.current:.2f}Mhz")
    # CPU usage
    print("CPU每核心的使用量:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"總共CPU使用量: {psutil.cpu_percent()}%")
    # Memory Information
    print("="*40, "記憶體(Ram) 資訊", "="*40)
    # get the memory details
    svmem = psutil.virtual_memory()
    print(f"總共: {get_size(svmem.total)}")
    print(f"可用: {get_size(svmem.available)}")
    print(f"已用: {get_size(svmem.used)}")
    print(f"使用百分比: {svmem.percent}%")
    print("="*20, "SWAP", "="*20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print(f"總共: {get_size(swap.total)}")
    print(f"空閒: {get_size(swap.free)}")
    print(f"已用: {get_size(swap.used)}")
    print(f"使用百分比: {swap.percent}%")
    # Disk Information
    print("="*40, "硬碟資訊", "="*40)
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== 裝置: {partition.device} ===")
        print(f"  掛載: {partition.mountpoint}")
        print(f"  儲存資料類型: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        print(f"  總共空間: {get_size(partition_usage.total)}")
        print(f"  已用: {get_size(partition_usage.used)}")
        print(f"  空閒: {get_size(partition_usage.free)}")
        print(f"  使用百分比: {partition_usage.percent}%")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"(自開機以來)已讀取: {get_size(disk_io.read_bytes)}")
    print(f"(自開機以來)已寫入: {get_size(disk_io.write_bytes)}")
    # Network information
    print("="*40, "網路資訊", "="*40)
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"=== 介面卡: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IPv4 地址: {address.address}")
                print(f"  子網路遮罩: {address.netmask}")
                print(f"  廣播 IP 地址: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC 地址: {address.address}")
                print(f"  子網路遮罩: {address.netmask}")
                print(f"  廣播 MAC: {address.broadcast}")
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    print(f"上傳總流量: {get_size(net_io.bytes_sent)}")
    print(f"下載總流量: {get_size(net_io.bytes_recv)}")
    # GPU information
    print("="*40, "GPU 資訊", "="*40)
    gpus = GPUtil.getGPUs()
    if len(str(gpus)) == 2:
        print('這個伺服器沒有安裝任何GPU。')
    else:
        list_gpus = []
        for gpu in gpus:
            # get the GPU id
            gpu_id = gpu.id
            # name of GPU
            gpu_name = gpu.name
            # get % percentage of GPU usage of that GPU
            gpu_load = f"{gpu.load*100}%"
            # get free memory in MB format
            gpu_free_memory = f"{gpu.memoryFree}MB"
            # get used memory
            gpu_used_memory = f"{gpu.memoryUsed}MB"
            # get total memory
            gpu_total_memory = f"{gpu.memoryTotal}MB"
            # get GPU temperature in Celsius
            gpu_temperature = f"{gpu.temperature} °C"
            gpu_uuid = gpu.uuid
            list_gpus.append((
                gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                gpu_total_memory, gpu_temperature, gpu_uuid
            ))
        print('ID: ' + str(gpu_id))
        print('名稱: ' + gpu_name)
        print('負載: ' + gpu_load)
        print('空閒記憶體:' + gpu_free_memory)
        print('已使用記憶體: ' + gpu_used_memory)
        print('總共記憶體: ' + gpu_total_memory)
        print('溫度: ' + gpu_temperature)
        print('UUID: ' + gpu_uuid)

print('\n'*3)
print('='*10)
print('')
print('# 已列印完成系統資訊。')
exit()