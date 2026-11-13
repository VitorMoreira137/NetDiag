import socket


COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL"
}


def scan_ports(host, ports, timeout=2):

    # Resolve hostname to IPv4
    try:
        ip_address = socket.gethostbyname(host)

    except socket.gaierror:
        return {
            "error": "Unable to resolve hostname."
        }

    results = []

    # Tests each TCP port
    for port in ports:

        service = COMMON_PORTS.get(port, "Unknown")

        try:

            # Creates a TCP socket
            with socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            ) as client:

                client.settimeout(timeout)

                # Attempts TCP connection
                client.connect((ip_address, port))

                state = "Open"

        except ConnectionRefusedError:

            state = "Closed"

        except socket.timeout:

            state = "Timeout"

        except OSError:

            state = "Error"

        results.append({
            "port": port,
            "service": service,
            "state": state
        })

    return {
        "host": host,
        "ip": ip_address,
        "results": results
    }
