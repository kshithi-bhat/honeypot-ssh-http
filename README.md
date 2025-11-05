<h1 align="center">🕵️‍♂️ Honeypy — SSH & WordPress Honeypot Toolkit</h1>

<p align="center">
A lightweight Python honeypot for studying attacker behavior on SSH & fake WordPress login portals.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" />
  <img src="https://img.shields.io/badge/SSH-Honeypot-orange" />
  <img src="https://img.shields.io/badge/Flask-Web%20Honeypot-green" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
</p>

---

## 📌 Overview

Honeypy is a trap system designed to **simulate vulnerable services** and record intruder activity.  
It currently supports:

| Feature | Description |
|--------|------------|
🐚 SSH Honeypot | Logs brute-force attempts & fake shell commands (via Paramiko)  
🌐 WordPress-style Web Honeypot | Captures login credentials & attacker IPs  
🧠 Realistic Fake Shell | Supports commands like `pwd`, `ls`, `whoami`  
📝 Rotating Logs | Stores attacker activity & attempts  
⚙️ CLI Control | Argparse-based interface to choose service type  

> ⚠️ **For cybersecurity learning & research only. Do not deploy on public networks without proper safeguards.**

---

## 🏗️ Project Structure
honeypot-project/
├── templates/
│ └── wp-admin.html # Fake WordPress login page
├── honeypy.py # Main CLI runner
├── ssh_honeypot.py # SSH honeypot engine
├── web_honeypot.py # Web honeypot (Flask)
├── server.key # SSH private key
├── server.key.pub # SSH public key
├── audits.log # SSH login attempts
├── cmd_audits.log # Commands executed in fake shell
└── http_audits.log # Web login attempts


---

## ⚙️ Setup

### 🔧 Install dependencies
```bash
pip install flask paramiko

🔑 Generate SSH host key (if needed)
ssh-keygen -t rsa -b 2048 -f server.key -N ""

🚀 Usage
▶️ SSH Honeypot
python honeypy.py --ssh -a 0.0.0.0 -p 2223


With custom credentials:

python honeypy.py --ssh -a 0.0.0.0 -p 2223 -u admin -pw secret

🌐 Web Honeypot (Fake WordPress Login)
python honeypy.py --http -a 0.0.0.0 -p 5000


Visit in browser:

http://localhost:5000

📊 Logs & Outputs
File	Data
audits.log	SSH login attempts (IP + credentials)
cmd_audits.log	Commands entered in fake shell
http_audits.log	Web login attempts & IPs
📸 Screenshots (Add yours here!)

Replace these with your screenshots

Fake WP Login	SSH Attack

	
🚧 Future Enhancements

📡 Real-time dashboard (ELK stack / Grafana)

🧠 ML-based attacker behavior tagging

🐳 Docker support

🌍 GeoIP mapping of attackers

📩 Telegram/Slack alerting support

🛡️ Legal & Ethical Disclaimer

This project is for educational and defensive security research only.
The author is not responsible for misuse.

Use in a controlled lab / VM / private network only.

🤝 Contributing

Pull Requests welcome!
If you add features like dashboards or Dockerization — please PR 🙌

⭐ Support

If you find this useful:

⭐ Star this repo

🍴 Fork it

🐛 Report issues

🗨️ Share feedback
