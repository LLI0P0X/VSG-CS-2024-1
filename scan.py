import ipaddress
import nmap
import asyncio
import orm

from myLogger import logger


async def scan_host(tid, ip, ports=None):
    ip = str(ip)
    args = '-A'
    if ports:
        args += ' -p ' + ports
    args += ' --unprivileged --script vulners.nse'
    nm = nmap.PortScanner()  # TODO: разобраться в nmap.PortScannerAsync()
    logger.info('Запуск nmap ' + args + ' ' + ip)
    nm.scan(ip, arguments=args)

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
                                logger.info(
                                    f'Найдена уязвимость: {tid}, {ip}, {protocol}, {portt}, {CVE[0]}, {CVE[1]}, {CVE[2]}')
                                await orm.add_report(tid, ip, protocol, portt, CVE[0], CVE[1], CVE[2])


async def cycle():
    while True:
        task = await orm.get_tasks_by_need_run()

        if not task:
            logger.info('Хочу спать')
            await asyncio.sleep(1)
            continue

        start = ipaddress.IPv4Address(task.fromIp)
        end = ipaddress.IPv4Address(task.toIp)
        aiotasks = []

        for ip in range(int(start), int(end) + 1):
            aiotasks.append(scan_host(task.tid, ipaddress.IPv4Address(ip), task.ports))

        await asyncio.gather(*aiotasks)
        await orm.complete_task(task.tid)


def main():
    logger.info('Запуск цикла сканирований')
    try:
        asyncio.run(cycle())
    except KeyboardInterrupt:
        logger.info('Завершение цикла')


if __name__ == "__main__":
    main()
