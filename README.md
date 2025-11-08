<h1 align="center">🕵️‍♂️ Honeypy — SSH & WordPress Honeypot Toolkit</h1> <p align="center"> A Python honeypot to study attacker behavior on SSH & fake WordPress login portals. </p> <p align="center"> <img src="https://img.shields.io/badge/Python-3.8%2B-blue" /> <img src="https://img.shields.io/badge/SSH-Honeypot-orange" /> <img src="https://img.shields.io/badge/Web-Honeypot-green" /> <img src="https://img.shields.io/badge/Status-Active-success" /> </p>
📌 Overview

Honeypy simulates vulnerable login services to lure attackers and log their activity.

Features
Component	Description
🐚 SSH Honeypot	Logs brute-force attempts & shell commands
🌐 WordPress honeypot	Fake login page via Flask
📁 Logging	Rotating logs (credentials + commands + IP)
⚙️ CLI	Choose honeypot type & credentials
🧠 Fake shell	Basic Linux commands emulated

⚠️ Only run in isolated labs / VMs.

📂 Directory Structure
honeypot/
├── honeypy.py
├── ssh_honeypot.py
├── web_honeypot.py
├── templates/
│   └── wp-admin.html
├── server.key
├── server.key.pub
├── audits.log
├── cmd_audits.log
└── http_audits.log

🛠️ Installation

Install requirements:

pip install flask paramiko


Generate SSH server key:

ssh-keygen -t rsa -b 2048 -f server.key -N ""

🚀 Usage
SSH Honeypot

Run (accepts any credentials):

python honeypy.py --ssh -a 0.0.0.0 -p 2223


Require specific credentials:

python honeypy.py --ssh -a 0.0.0.0 -p 2223 -u admin -pw secret123

Web Honeypot
python honeypy.py --http -a 0.0.0.0 -p 5000


Visit:

http://localhost:5000

🔐 How to SSH into the honeypot

From another machine / VM:

ssh -p 2223 testuser@<HONEYPOT_IP>


Local test:

ssh -p 2223 attacker@localhost


Skip key prompts:

ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 2223 attacker@<HONEYPOT_IP>


You will see:

corporate-jumpbox2$


Supported commands:

pwd

whoami

ls

cat jumpbox1.conf

exit

All other commands are echoed & logged.

📊 Logs
File	Description
audits.log	SSH login attempts (username/password/IP)
cmd_audits.log	Commands executed inside fake shell
http_audits.log	WordPress login attempts
📸 Demo (Add screenshots)
Fake WP Login	SSH Session
(put screenshot here)	(put SSH session screenshot here)
🚧 Roadmap

Docker deployment

ELK dashboard

Geo-IP heatmap

Telegram/Slack alerts

🛡️ Disclaimer

This project is for ethical security research & learning.
Author is not responsible for misuse.

🤝 Contributing

PRs welcome — ⭐ star the repo if you find it useful.
