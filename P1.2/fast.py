import threading
from dns import resolver

ipfile = open('ip_addresses.txt', 'w')

class ResolveDNS(threading.Thread):
    def __init__(self, address):
        threading.Thread.__init__(self)
        self.address = address

    def run(self):
        try:
            result = resolver.query(self.address)[0].to_text()
            ipfile.write(result+'\n')
        except:
            pass

def main():
    dnsfile = open("bmontano6-top-1ht.txt", "r")
    lines = dnsfile.readlines()
    threads = []

    for address in lines:
        address = address.strip()
        resolver_thread = ResolveDNS(address)
        threads.append(resolver_thread)
        resolver_thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
