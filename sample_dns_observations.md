# Sample DNS Observations

The DNS log contained mDNS and local discovery traffic.

Observed indicators:

| Indicator | Meaning |
|---|---|
| 224.0.0.251 | IPv4 multicast DNS |
| ff02::fb | IPv6 multicast DNS |
| Port 5353 | mDNS local discovery |
| `.local` | Local device discovery domain |

Interpretation:
This activity is common on home Wi-Fi networks and is not automatically suspicious. It may represent printers, smart devices, laptops, phones, or local services discovering one another.
