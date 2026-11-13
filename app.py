import streamlit as st
from modules.ping import ping_host
from modules.traceroute import trace_route
from modules.dns_lookup import dns_lookup

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
    st.header("Network Overview")
    st.info("Welcome to NetDiag!")

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
    st.header("Port Scanner")

print("Executado!!")