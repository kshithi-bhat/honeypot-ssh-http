#Libraries import ssh_honeypot.py and argparse
import argparse #starts out with creating an instance of the argparse object 
from ssh_honeypot import *
from web_honeypot import *
#Parse Arguements

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--address', type=str, required=True)
    parser.add_argument('-p', '--port', type=int, required=True)
    parser.add_argument('-u', '--username', type=str)
    parser.add_argument('-pw', '--password', type=str)

    #two more for ssh and http
    parser.add_argument('-s', '--ssh', action='store_true') #if password supplied then stores as true if not then its stored as false
    parser.add_argument('-w', '--http', action="store_true")

    #combine all these args
    args = parser.parse_args() #combines and stores in args object

    try:
        if args.ssh:
            print("[-] Running SSH Honeypot...")
            honeypot(args.address, args.port, args.username, args.password)

            if not args.username:
                username = None
            if not args.password:
                password = None
        elif args.http:
            print("[-] Running HTTP WordPress Honeypot...")

            if not args.username:
                args.username = "admin"
            if not args.password:
                args.password = "password"

                print(f"Port: {args.port} Username: {args.username} Password: {args.password}")
                run_web_honeypot(args.port, args.username, args.password)

            pass 
        else:
            print("[-] Choose a honeypot type (SSH --ssh) or (HTTP --http).")
    except:
        print("\n Exiting HONEYPY...\n")

#now making it web based!!! using python flask and static html file
