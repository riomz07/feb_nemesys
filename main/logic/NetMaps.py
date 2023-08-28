from ping3 import ping


class NetMapsLogic:
    
    def __init__(self, ip=None):
        self.ip = ip

    def check_response(self):
        response = ping(self.ip, timeout=0.01, unit='ms')
        if response == False or response == None:
            return 'off'
        else :
            return 'on'
        
    def check_latency(self):
        response = ping(self.ip, timeout=0.01, unit='ms')
        if response == False or response == None:
            return response
        else :
            return response
