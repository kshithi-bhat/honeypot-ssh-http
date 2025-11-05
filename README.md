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

