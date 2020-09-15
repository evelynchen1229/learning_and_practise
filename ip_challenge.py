import numpy as np

def valid_ip(ip):

    ip_list = ip.split('.')

    num_octet = len(ip_list)

    return len(ip_list) == 4 and min([int(i) in range (0,256) for i in ip_list]) == 1
    #False not in

def num_ip(start,end):

    start_list = np.array([int(i) for i in start.split('.')])

    end_list=np.array([int(i) for i in end.split('.')])

    coefficient = [256**n for n in range(3,-1,-1)]

    num_ip = sum((end_list-start_list)*coefficient)


    return num_ip


ip_start = '255.0.0.0'
ip_end = '255.0.1.10'


if valid_ip(ip_start) and valid_ip(ip_end):
    if ip_end > ip_start:
        print (num_ip(ip_start,ip_end))

    elif ip_end <= ip_start:
        print ("end range needs to be bigger than start range")

else:
    print("please put a valid IPv4 address")






