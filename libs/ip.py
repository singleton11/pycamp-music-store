class IPList(list):
    """Allow network masks in INTERNAL_IPS setting

    Args:
        ips (list): List of IP addresses or masks as strings

    Usage:
        INTERNAL_IPS = IPList(['127.0.0.1', '192.168.1.0/24'])
    """

    def __init__(self, ips):
        try:
            from IPy import IP
            for ip in ips:
                self.append(IP(ip))
        except ImportError:
            pass

    def __contains__(self, ip):
        try:
            for net in self:
                if ip in net:
                    return True
        except:
            pass
        return False
