# Project Summary

This SOC lab demonstrates how packet capture data can be transformed into searchable SIEM telemetry.

The workflow began with Wireshark and Npcap capturing Wi-Fi traffic on Windows. The capture was saved as a PCAPNG file and transferred to Kali Linux using a VirtualBox shared folder. Because native Zeek installation failed due to a Kali dependency conflict, Zeek was run through Docker. Zeek processed the packet capture and generated logs such as `conn.log`, `dns.log`, `ssl.log`, and `weird.log`.

The `conn.log` file was uploaded into Splunk and assigned a custom source type called `zeek_conn`. Splunk was then used to search the ingested telemetry, extract IPv4 source addresses using the `rex` command, and aggregate activity by source IP using `stats count by src_ip`.

This project demonstrates foundational SOC analyst skills including network monitoring, telemetry generation, SIEM ingestion, field extraction, dashboard preparation, and threat hunting.
