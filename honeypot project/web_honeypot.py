#implementing web is actually easier python has web extensive services
# using python and flask

# Libraries
import logging     #to log username and password from the wordpress file
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for




# Logging Format
#going to be a but different from ssh logging format

logging_format = logging.Formatter('%(asctime)s %(message)s')

# HTTP Logger
funnel_logger = logging.getLogger('HTTP Logger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler('http_audits.log', maxBytes=2000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

# Baseline honeypot
#2 functions , 1 static webpage with the username and password WordPress admin login page , 2 small function that'll run the app for us -> pass it to out honeypy file and we can run it from argparse logic


def web_honeypot(input_username="admin", input_password="password"):

    app = Flask(__name__) #small scale web server, create app variable 
    

    #declare root of webpage
    @app.route('/')

    def index():
        return render_template('wp-admin.html')
    

    #collect username and password
    @app.route('/wp-admin-login', methods=['POST']) #add route to the webpage, POST will be the only method allowed to be used for the user to interact with the webpage

    def login():
        username = request.form['username']
        password = request.form['password']


        ip_address = request.remote_addr


        funnel_logger.info(f'Client with IP Address: {ip_address} entered\n Username: {username}, Password: {password}')
        #redirecting
        if username == input_username and password == input_password:
            return 'DEEBOODAH'
        else:
            return "Invalid username or password. Please Try Again"
        
    return app


def run_web_honeypot(port=5000, input_username="admin", input_password="password"):
    run_web_honeypot_app = web_honeypot(input_username, input_password)
    run_web_honeypot_app.run(debug=True, port=port, host="0.0.0.0") #debug will give some output port is default 

    return run_web_honeypot_app #enable the capabilty of running the web honeypot
    

#run_web_honeypot(port=5000,input_username="admin", input_password="password")

