class IPv4:
    def __init__(self,ip):
        self.ip = ip

    def get_ip(self):
        return self.ip

    def is_valid(ip):
        '''
        check whether an ip address is a valid IPv4 address
        '''
        ip_list = ip.split('.')

        num_octet = len(ip_list)

        return len(ip_list) == 4 and min([int(i) in range (0,256) for i in ip_list]) == 1
        #False not in

    def num_ip(ip):
        '''
        calculate the number of ip addresses within the ip range up till the given address
        '''

        ip_digits = [int(i) for i in ip.split('.')]

        num_ip = sum([ip_digits[3-n]*256**n for n in range (3,-1,-1)])

        return num_ip

    def check_ip(ip1, ip2):
        ip1 = IPv4.get_ip(ip1)
        ip2 = IPv4.get_ip(ip2)
        if IPv4.is_valid(ip1) and IPv4.is_valid(ip2):
            print (f"{ip1} and {ip2} are a valid IPv4 addresses")
            if ip1 < ip2:
                total_num_ip = IPv4.num_ip(ip2) - IPv4.num_ip(ip1)

                print(f"There can be {total_num_ip} ip addresses within the given ip range")

                return total_num_ip
            else:
                print("You ip end range is not greater than the start range. Please check again.")
        elif valid_ip(ip1) is False and valid_ip(ip2):
            print(f"{ip1} is not a valid IPv4 address. Please check again.")

        elif valid_ip(ip1) and valid_ip(ip2) is False:
            print(f"{ip2} is not a valid IPv4 address. Please check again.")
        else:
            print(f"Both {ip1} and {ip2} are not valid IPv4 address. Please check again")








