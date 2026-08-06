# SocLab: Microsoft Sentinel SOC Investigation & Security Analytics Lab

> Hands-on security analytics lab demonstrating detection engineering, KQL query optimization, and quantitative incident response metrics in Microsoft Sentinel.

## 🎯 Objective
- **Problem:** Traditional SOC labs focus on configuration without measuring detection efficacy or analytical depth
- **Goal:** Build a complete Sentinel investigation pipeline with statistical anomaly detection and measurable outcomes
- **Outcome:** Production-ready detection rules, annotated KQL analytics, and documented triage methodology

## 🏗️ Architecture
<!-- TODO: Add architecture diagram -->
![Architecture Diagram](./docs/architecture.png)

## 🛠️ Tools & Technologies
| Category | Tools Used |
|----------|-----------|
| SIEM / Cloud | Microsoft Sentinel, Azure Log Analytics |
| Query / Analytics | KQL (Advanced), Time-Series Analysis |
| Visualization | Sentinel Workbooks, Azure Monitor |
| Frameworks | MITRE ATT&CK, NIST CSF |
| Data Sources | [List your connected sources] |

## 📈 Key Analytics & Detection Logic

```kql
// Anomaly detection: Failed sign-ins beyond 3σ baseline per user
SigninLogs
| where ResultType == 50126
| summarize FailCount = count() by UserPrincipalName, bin(TimeGenerated, 1h)
| extend BaselineAvg = avg(FailCount), BaselineStd = stdev(FailCount)
| extend ZScore = (FailCount - BaselineAvg) / BaselineStd
| where ZScore > 3
