# Router & Switch Management with TFTP Backup and Automated IOS Upgrade

[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Netmiko](https://img.shields.io/badge/Netmiko-4.x-blue)](https://github.com/ktbyers/netmiko)
[![Ansible](https://img.shields.io/badge/Ansible-2.14+-EE0000?logo=ansible&logoColor=white)](https://ansible.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A university-level network automation project simulating enterprise-grade configuration management, TFTP backup, IOS upgrade workflows, and fully automated monitoring using Python, Ansible, and GitHub Actions.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup and Configuration](#setup-and-configuration)
- [Usage](#usage)
- [Automation Pipeline](#automation-pipeline)
- [Network Security](#network-security)
- [Monitoring and Observability](#monitoring-and-observability)
- [Real-World Mapping](#real-world-mapping)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project simulates a small enterprise network with centrally managed routers and switches, covering the full lifecycle of network device management: IP addressing, configuration backup via TFTP, IOS image management, disaster recovery simulation, and fully automated configuration versioning through GitHub Actions.

The extended version layers in **network segmentation (VLANs)**, **access control (ACLs)**, **dynamic routing (OSPF)**, **Python-based SSH automation (Netmiko)**, **configuration-as-code (Git)**, and **infrastructure monitoring (Syslog + SNMP)** — bringing the project in line with industry-standard NetDevOps practices used in production enterprise environments.

The core idea is that your router and switch configurations should be treated exactly like software source code: versioned, diffed, reviewed, and rolled back when something goes wrong. Every configuration file committed to this repository serves as a timestamped snapshot of the network's state at that moment in time.

---

## Architecture

### Base Topology (Cisco Packet Tracer)

```
                    [TFTP / Syslog Server]
                      192.168.10.100
                            |
             +--------------+--------------+
             |                             |
        [Switch 1]                    [Switch 2]
         /       \                    /       \
   [Router 1]  [PC 1]          [Router 2]  [PC 2]
         \                          /
          +------[Router 3]---------+
                 (Core Router)
```

### Extended Topology with VLANs

```
Management VLAN 10  ┌───────────────────────────────────────────┐
                    │          Core Switch (Layer 3)             │
Data VLAN 20        │   ┌──────────┬──────────┬─────────────┐   │
Guest VLAN 30       │   │ VLAN 10  │ VLAN 20  │   VLAN 30   │   │
                    └───┼──────────┼──────────┼─────────────┼───┘
                        │          │          │             │
                  [Mgmt PC]   [Router 1]  [Router 2]   [Router 3]
                  [TFTP/Syslog]            [OSPF backbone]
```

### Device IP Addressing Table

| Device       | Interface  | IP Address      | VLAN | Role             |
|--------------|------------|-----------------|------|------------------|
| Router 1     | Gi0/0      | 192.168.10.1    | 10   | Branch Router    |
| Router 2     | Gi0/0      | 192.168.10.2    | 10   | Branch Router    |
| Router 3     | Gi0/0      | 192.168.10.3    | 10   | Core Router      |
| Switch 1     | VLAN 10    | 192.168.10.11   | 10   | Access Switch    |
| Switch 2     | VLAN 10    | 192.168.10.12   | 10   | Access Switch    |
| TFTP Server  | NIC        | 192.168.10.100  | 10   | Backup + Syslog  |
| PC 1         | NIC        | 192.168.20.1    | 20   | User Endpoint    |
| PC 2         | NIC        | 192.168.20.2    | 20   | User Endpoint    |

### Backup File Naming Convention

All configuration backups follow a consistent naming pattern so that Git history is human-readable and sortable by date.

| Device   | Backup Filename                          |
|----------|------------------------------------------|
| Router 1 | `router1_running_YYYY-MM-DD.cfg`         |
| Router 2 | `router2_running_YYYY-MM-DD.cfg`         |
| Router 3 | `router3_running_YYYY-MM-DD.cfg`         |
| Switch 1 | `switch1_startup_YYYY-MM-DD.cfg`         |
| Switch 2 | `switch2_startup_YYYY-MM-DD.cfg`         |

---

## Features

### Base Features (Cisco Packet Tracer Simulation)

The initial project layer simulates a small enterprise LAN with 3 routers and 2 switches, a TFTP server for configuration backup and restore, manual backup using `copy running-config tftp`, a disaster recovery simulation through config wipe and TFTP restore, a conceptual IOS image backup workflow, and full device and IP addressing documentation.

### Extended Features (University Level)

The extended project introduces VLAN segmentation with isolated Management, Data, and Guest VLANs; ACL-based security that restricts TFTP and SSH access to authorised management hosts only; OSPF dynamic routing for automatic path failover between routers; STP/RSTP loop prevention on redundant switch links; Python automation using Netmiko for SSH-based config backup; Git version control where every config is saved as a versioned `.cfg` file; GitHub Actions CI/CD for nightly automated backup with drift detection and alerting; Ansible playbooks for push-based configuration restore to multiple devices simultaneously; a centralised Syslog server for log aggregation from all devices; SNMP polling for real-time device health monitoring; and email or Slack alert notifications whenever configuration drift is detected.

---

## Technology Stack

| Layer           | Tool / Protocol      | Purpose                                       |
|-----------------|----------------------|-----------------------------------------------|
| Simulation      | Cisco Packet Tracer  | Network topology and CLI simulation           |
| Scripting       | Python 3.10+         | Automation of SSH backup and restore          |
| SSH Library     | Netmiko 4.x          | Multi-vendor network device SSH abstraction   |
| Config Mgmt     | Ansible 2.14+        | Declarative config push and rollback          |
| Version Control | Git + GitHub         | Config history, diff, and audit trail         |
| CI/CD           | GitHub Actions       | Scheduled backup, drift detection, alerting   |
| Monitoring      | Syslog (rsyslog)     | Centralised device log aggregation            |
| Polling         | SNMP v2c             | Device health metrics (CPU, interfaces)       |
| Alerting        | SMTP / Slack API     | Notification on detected config changes       |

---

## Project Structure

```
network-backup-project/
│
├── .github/
│   └── workflows/
│       └── backup.yml              # GitHub Actions workflow (nightly + manual)
│
├── configs/                        # Versioned device configuration backups
│   ├── router1/
│   │   └── router1_running_2026-04-09.cfg
│   ├── router2/
│   ├── router3/
│   ├── switch1/
│   └── switch2/
│
├── scripts/
│   ├── backup.py                   # SSH into devices and pull running-config
│   ├── restore.py                  # Push a saved config back to a device
│   ├── diff_checker.py             # Compare current configs with last Git commit
│   ├── alert.py                    # Send Slack / email alert on drift detection
│   └── generate_report.py          # Build a summary report of backup results
│
├── ansible/
│   ├── inventory.ini               # Device inventory for Ansible
│   ├── backup_playbook.yml         # Ansible playbook for automated backup
│   └── restore_playbook.yml        # Ansible playbook for config restore
│
├── monitoring/
│   ├── syslog_config.txt           # Cisco device Syslog configuration commands
│   └── snmp_poll.py                # Python SNMP polling script using pysnmp
│
├── docs/
│   ├── topology_diagram.png        # Network topology screenshot from Packet Tracer
│   ├── tftp_server_logs.png        # TFTP server log screenshots
│   └── vlan_acl_table.md           # VLAN and ACL design documentation
│
├── packet_tracer/
│   └── final_nnd_project.pkt       # Cisco Packet Tracer project file
│
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## Prerequisites

### Python Dependencies

Install all required libraries using pip:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```
netmiko==4.3.0
paramiko==3.4.0
pysnmp==6.1.2
ansible==9.2.0
python-dotenv==1.0.0
requests==2.31.0
```

### System Requirements

You will need Python 3.10 or higher, Git 2.x, and Ansible 2.14+ for the playbook-based restore workflow. For live SSH testing, a GNS3, EVE-NG, or real hardware lab is required, since Cisco Packet Tracer does not expose SSH to the host operating system.

> **Note**: The `.pkt` file in this repository demonstrates the full topology and the manual TFTP backup/restore workflow. The Python and Ansible scripts are designed for environments where the devices are reachable over real or emulated SSH.

---

## Setup and Configuration

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/network-backup-project.git
cd network-backup-project
```

### 2. Configure Device Credentials

Create a `.env` file in the project root to store sensitive values. This file must never be committed to Git — it is already listed in `.gitignore`.

```env
DEVICE_USERNAME=admin
DEVICE_PASSWORD=yourpassword
ENABLE_SECRET=yourenablesecret
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
ALERT_EMAIL=your@email.com
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

Add `.env` to your `.gitignore`:

```
.env
*.pyc
__pycache__/
```

### 3. Update Device Inventory

Edit `ansible/inventory.ini` with your lab's actual IP addresses:

```ini
[routers]
router1 ansible_host=192.168.10.1
router2 ansible_host=192.168.10.2
router3 ansible_host=192.168.10.3

[switches]
switch1 ansible_host=192.168.10.11
switch2 ansible_host=192.168.10.12

[network:children]
routers
switches

[network:vars]
ansible_network_os=ios
ansible_connection=network_cli
ansible_user={{ lookup('env', 'DEVICE_USERNAME') }}
ansible_password={{ lookup('env', 'DEVICE_PASSWORD') }}
```

### 4. Enable SSH on Cisco Devices

Run these commands on each Cisco router and switch to enable SSH version 2:

```
Router(config)# hostname Router1
Router(config)# ip domain-name lab.local
Router(config)# crypto key generate rsa modulus 2048
Router(config)# username admin privilege 15 secret yourpassword
Router(config)# line vty 0 4
Router(config-line)# login local
Router(config-line)# transport input ssh
Router(config)# ip ssh version 2
```

### 5. Configure Syslog Forwarding on Each Device

```
Router(config)# logging host 192.168.10.100
Router(config)# logging trap informational
Router(config)# logging on
```

---

## Usage

### Manual Backup (Single Device)

```bash
# Pull running config from one device and save it locally
python scripts/backup.py --host 192.168.10.1 --device-type cisco_ios --output configs/router1/
```

### Backup All Devices at Once

```bash
python scripts/backup.py --all
```

This reads the device list from `ansible/inventory.ini`, SSHes into each one using Netmiko, and saves the running configuration as a timestamped `.cfg` file in the appropriate subdirectory under `configs/`.

### Restore a Config to a Device

```bash
# Push a saved config back to a router (disaster recovery)
python scripts/restore.py --host 192.168.10.1 --config configs/router1/router1_running_2026-04-08.cfg
```

### Run Config Drift Check Manually

```bash
python scripts/diff_checker.py
```

This script pulls the latest configs from all devices and compares them against the last Git commit in the `configs/` folder. Any differences are printed to the console and can be used to trigger an alert.

### Ansible Backup (All Devices via Playbook)

```bash
ansible-playbook ansible/backup_playbook.yml -i ansible/inventory.ini
```

### Ansible Restore (Single Device via Playbook)

```bash
ansible-playbook ansible/restore_playbook.yml -i ansible/inventory.ini \
  --limit router1 \
  --extra-vars "config_file=configs/router1/router1_running_2026-04-08.cfg"
```

---

## Automation Pipeline

The GitHub Actions workflow defined in `.github/workflows/backup.yml` runs every night at midnight UTC. It can also be triggered manually from the GitHub UI or automatically on any push to the `main` branch. The pipeline follows these stages: pull the latest code, set up the Python environment, SSH into every device to fetch configs, check git diff to detect changes, commit and alert if drift is found, and generate a backup report that is uploaded as a workflow artifact.

### Workflow File

```yaml
name: Network Config Backup

on:
  schedule:
    - cron: '0 0 * * *'        # Nightly at midnight UTC
  workflow_dispatch:            # Manual trigger from the GitHub UI
  push:
    branches:
      - main

jobs:
  backup:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run backup script
        env:
          DEVICE_USERNAME: ${{ secrets.DEVICE_USERNAME }}
          DEVICE_PASSWORD: ${{ secrets.DEVICE_PASSWORD }}
          ENABLE_SECRET:   ${{ secrets.ENABLE_SECRET }}
        run: python scripts/backup.py --all

      - name: Check for config drift
        id: drift
        run: |
          git diff --exit-code configs/ || echo "drift=true" >> $GITHUB_OUTPUT

      - name: Commit and push changed configs
        if: steps.drift.outputs.drift == 'true'
        run: |
          git config user.name  "NetBackup Bot"
          git config user.email "bot@github.com"
          git add configs/
          git commit -m "chore: automated config backup $(date -u +%Y-%m-%d)"
          git push

      - name: Send change alert
        if: steps.drift.outputs.drift == 'true'
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          ALERT_EMAIL:       ${{ secrets.ALERT_EMAIL }}
        run: python scripts/alert.py --message "Config drift detected on $(date -u +%Y-%m-%d)"

      - name: Generate backup report
        run: python scripts/generate_report.py >> backup_report.txt

      - name: Upload report as workflow artifact
        uses: actions/upload-artifact@v4
        with:
          name: backup-report
          path: backup_report.txt
```

### Setting Up GitHub Secrets

In your repository go to **Settings → Secrets and variables → Actions** and add the following secrets. These are injected into the runner environment at runtime and never appear in logs.

| Secret Name          | Description                          |
|----------------------|--------------------------------------|
| `DEVICE_USERNAME`    | SSH username for all network devices |
| `DEVICE_PASSWORD`    | SSH password for all network devices |
| `ENABLE_SECRET`      | Cisco enable / privilege password    |
| `SLACK_WEBHOOK_URL`  | Slack incoming webhook URL           |
| `ALERT_EMAIL`        | Destination address for email alerts |

---

## Network Security

### VLAN Design

Traffic is isolated into three VLANs. The Management VLAN carries only administrative traffic such as SSH sessions, TFTP transfers, and SNMP polling. Regular user endpoints live on the Data VLAN and cannot initiate connections to network devices. Guest devices are further isolated on their own VLAN with no access to the other two.

| VLAN | Name       | Subnet           | Purpose                           |
|------|------------|------------------|-----------------------------------|
| 10   | Management | 192.168.10.0/24  | Device management, TFTP, SSH      |
| 20   | Data       | 192.168.20.0/24  | User workstations and servers     |
| 30   | Guest      | 192.168.30.0/24  | Isolated guest access             |

### ACL Configuration (Restricting TFTP and SSH to Management Host)

The ACL below ensures that only the management PC at 192.168.10.100 may initiate TFTP transfers (UDP port 69) or SSH sessions (TCP port 22) to any network device. All other hosts in the Data VLAN are explicitly denied.

```
Router(config)# ip access-list extended MGMT-ONLY
Router(config-ext-nacl)# permit tcp host 192.168.10.100 any eq 22
Router(config-ext-nacl)# permit udp host 192.168.10.100 any eq 69
Router(config-ext-nacl)# deny   ip 192.168.20.0 0.0.0.255 any
Router(config-ext-nacl)# permit ip any any

Router(config)# interface GigabitEthernet0/0
Router(config-if)# ip access-group MGMT-ONLY in
```

### OSPF Dynamic Routing Configuration

OSPF ensures that if one router or link goes down, backup traffic (including TFTP flows and management SSH sessions) automatically reroutes through the remaining paths without any manual intervention.

```
Router(config)# router ospf 1
Router(config-router)# network 192.168.10.0 0.0.0.255 area 0
Router(config-router)# network 192.168.20.0 0.0.0.255 area 0
Router(config-router)# passive-interface GigabitEthernet0/1
```

---

## Monitoring and Observability

### Centralised Syslog Collection

All routers and switches forward their system logs to the server at 192.168.10.100 on UDP port 514. On the server side, `rsyslog` collects and stores these logs by source IP so that each device has its own log file.

```bash
# /etc/rsyslog.d/network.conf — add to the rsyslog configuration on your server
$ModLoad imudp
$UDPServerRun 514
:fromhost-ip, startswith, "192.168.10." /var/log/network/devices.log
```

With syslog in place, you can see exactly when a config change was made via the CLI (which generates a log entry), when a device restarted, and when a backup was triggered — all in a central location.

### SNMP Polling

The `monitoring/snmp_poll.py` script polls each device's SNMP OIDs for CPU usage, memory utilisation, and interface operational status. The example below retrieves the Cisco IOS 5-second CPU average using pysnmp:

```python
from pysnmp.hlapi import *

# OID 1.3.6.1.4.1.9.2.1.56.0 = Cisco IOS CPU 5-second average utilisation
for errorIndication, errorStatus, errorIndex, varBinds in getCmd(
    SnmpEngine(),
    CommunityData('public'),
    UdpTransportTarget(('192.168.10.1', 161)),
    ContextData(),
    ObjectType(ObjectIdentity('1.3.6.1.4.1.9.2.1.56.0'))
):
    if not errorIndication and not errorStatus:
        for varBind in varBinds:
            print(f"Router 1 CPU: {varBind[1]}%")
```

Enable SNMP on each Cisco device with the following commands:

```
Router(config)# snmp-server community public RO
Router(config)# snmp-server location Lab-Room-101
Router(config)# snmp-server contact admin@lab.local
```

---

## Real-World Mapping

This project's concepts map directly to production engineering practices used in large organisations.

**Enterprise IT Operations** — Large companies with hundreds of branch office routers use nightly automated config backups and Git-based version history to manage their WAN infrastructure. The GitHub Actions pipeline in this project mirrors that workflow exactly, at a scale appropriate for a lab environment.

**ISP Network Operations** — Internet Service Providers must restore a replacement router's full configuration within minutes of hardware failure, because every minute of downtime affects thousands of customers. The Ansible restore playbook in this project simulates precisely that operational procedure.

**Compliance Auditing (PCI-DSS, SOX)** — Banks and financial institutions are legally required to maintain an audit trail recording who changed what network configuration and when. Every `git commit` in the `configs/` folder of this repository serves as that audit trail, complete with timestamps and author attribution.

**Disaster Recovery Drills** — Enterprise network teams perform quarterly DR drills where they deliberately wipe a device and verify that a junior engineer can restore full operation from backup alone. The config wipe-and-restore procedure demonstrated in Cisco Packet Tracer, and the more advanced Ansible-based restore playbook, both simulate this drill.

**NetDevOps Pipelines** — The combination of Python, Ansible, and GitHub Actions used here is the standard open-source NetDevOps stack deployed at companies such as LinkedIn, Cloudflare, and large telecommunications operators worldwide.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss the proposal.

To contribute, fork the repository, create a feature branch (`git checkout -b feature/add-snmp-alerting`), commit your changes using the Conventional Commits format (`git commit -m 'feat: add SNMP threshold alerting'`), push the branch, and open a pull request.

Commit message prefixes to use: `feat:` for new features, `fix:` for bug fixes, `chore:` for routine tasks such as automated backups, `docs:` for documentation updates, and `refactor:` for code improvements that do not change behaviour.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Built as part of the Networks and Networking Devices (NND) coursework. Extended with industry-standard NetDevOps practices including Python automation, Ansible configuration management, GitHub Actions CI/CD, and network observability.*
