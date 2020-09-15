import numpy as np

def num_octet(ip):
    
    lp_list = ip.split('.')
  
    return len(lp_list)
    
    
def num_ip(start,end):
    start_list = np.array([int(i) for i in start.split('.')])
    
    end_list=np.array([int(i) for i in end.split('.')])
    
    coefficience = [255**n for n in range(3,-1,-1)]  
    
    num_ip = sum((end_list-start_list)*coefficience)

     
    return num_ip


ip_start = '255.0.1.0'
ip_end = '255.0.1.10'


if num_octet(ip_start)==4 and num_octet(ip_end) ==4 and \
    ip_start >='0.0.0.0' and ip_start <='255.255.255.255' and \
    ip_end >='0.0.0.0' and ip_end <='255.255.255.255':
    
    if ip_end >ip_start:
        print(num_ip(ip_start,ip_end))
        
    elif ip_end <= ip_start:
        print ("end range needs to be bigger than start range")
        
else:
    print("please put a valid IPv4 address")

    




