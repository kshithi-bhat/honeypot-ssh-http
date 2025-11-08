<h1 align="center">🕵️‍♂️ Honeypy — SSH & WordPress Honeypot Toolkit</h1>

<p align="center">
A Python honeypot to study attacker behavior on SSH & fake WordPress login portals.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" />
  <img src="https://img.shields.io/badge/SSH-Honeypot-orange" />
  <img src="https://img.shields.io/badge/Web-Honeypot-green" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
</p>

---

## 📌 Overview

Honeypy simulates vulnerable login services to lure attackers and log their activity.

### Features
| Component | Description |
|----------|------------|
🐚 SSH Honeypot | Logs brute-force attempts & fake shell commands  
🌐 WordPress honeypot | Fake login page built w/ Flask  
📁 Logging | Credential + command + IP logging  
⚙️ CLI Args | Choose honeypot type & credentials  
🧠 Fake shell | Supports common Linux commands  

> ⚠️ **Use only inside labs / VMs / isolated networks.**

---

## 📂 Directory Structure

honeypot/
├── honeypy.py
├── ssh_honeypot.py
├── web_honeypot.py
├── templates/
│ └── wp-admin.html
├── server.key
├── server.key.pub
├── audits.log
├── cmd_audits.log
└── http_audits.log


---

## 🛠️ Installation

Install requirements:
```bash
pip install flask paramiko
Generate SSH server key:

bash
ssh-keygen -t rsa -b 2048 -f server.key -N ""
🚀 Usage
▶️ SSH Honeypot
Start (accepts any credentials):

bash
Copy code
python honeypy.py --ssh -a 0.0.0.0 -p 2223
Require specific username/password:

bash
python honeypy.py --ssh -a 0.0.0.0 -p 2223 -u admin -pw secret123
🌐 Web Honeypot
bash
python honeypy.py --http -a 0.0.0.0 -p 5000

Visit:

arduino
http://localhost:5000
🔐 How to SSH into the honeypot
Recommended: connect from a VM or another host.

Standard login:

bash
ssh -p 2223 testuser@<HONEYPOT_IP>
Local testing:

bash
ssh -p 2223 attacker@localhost
To skip key warnings:

bash
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 2223 attacker@<HONEYPOT_IP>
Once connected you'll see:

ruby
corporate-jumpbox2$
Supported commands:
pwd, whoami, ls, cat jumpbox1.conf, exit
Other commands echo back and get logged.

📊 Logs
File	Description
audits.log	SSH login attempts (username & password)
cmd_audits.log	Commands typed inside honeypot shell
http_audits.log	WordPress login attempts

📸 Demo (Add your screenshots)
Fake WP Login	SSH Session
(screenshot here)	(ssh demo here)

🚧 Future Enhancements
Docker support

Real-time dashboard (ELK / Kibana)

Geo-IP attacker heatmap

Telegram/Slack alerts

🛡️ Disclaimer
This tool is for cybersecurity research & education.
The author is not responsible for illegal use.

🤝 Contributing
PRs welcome — star ⭐ the repo if you like it!
