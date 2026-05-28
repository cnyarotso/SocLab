# Sample Connection Log Observations

The Zeek connection log showed network behavior including:

- TCP 443 HTTPS traffic
- UDP 53 DNS traffic
- UDP 5353 mDNS traffic
- IPv6 DNS traffic
- Connection states such as SF, S0, OTH, and SHR

## Connection State Notes

| State | Meaning |
|---|---|
| SF | Successful connection |
| S0 | Connection attempt with no reply |
| OTH | Incomplete or unusual connection |
| SHR | Partial handshake/reset behavior |

SOC interpretation:
Repeated `S0`, `OTH`, or `SHR` states may be worth investigating if they appear frequently from the same host or target unusual ports.
