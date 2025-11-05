🍯 HoneyPy: A Simple SSH & HTTP Honeypot
HoneyPy is a simple, low-interaction honeypot framework written in Python. It's designed to simulate two of the most commonly attacked services: an SSH server and a WordPress admin login page.

It captures and logs all login attempts and, in the case of the SSH honeypot, basic attacker commands.

🚀 Features
Dual Honeypots: Run either an SSH or an HTTP honeypot from a single script.

SSH Simulation (--ssh):

Uses paramiko to emulate a full SSH server.

Logs all username and password-based login attempts.

Features a simple emulated shell that captures common commands like ls, pwd, whoami, and cat.

HTTP Simulation (--http):

Uses Flask to serve a convincing clone of a WordPress admin login page (wp-admin.html).

Captures all usernames and passwords submitted to the login form.

Detailed Logging:

All captured credentials (SSH & HTTP) and commands (SSH) are logged to separate, rotating log files.

🔧 Setup and Installation
1. Requirements
Python 3

Flask (for the web honeypot)

paramiko (for the SSH honeypot)

2. Install Dependencies
Install the required Python libraries using pip:

Bash
pip install Flask paramiko
3. Generate SSH Server Key
The paramiko SSH server requires an RSA host key to function. You can generate the required server.key file with this command:

Bash
# This creates a 2048-bit RSA key named 'server.key' with no passphrase
ssh-keygen -t rsa -b 2048 -f server.key -N ""
This will create server.key and server.key.pub, which the SSH honeypot will use.

4. Set Up Web Template
The Flask web server looks for its HTML files in a folder named templates by default.

Create the templates directory:

Bash
mkdir templates
Move the wp-admin.html file into it (assuming it's in the same directory):

Bash
mv wp-admin.html templates/
⚙️ How to Run
Use the main honeypy.py script to launch your chosen honeypot. You must specify a service (--ssh or --http), an address (-a), and a port (-p).

The command-line usage is:

Bash
usage: honeypy.py [-h] -a ADDRESS -p PORT [-u USERNAME] [-pw PASSWORD] [-s] [-w]
SSH Honeypot Examples
Example 1: Run on port 2222, accepting any username and password. This is the default and most effective mode for capturing credentials.

Bash
python honeypy.py --ssh -a 127.0.0.1 -p 2222
Any login attempt will be logged and the attacker will be "let in" to the emulated shell.

Example 2: Run on port 2222, accepting only specific credentials. You can set a specific username and password. Only this combination will grant access to the emulated shell.

Bash
python honeypy.py --ssh -a 127.0.0.1 -p 2222 -u admin -pw "secure_pass_123"
HTTP Honeypot Example
Example: Run the WordPress honeypot on port 8080. This will serve the fake WordPress login page on http://<your-ip>:8080.

Bash
python honeypy.py --http -a 0.0.0.0 -p 8080
(Using 0.0.0.0 makes it accessible to other machines on your network. Use 127.0.0.1 for local testing only).

🪵 Viewing the Logs
All activity is recorded in the root directory of the project:

http_audits.log: Records all web login attempts (IP, username, password) from the HTTP honeypot.

audits.log: Records all SSH login attempts (IP, username, password).

cmd_audits.log: Records all commands entered by attackers who successfully "log in" to the SSH honeypot.
