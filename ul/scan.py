import nmap
import json

def scan_host(target):
    nm = nmap.PortScanner()
    nm.scan(target, arguments='-sV -O -sC -A -T4 -p-')

    results = []

    for host in nm.all_hosts():
        host_info = {
            "host": host,
            "state": nm[host].state(),
            "protocol": "tcp"
        }
        results.append(host_info)

        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in sorted(lport):
                port_info = {
                    "port": port,
                    "state": nm[host][proto][port]['state'],
                    "service": nm[host][proto][port]['name'],
                    "product": nm[host][proto][port]['product'],
                    "version": nm[host][proto][port]['version'],
                    "script": nm[host][proto][port]['script'] if 'script' in nm[host][proto][port] else "No script information available"
                }
                results.append(port_info)

        if 'osmatch' in nm[host]:
            for osmatch in nm[host]['osmatch']:
                os_info = {
                    "type": "OS Match",
                    "name": osmatch['name'],
                    "accuracy": osmatch['accuracy']
                }
                results.append(os_info)

    return results

target = '127.0.0.1'
scan_results = scan_host(target)

# Записываем результаты в файл в формате JSON
with open('scan_results.json', 'w') as json_file:
    json.dump(scan_results, json_file, indent=4)

# Выводим результаты на экран
print(json.dumps(scan_results, indent=4))