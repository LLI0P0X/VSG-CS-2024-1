import nmap


def scan_host(target):
    nm = nmap.PortScanner()
    nm.scan(target, arguments='-sV -O -sC -A -T4 -p-')

    for host in nm.all_hosts():
        print(f"Host: {host}")
        print(f"State: {nm[host].state()}")

        for proto in nm[host].all_protocols():
            print(f"Protocol: {proto}")
            lport = nm[host][proto].keys()
            for port in sorted(lport):
                print(f"Port: {port}")
                print(f"State: {nm[host][proto][port]['state']}")
                print(f"Service: {nm[host][proto][port]['name']}")
                print(f"Product: {nm[host][proto][port]['product']}")
                print(f"Version: {nm[host][proto][port]['version']}")

                # Проверка на наличие ключа 'script'
                if 'script' in nm[host][proto][port]:
                    print(f"Script: {nm[host][proto][port]['script']}")
                else:
                    print("Script: No script information available")

        if 'osmatch' in nm[host]:
            for osmatch in nm[host]['osmatch']:
                print(f"OS Match: {osmatch['name']}")
                print(f"Accuracy: {osmatch['accuracy']}")

        print("-" * 60)


target = '127.0.0.1'
scan_host(target)