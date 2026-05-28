# SOC Network Traffic Monitoring Lab with Zeek & Splunk

## Overview

This project documents a hands-on Security Operations Center (SOC) lab that simulates network traffic monitoring, packet capture, Zeek telemetry generation, Splunk SIEM ingestion, field extraction, and dashboard development.

The lab demonstrates how raw network traffic can be captured, transformed into security telemetry, ingested into a SIEM, and analyzed using search queries and dashboard-ready metrics.

## Short Description

Designed and implemented a hands-on SOC monitoring lab using Wireshark, Npcap, Kali Linux, Docker, Zeek, and Splunk to simulate real-world network security operations. The project focused on packet capture, network telemetry generation, SIEM ingestion, threat hunting, field extraction, and dashboard visualization to analyze DNS, HTTPS, mDNS, and TCP traffic within a controlled lab environment.

---

## Lab Architecture

```text
Network Traffic
      ↓
Npcap Packet Capture
      ↓
Wireshark Traffic Collection
      ↓
PCAP/PCAPNG Capture File
      ↓
Kali Linux VM
      ↓
Dockerized Zeek Analysis
      ↓
Zeek Logs
      ↓
Splunk SIEM Ingestion
      ↓
Search, Field Extraction, Dashboards
```

---

## Tools Used

| Tool | Purpose |
|---|---|
| Wireshark | Captures and inspects raw network packets |
| Npcap | Windows packet capture driver used by Wireshark |
| Kali Linux | Security workstation and analysis environment |
| VirtualBox | Virtualization platform for the Kali VM |
| Docker | Containerized Zeek deployment |
| Zeek | Converts packet captures into network security telemetry |
| Splunk | SIEM platform for log ingestion, search, visualization, and alerting |

---

## Project Objectives

- Capture live Wi-Fi network traffic using Wireshark.
- Understand the role of Npcap in packet capture.
- Configure Kali Linux networking for internet access.
- Use Docker to run Zeek when native installation fails due to dependency conflicts.
- Analyze packet captures with Zeek.
- Generate Zeek logs including `conn.log`, `dns.log`, `ssl.log`, and `weird.log`.
- Ingest Zeek logs into Splunk.
- Extract fields from raw Zeek logs.
- Build a dashboard-ready search for top source IP activity.
- Document how this mirrors real-world SOC workflows.

---

## Repository Structure

```text
soc-zeek-splunk-lab/
│
├── README.md
├── screenshots/
├── splunk_queries/
│   ├── top_source_ips.spl
│   ├── extract_source_ip.spl
│   ├── search_all_zeek_conn.spl
│   └── suspicious_connection_states.spl
├── zeek_commands/
│   └── docker_zeek_commands.md
├── notes/
│   ├── soc_workflow_notes.md
│   └── troubleshooting_notes.md
├── docs/
│   └── project_summary.md
└── sample_outputs/
    ├── sample_conn_log_observations.md
    └── sample_dns_observations.md
```

---

## Step-by-Step Lab Workflow

### 1. Install Wireshark and Npcap

Wireshark was used to capture and inspect network traffic. Npcap enabled packet capture on Windows by allowing Wireshark to access network interfaces.

**Key concept:**  
Wireshark is the packet analysis tool. Npcap is the packet capture driver that allows Wireshark to collect traffic from the network adapter.

---

### 2. Configure Kali Linux VM Networking

The Kali VM initially used a Host-Only Adapter and could not resolve internet domains.

The issue appeared as:

```text
Temporary failure resolving 'http.kali.org'
```

The VM interface showed an address like:

```text
192.168.56.101
```

This indicated Host-Only networking.

The adapter was changed to:

```text
NAT
```

After switching to NAT, Kali successfully reached the internet:

```bash
ping google.com
```

---

### 3. Attempt Native Zeek Installation

The initial attempt to install Zeek directly on Kali failed due to dependency conflicts:

```text
zeek : Depends: libc6 (< 2.38) but 2.42-13 is to be installed
```

To avoid breaking Kali by downgrading core libraries, Docker was used instead.

---

### 4. Install and Verify Docker

```bash
sudo apt install docker.io -y
sudo systemctl start docker
sudo docker run hello-world
```

Docker confirmed successful installation.

---

### 5. Run Zeek with Docker

Zeek was verified using the official Zeek Docker image:

```bash
sudo docker run --rm zeek/zeek zeek --version
```

Observed output:

```text
zeek version 8.2.0
```

---

### 6. Save Wireshark Packet Capture

