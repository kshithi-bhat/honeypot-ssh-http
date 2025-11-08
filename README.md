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

**Features**
- SSH honeypot with fake shell and command logging.  
- Web honeypot (fake WordPress login page built with Flask).  
- Rotating logging (audits + command logs).  
- Argparse CLI to select mode and credentials.

> ⚠️ Use only inside labs / VMs / isolated networks.

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

yaml
Copy code

---

## 🛠️ Installation

Install requirements:

```bash
pip install flask paramiko
Generate SSH server key (run once):

bash
Copy code
ssh-keygen -t rsa -b 2048 -f server.key -N ""
🚀 Usage
Start SSH honeypot (accept any credentials)
bash
Copy code
python honeypy.py --ssh -a 0.0.0.0 -p 2223
Start SSH honeypot (require specific credentials)
bash
Copy code
python honeypy.py --ssh -a 0.0.0.0 -p 2223 -u admin -pw secret123
Start Web honeypot (fake WordPress login)
bash
Copy code
python honeypy.py --http -a 0.0.0.0 -p 5000
Open in browser:

text
Copy code
http://localhost:5000
🔐 How to SSH into the honeypot
Recommended: connect from a separate VM or another host.

From another machine / VM
bash
Copy code
ssh -p 2223 testuser@<HONEYPOT_IP>
Local test (same host)
bash
Copy code
ssh -p 2223 attacker@localhost
To skip host-key prompts (optional)
bash
Copy code
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 2223 attacker@<HONEYPOT_IP>
What you will see after login
ruby
Copy code
corporate-jumpbox2$
Built-in/faked commands
text
Copy code
pwd
whoami
ls
cat jumpbox1.conf
exit
Other commands will be echoed back and logged.

📊 Logs
File	Description
audits.log	SSH login attempts (IP + username + password)
cmd_audits.log	Commands executed in the fake SSH shell
http_audits.log	Web login attempts & IPs

Logs use RotatingFileHandler — adjust maxBytes / backupCount in the code if you want different rotation.

✅ Best Practices
Run in an isolated VM or lab network.

Do not expose to public internet without containment.

Never commit server.key to public repos.

Monitor and rotate logs regularly.

🛡️ Disclaimer
This project is for educational cybersecurity research only. The author assumes no responsibility for misuse.

🤝 Contributing
Contributions welcome — fork, open an issue, or submit a PR.
