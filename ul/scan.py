import ipaddress
import nmap


def scan_host(start_ip, end_ip):
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)

    ip_list = []

    for ip_int in range(int(start), int(end) + 1):
        ip_list.append(str(ipaddress.IPv4Address(ip_int)))

    for target in ip_list:
        nm = nmap.PortScanner()
        nm.scan(target, arguments='-sV -Pn --unprivileged --script vulners.nse')
        ip = nm.all_hosts()[0]

        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                protocol = proto

                lport = nm[host][proto].keys()
                for port in lport:
                    portt = port
                    service = nm[host][proto][port]

                    if 'script' in service:
                        for script_id, output in service['script'].items():
                            if 'vulners' in script_id:
                                cves = list(map(lambda x: x[:x.index('\n') if "\n" in x else len(x)], list(filter(lambda x: x != '*EXPLOIT*\n    ' and x != '*EXPLOIT*', output.split("\t")[1:]))))
                                CVEs = [cves[i:i + 3] for i in range(0, len(cves), 3)]
                                for CVE in CVEs:
                                    #записываю в бд
                                    print(ip, protocol, portt, CVE[0], CVE[1], CVE[2])




if __name__ == "__main__":
    target = '138.201.80.190'  # Замените на ваш IP-адрес или диапазон
    scan_host(target, '138.201.80.195')
