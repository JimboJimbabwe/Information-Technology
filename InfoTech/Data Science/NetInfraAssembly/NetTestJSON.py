import json
import re


def parse_service(line):
    # Regular expression to match port numbers
    port_regex = r'(\d+(?:,\d+)*(?:/[a-z]+)?)'

    # Try to find port numbers
    port_match = re.search(port_regex, line)

    if port_match:
        ports = port_match.group(1)
        service = line.split('-', 1)[1].strip() if '-' in line else line
    else:
        ports = ""
        service = line.strip()

    return {
        "name": service,
        "ports": ports,
        "link": ""
    }


def main():
    services_list = [
        "Pentesting JDWP - Java Debug Wire Protocol",
        "Pentesting Printers",
        "Pentesting SAP",
        "Pentesting VoIP",
        "Pentesting Remote GdbServer",
        "7/tcp/udp - Pentesting Echo",
        "21 - Pentesting FTP",
        "22 - Pentesting SSH/SFTP",
        "23 - Pentesting Telnet",
        "25,465,587 - Pentesting SMTP/s",
        "43 - Pentesting WHOIS",
        "49 - Pentesting TACACS+",
        "53 - Pentesting DNS",
        "69/UDP TFTP/Bittorrent-tracker",
        "79 - Pentesting Finger",
        "80,443 - Pentesting Web Methodology",
        "88tcp/udp - Pentesting Kerberos",
        "110,995 - Pentesting POP",
        "111/TCP/UDP - Pentesting Portmapper",
        "113 - Pentesting Ident",
        "123/udp - Pentesting NTP",
        "135, 593 - Pentesting MSRPC",
        "137,138,139 - Pentesting NetBios",
        "139,445 - Pentesting SMB",
        "143,993 - Pentesting IMAP",
        "161,162,10161,10162/udp - Pentesting SNMP",
        "194,6667,6660-7000 - Pentesting IRC",
        "264 - Pentesting Check Point FireWall-1",
        "389, 636, 3268, 3269 - Pentesting LDAP",
        "500/udp - Pentesting IPsec/IKE VPN",
        "502 - Pentesting Modbus",
        "512 - Pentesting Rexec",
        "513 - Pentesting Rlogin",
        "514 - Pentesting Rsh",
        "515 - Pentesting Line Printer Daemon (LPD)",
        "548 - Pentesting Apple Filing Protocol (AFP)",
        "554,8554 - Pentesting RTSP",
        "623/UDP/TCP - IPMI",
        "631 - Internet Printing Protocol(IPP)",
        "700 - Pentesting EPP",
        "873 - Pentesting Rsync",
        "1026 - Pentesting Rusersd",
        "1080 - Pentesting Socks",
        "1098/1099/1050 - Pentesting Java RMI - RMI-IIOP",
        "1414 - Pentesting IBM MQ",
        "1433 - Pentesting MSSQL - Microsoft SQL Server",
        "1521,1522-1529 - Pentesting Oracle TNS Listener",
        "1723 - Pentesting PPTP",
        "1883 - Pentesting MQTT (Mosquitto)",
        "2049 - Pentesting NFS Service",
        "2301,2381 - Pentesting Compaq/HP Insight Manager",
        "2375, 2376 Pentesting Docker",
        "3128 - Pentesting Squid",
        "3260 - Pentesting ISCSI",
        "3299 - Pentesting SAPRouter",
        "3306 - Pentesting Mysql",
        "3389 - Pentesting RDP",
        "3632 - Pentesting distcc",
        "3690 - Pentesting Subversion (svn server)",
        "3702/UDP - Pentesting WS-Discovery",
        "4369 - Pentesting Erlang Port Mapper Daemon (epmd)",
        "4786 - Cisco Smart Install",
        "4840 - OPC Unified Architecture",
        "5000 - Pentesting Docker Registry",
        "5353/UDP Multicast DNS (mDNS) and DNS-SD",
        "5432,5433 - Pentesting Postgresql",
        "5439 - Pentesting Redshift",
        "5555 - Android Debug Bridge",
        "5601 - Pentesting Kibana",
        "5671,5672 - Pentesting AMQP",
        "5800,5801,5900,5901 - Pentesting VNC",
        "5984,6984 - Pentesting CouchDB",
        "5985,5986 - Pentesting WinRM",
        "5985,5986 - Pentesting OMI",
        "6000 - Pentesting X11",
        "6379 - Pentesting Redis",
        "8009 - Pentesting Apache JServ Protocol (AJP)",
        "8086 - Pentesting InfluxDB",
        "8089 - Pentesting Splunkd",
        "8333,18333,38333,18444 - Pentesting Bitcoin",
        "9000 - Pentesting FastCGI",
        "9001 - Pentesting HSQLDB",
        "9042/9160 - Pentesting Cassandra",
        "9100 - Pentesting Raw Printing (JetDirect, AppSocket, PDL-datastream)",
        "9200 - Pentesting Elasticsearch",
        "10000 - Pentesting Network Data Management Protocol (ndmp)",
        "11211 - Pentesting Memcache",
        "15672 - Pentesting RabbitMQ Management",
        "24007,24008,24009,49152 - Pentesting GlusterFS",
        "27017,27018 - Pentesting MongoDB",
        "44134 - Pentesting Tiller (Helm)",
        "44818/UDP/TCP - Pentesting EthernetIP",
        "47808/udp - Pentesting BACNet",
        "50030,50060,50070,50075,50090 - Pentesting Hadoop"
    ]

    services_dict = {}
    for service in services_list:
        parsed_service = parse_service(service)
        services_dict[parsed_service["name"]] = {
            "ports": parsed_service["ports"],
            "link": parsed_service["link"]
        }

    # Write the result to a JSON file
    output_file = "services.json"
    with open(output_file, "w") as f:
        json.dump(services_dict, f, indent=2)

    print(f"JSON structure has been written to {output_file}")


if __name__ == "__main__":
    main()