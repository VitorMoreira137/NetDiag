import streamlit as st
from modules.ping import ping_host
from modules.traceroute import trace_route
from modules.dns_lookup import dns_lookup
from modules.port_scanner import scan_ports

st.set_page_config(
    page_title="NetDiag",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 NetDiag")
st.caption("Network Diagnostic Dashboard")

st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Select a tool",
    [
        "Dashboard",
        "Ping Monitor",
        "Traceroute",
        "DNS Lookup",
        "Port Scanner"
    ]
)


if menu == "Dashboard":

    st.markdown("---")

    st.subheader("Network Overview")

    st.write(
        "NetDiag is a Python-based network diagnostic "
        "tool designed to analyze connectivity, network "
        "routes, DNS resolution and TCP services."
    )

    # General metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Diagnostic Tools", "4")
    col2.metric("Protocols", "ICMP / TCP / DNS")
    col3.metric("IP Versions", "IPv4 / IPv6*")
    col4.metric("Platform", "Windows")

    st.markdown("---")

    # Available tools
    st.subheader("Available Tools")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader("📡 Ping Monitor")

            st.write(
                "Test network connectivity and measure "
                "round-trip latency and packet loss."
            )

            st.caption("Technology: ICMP")

        with st.container(border=True):

            st.subheader("🔎 DNS Lookup")

            st.write(
                "Resolve domain names and retrieve "
                "IPv4 and IPv6 addresses."
            )

            st.caption("Technology: DNS / Socket")

    with col2:

        with st.container(border=True):

            st.subheader("🌍 Traceroute")

            st.write(
                "Discover the network path between "
                "your computer and a destination."
            )

            st.caption("Technology: Traceroute / ICMP")

        with st.container(border=True):

            st.subheader("🔌 TCP Port Scanner")

            st.write(
                "Check TCP ports and identify "
                "services accepting connections."
            )

            st.caption("Technology: TCP / Socket")

    st.markdown("---")

    # Getting started
    st.subheader("Getting Started")

    st.info(
        "Select a diagnostic tool from the sidebar "
        "to start analyzing a network destination."
    )

    st.caption(
        "* IPv6 support is currently available in DNS Lookup. "
        "Ping and Port Scanner currently use IPv4."
    )

    st.markdown("---")

    st.caption(
        "NetDiag | Developed with Python and Streamlit"
    )


elif menu == "Ping Monitor":
    st.header("Ping Monitor")
    st.write("Test network connectivity and latency.")

    # Input do endereço de destino
    host = st.text_input(
        "Enter an IP address or hostname:",
        placeholder="Example: google.com"
    )

    # Quantidade de pacotes
    count = st.slider(
        "Number of packets:",
        min_value=1,
        max_value=10,
        value=4
    )

    # Botão para iniciar o teste
    if st.button("Run Ping Test"):

        if host.strip() == "":
            st.warning("Please enter an IP address or hostname.")

        else:
            with st.spinner("Testing connectivity..."):

                result = ping_host(host, count)

            if "error" in result:
                st.error(result["error"])

            else:
                st.subheader("Ping Results")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Packets Received",
                    result["received"]
                )

                col2.metric(
                    "Average Latency",
                    f"{result['average_latency']:.2f} ms"
                    if result["average_latency"] is not None
                    else "N/A"
                )

                col3.metric(
                    "Packet Loss",
                    f"{result['packet_loss']:.1f}%"
                )

                st.write(f"**Destination:** {result['host']}")
                st.write(f"**IP Address:** {result['ip']}")

                if result["response_times"]:
                    st.subheader("Latency Analysis")

                    st.line_chart(
                        result["response_times"]
                    )
                else:
                    st.warning("No ICMP replies received.")

elif menu == "Traceroute":

    st.header("Traceroute")
    st.write("Discover the network route to a destination.")

    # Campo de destino
    host = st.text_input(
        "Destination IP or hostname:",
        placeholder="Example: google.com"
    )

    # Quantidade máxima de saltos
    max_hops = st.slider(
        "Maximum hops:",
        min_value=5,
        max_value=30,
        value=15
    )

    # Timeout
    timeout = st.select_slider(
        "Timeout per probe (ms):",
        options=[500, 1000, 2000, 3000, 5000],
        value=1000
    )

    # Executar Traceroute
    if st.button("Run Traceroute"):

        if host.strip() == "":
            st.warning("Please enter a destination.")

        else:

            with st.spinner("Tracing network route..."):

                result = trace_route(
                    host,
                    max_hops,
                    timeout
                )

            if "error" in result:

                st.error(result["error"])

            else:

                st.subheader("Traceroute Results")

                st.write(f"**Destination:** {result['host']}")

                st.code(
                    result["output"],
                    language="text"
                )

                if result["return_code"] == 0:
                    st.success("Traceroute process completed.")
                else:
                    st.warning(
                        "Traceroute finished with a non-zero exit code. "
                        "Check the output above."
                    )