A Wireshark capture was saved from the Windows host into:

```text
C:\temp
```

The capture file used in the lab:

```text
wifitest--pcappng.pcapng
```

A VirtualBox shared folder was configured so Kali could access the Windows folder at:

```bash
/media/sf_temp
```

---

### 7. Generate Zeek Logs from Packet Capture

Navigate to the shared folder:

```bash
cd /media/sf_temp
```

Create an output directory:

```bash
mkdir zeek_output
```

Run Zeek against the packet capture:

```bash
sudo docker run --rm -v "$PWD":/pcap -w /pcap/zeek_output zeek/zeek zeek -r /pcap/wifitest--pcappng.pcapng
```

Zeek generated logs such as:

```text
conn.log
dns.log
packet_filter.log
quic.log
snmp.log
ssl.log
weird.log
x509.log
```

---

### 8. Review Zeek Logs

Check DNS log:

```bash
head zeek_output/dns.log
```

Check connection log:

```bash
head -20 zeek_output/conn.log
```

Observed examples included:

- DNS traffic on port 53
- HTTPS traffic on port 443
- mDNS traffic on port 5353
- IPv6 DNS activity
- Zeek connection states such as `SF`, `S0`, `OTH`, and `SHR`

---

### 9. Ingest Zeek Logs into Splunk

In Splunk:

1. Open **Search & Reporting**
2. Go to **Settings → Add Data**
3. Upload `conn.log`
4. Create a source type named:

```text
zeek_conn
```

5. Complete ingestion
6. Start searching the uploaded data

---

### 10. Search Zeek Logs in Splunk

Search all Zeek connection events:

```spl
sourcetype="zeek_conn"
```

---

### 11. Extract Source IP Field

Splunk initially treated the Zeek log as raw text, so a regex extraction was used:

```spl
sourcetype="zeek_conn"
| rex field=_raw "(?<src_ip>\d+\.\d+\.\d+\.\d+)"
```

This created a usable field called:

```text
src_ip
```

---

### 12. Create Dashboard-Ready Aggregation

The first SOC dashboard metric counted network activity by source IP:

```spl
sourcetype="zeek_conn"
| rex field=_raw "(?<src_ip>\d+\.\d+\.\d+\.\d+)"
| stats count by src_ip
```

Sample result:

| Source IP | Count |
|---|---|
| 10.0.0.79 | 6 |
| 10.0.0.19 | 5 |
| 10.0.0.142 | 1 |

This metric helps identify high-activity hosts, noisy systems, and potential starting points for investigation.

---

## SOC Concepts Demonstrated

### Packet Capture vs SIEM Monitoring

| Layer | Tool | Purpose |
|---|---|---|
| Packet capture | Npcap | Enables packet collection |
| Packet inspection | Wireshark | Deep packet analysis |
| Telemetry generation | Zeek | Converts packets into structured logs |
| SIEM | Splunk | Centralized search, dashboarding, and alerting |

---

## Real-World SOC Parallel

In a real SOC, analysts usually do not watch Wireshark all day. Instead:

1. Network and endpoint tools collect telemetry.
2. SIEM platforms ingest and correlate logs.
3. Alerts are created based on detection rules.
4. Analysts investigate alerts in tools like Splunk.
5. Wireshark is used for deeper packet-level investigation when needed.

This lab simulates the foundation of that workflow.

---

## Screenshots

Screenshots are stored in the `screenshots/` folder and document:

- VirtualBox network configuration
- Kali network troubleshooting
- Wireshark capture saving
- Shared folder setup
- Splunk upload process
- Splunk source type creation
- Splunk search results
- Field extraction using `rex`
- Source IP aggregation results

---

## Key Skills Demonstrated

- Network packet capture
- Wireshark analysis
- Kali Linux troubleshooting
- Docker-based security tooling
- Zeek network telemetry generation
- Splunk SIEM ingestion
- SPL search queries
- Regex field extraction
- SOC dashboard preparation
- Threat hunting fundamentals
- Security documentation

---

## Future Improvements

- Configure continuous log ingestion into Splunk.
- Add DNS-specific dashboards.
- Create alert rules for excessive failed connections.
- Build a port scan detection query.
- Add Suricata for IDS alerting.
- Integrate email alert notifications.
- Explore SOAR workflows using Splunk SOAR or Microsoft Sentinel Playbooks.

---

## Author

Carol Nyarotso  
Cybersecurity • Digital Health Systems • SOC Labs • SIEM • Threat Detection • Data Analytics
