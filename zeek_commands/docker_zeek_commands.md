# Dockerized Zeek Commands

## Verify Zeek Version

```bash
sudo docker run --rm zeek/zeek zeek --version
```

## Navigate to Shared Folder

```bash
cd /media/sf_temp
```

## Create Output Folder

```bash
mkdir zeek_output
```

## Run Zeek Against Capture File

```bash
sudo docker run --rm -v "$PWD":/pcap -w /pcap/zeek_output zeek/zeek zeek -r /pcap/wifitest--pcappng.pcapng
```

## List Generated Logs

```bash
ls zeek_output
```

## Review DNS Logs

```bash
head zeek_output/dns.log
```

## Review Connection Logs

```bash
head -20 zeek_output/conn.log
```