elif menu == "DNS Lookup":

    st.header("DNS Lookup")
    st.write("Resolve domain names into IP addresses.")

    host = st.text_input(
        "Enter a domain name:",
        placeholder="Example: google.com"
    )

    if st.button("Run DNS Lookup"):

        if host.strip() == "":
            st.warning("Please enter a domain name.")

        else:

            with st.spinner("Resolving hostname..."):

                result = dns_lookup(host)

            if "error" in result:

                st.error(result["error"])

            else:

                st.subheader("DNS Results")

                st.write(f"**Hostname:** {result['hostname']}")

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader("IPv4 Addresses")

                    if result["ipv4"]:
                        for ip in result["ipv4"]:
                            st.code(ip)
                    else:
                        st.info("No IPv4 addresses found.")

                with col2:

                    st.subheader("IPv6 Addresses")

                    if result["ipv6"]:
                        for ip in result["ipv6"]:
                            st.code(ip)
                    else:
                        st.info("No IPv6 addresses found.")

                total = len(result["ipv4"]) + len(result["ipv6"])

                st.metric("Total IP Addresses", total)



elif menu == "Port Scanner":

    st.header("TCP Port Scanner")
    st.write("Scan TCP ports on a target host.")

    st.warning(
        "Only scan devices and networks you own "
        "or have authorization to test."
    )

    host = st.text_input(
        "Target hostname or IP address:",
        placeholder="Example: google.com"
    )

    scan_mode = st.radio(
        "Port selection:",
        ["Common ports", "Custom range"],
        horizontal=True
    )

    common_ports = [
        21, 22, 25, 53, 80, 443, 3306, 5432
    ]

    if scan_mode == "Common ports":

        ports = st.multiselect(
            "Select ports to scan:",
            options=common_ports,
            default=[22, 80, 443, 3306]
        )

    else:

        col1, col2 = st.columns(2)

        with col1:
            start_port = st.number_input(
                "First port:",
                min_value=1,
                max_value=65535,
                value=1
            )

        with col2:
            end_port = st.number_input(
                "Last port:",
                min_value=1,
                max_value=65535,
                value=100
            )

        ports = (
            list(range(int(start_port), int(end_port) + 1))
            if end_port >= start_port
            else []
        )

        if len(ports) > 100:
            st.warning("Please select a range of up to 100 ports.")
            ports = []

    timeout = st.slider(
        "Connection timeout (seconds):",
        min_value=1,
        max_value=5,
        value=2
    )

    if st.button("Start Port Scan"):

        if not host.strip():
            st.warning("Please enter a target hostname or IP.")

        elif not ports:
            st.warning("Please select at least one valid port.")

        else:

            with st.spinner("Scanning TCP ports..."):
                result = scan_ports(host.strip(), ports, timeout)

            if "error" in result:

                st.error(result["error"])

            else:

                st.subheader("Scan Results")

                st.write(f"**Target:** {result['host']}")
                st.write(f"**IP Address:** {result['ip']}")

                
                open_ports = [
                    item for item in result["results"]
                    if item["state"] == "Open"
                ]

                closed_ports = [
                    item for item in result["results"]
                    if item["state"] == "Closed"
                ]

                timeout_ports = [
                    item for item in result["results"]
                    if item["state"] == "Timeout"
                ]

                error_ports = [
                    item for item in result["results"]
                    if item["state"] == "Error"
                ]

                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Open", len(open_ports))
                col2.metric("Closed", len(closed_ports))
                col3.metric("Timeout", len(timeout_ports))
                col4.metric("Error", len(error_ports))

                st.subheader("Port Details")

                st.dataframe(
                    result["results"],
                    use_container_width=True,
                    hide_index=True
                )
   


print("Executado!!")