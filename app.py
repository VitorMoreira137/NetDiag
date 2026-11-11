import streamlit as st
from modules.ping import ping_host

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

elif menu == "DNS Lookup":
    st.header("DNS Lookup")

elif menu == "Port Scanner":
    st.header("Port Scanner")

print("Executado!!")