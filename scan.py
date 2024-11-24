import ipaddress
import nmap
import asyncio
import orm

from myLogger import logger


async def scan_host(tid, start_ip, end_ip):
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)
    args = '-A'
    ports = '80'
    if ports:
        args += ' -p ' + ports
    args += ' --unprivileged --script vulners.nse'
    ip_list = []

    for ip_int in range(int(start), int(end) + 1):
        ip_list.append(str(ipaddress.IPv4Address(ip_int)))

    for target in ip_list:
        nm = nmap.PortScanner()
        print('nmap ' + args + ' ' + target)
        nm.scan(target, arguments=args)
        # ip = nm.all_hosts()[0]
        ip = target

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
                                cves = list(map(lambda x: x[:x.index('\n') if "\n" in x else len(x)], list(
                                    filter(lambda x: x != '*EXPLOIT*\n    ' and x != '*EXPLOIT*',
                                           output.split("\t")[1:]))))
                                CVEs = [cves[i:i + 3] for i in range(0, len(cves), 3)]
                                for CVE in CVEs:
                                    print(tid, ip, protocol, portt, CVE[0], CVE[1], CVE[2])
                                    await orm.add_report(tid, ip, protocol, portt, CVE[0], CVE[1], CVE[2])


async def main():
    task = await orm.get_tasks_by_need_run()
    await scan_host(task.tid, task.fromIp, task.toIp)
    await orm.complete_task(task.tid)


if __name__ == "__main__":
    asyncio.run(main())
