# NetDiag – Network Diagnostic Dashboard

A network diagnostic application developed with Python and Streamlit.

## About

NetDiag is a practical project focused on computer networking fundamentals and network diagnostics.

The application provides tools to investigate network connectivity and analyze communication between devices.

## Current Features

- **Ping Monitor:** Test network connectivity, measure latency and calculate packet loss.
- **DNS Resolution:** Resolve hostnames into IPv4 addresses as part of the ping workflow.

## Technologies

- Python
- Streamlit
- Socket
- Subprocess
- Pandas
- Plotly

## Project Structure

```text
NetDiag/
├── app.py
├── modules/
│   ├── __init__.py
│   └── ping.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

1. Clone this repository.
2. Create a Python virtual environment.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
streamlit run app.py
```

## Development Roadmap

- [x] Initial Streamlit dashboard
- [x] Ping Monitor
- [ ] Traceroute
- [ ] DNS Lookup module
- [ ] TCP Port Scanner
- [ ] Final dashboard improvements

## Learning Objectives

This project explores fundamental networking concepts:

- TCP/IP
- ICMP
- DNS
- IPv4
- RTT and packet loss
- Network diagnostics

## Status

In development.