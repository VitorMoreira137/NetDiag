
import socket


def dns_lookup(host):

    try:

        # Performs DNS resolution
        results = socket.getaddrinfo(
            host,
            None,
            socket.AF_UNSPEC,
            socket.SOCK_STREAM
        )

        # Stores unique IP addresses
        addresses = {
            result[4][0]
            for result in results
        }

        # Separates IPv4 and IPv6 addresses
        ipv4 = []
        ipv6 = []

        for address in addresses:

            if ":" in address:
                ipv6.append(address)

            else:
                ipv4.append(address)

        return {
            "hostname": host,
            "ipv4": sorted(ipv4),
            "ipv6": sorted(ipv6)
        }

    except socket.gaierror:

        return {
            "error": "Unable to resolve hostname."
        }
