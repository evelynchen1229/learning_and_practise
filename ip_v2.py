import ipv4
from ipv4 import IPv4

ip_start = IPv4('20.0.0.0')
ip_end = IPv4('20.0.0.10')

IPv4.check_ip(ip_start,ip_end)
