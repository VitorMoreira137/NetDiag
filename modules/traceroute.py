import subprocess
import platform


def trace_route(host, max_hops=15, timeout=1000):

    # Identifica o sistema operacional
    system = platform.system().lower()

    # Verifica se o sistema é Windows
    if system != "windows":
        return {
            "error": "This version currently supports Windows only."
        }

    # Monta o comando tracert
    command = [
        "tracert",
        "-d",
        "-h", str(max_hops),
        "-w", str(timeout),
        host
    ]

    try:

        # Executa o comando
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=(max_hops * timeout * 3 / 1000) + 15
        )

        # Captura a saída do terminal
        output = result.stdout

        # Retorna os resultados
        return {
            "host": host,
            "output": output,
            "return_code": result.returncode
        }

    except subprocess.TimeoutExpired:

        return {
            "error": "Traceroute execution timed out."
        }

    except FileNotFoundError:

        return {
            "error": "The tracert command was not found."
        }
