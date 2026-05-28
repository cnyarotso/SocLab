# Troubleshooting Notes

## Kali Could Not Resolve Repositories

Error:

```text
Temporary failure resolving 'http.kali.org'
```

Cause:
The Kali VM was using a Host-Only Adapter, which did not provide internet access.

Fix:
Change VirtualBox network adapter to NAT.

## Zeek Native Install Failed

Error:

```text
zeek : Depends: libc6 (< 2.38) but 2.42-13 is to be installed
```

Cause:
Kali Rolling package dependency conflict.

Fix:
Use Dockerized Zeek instead of downgrading libc6.

## Docker Could Not Find PCAP File

Error:

```text
unable to open /pcap/yourfile.pcap: No such file or directory
```

Cause:
The placeholder filename was used instead of the real capture filename.

Fix:
Use the actual file name:

```text
wifitest--pcappng.pcapng
```

## Zeek Logs Did Not Appear

Cause:
The Docker container wrote logs inside the container instead of the host folder.

Fix:
Set the working directory to the mounted output folder:

```bash
-w /pcap/zeek_output
```
