
import subprocess
import platform
import socket
import re
import time


def ping_host(host, count=4, timeout=2):

    # Identifica o sistema operacional
    system = platform.system().lower()

    # Resolve o domínio para um endereço IPv4
    try:
        ip_address = socket.gethostbyname(host)

    except socket.gaierror:
        return {
            "error": "Unable to resolve hostname."
        }

    # Configura o comando conforme o sistema operacional
    if system == "windows":
        command = ["ping", "-n", "1", "-w",
                   str(timeout * 1000), ip_address]
    else:
        command = ["ping", "-c", "1", "-W",
                   str(timeout), ip_address]

    # Armazena os tempos de resposta
    response_times = []

    # Executa os testes
    for _ in range(count):

        start = time.perf_counter()

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                errors="replace",
                timeout=timeout + 2
            )

            output = result.stdout + result.stderr

            # Verifica se houve resposta
            if result.returncode == 0:

                match = re.search(
                    r"(?:time|tempo)[=<]\s*([\d.,]+)\s*ms",
                    output,
                    re.IGNORECASE
                )

                if match:
                    latency = float(
                        match.group(1).replace(",", ".")
                    )
                    response_times.append(latency)

        except subprocess.TimeoutExpired:
            pass

    # Calcula estatísticas
    received = len(response_times)
    lost = count - received

    average = (
        sum(response_times) / received
        if received > 0 else None
    )

    packet_loss = (lost / count) * 100

    return {
        "host": host,
        "ip": ip_address,
        "sent": count,
        "received": received,
        "lost": lost,
        "packet_loss": packet_loss,
        "average_latency": average,
        "response_times": response_times
    }
