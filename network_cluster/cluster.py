# Description: Configuration file for the application
import json
import argparse
import subprocess
from cluster_network.app import supervisor
from flask_socketio import SocketIO, emit, disconnect
ap = argparse.ArgumentParser()
# do not make it required
ap.add_argument("-i", "--setup",action='store_true', required=False,help="install dependencies")
ap.add_argument("-d", "--debug",action='store_true', required=False,help="debug mode")
ap.add_argument("-s", "--server",action='store_true', required=False,help="start server")
ap.add_argument("-p", "--port",type=int, required=False,default=5001,help="port number")
ap.add_argument("-pull", "--poll",action='store_true', required=False,help="Poll server for messages")
# ap.print_help()
ap.add_argument("-c", "--client",type=str, required=False,default="I have joined the cluster",help="client message")

args = vars(ap.parse_args())
DEBUG = args['debug']
PORT = args['port']
if args['setup']:
    subprocess.call(['sudo','bash','./setup.sh', '-depend'])

if args['server']:
    subprocess.call(['bash','./setup.sh', '-port',str(PORT)])
    supervisor( DEBUG,PORT)
    
    
    

if args['client']:
    from cluster_network.client import send_message,poll_server
    if args['poll']:
        poll_server(args['client'],args['poll'])
    else:
        send_message(args['client'])







# def write_config():
#     config = {
#         "DEBUG": DEBUG,
#         "PORT": PORT
#     }
#     with open('config.json', 'w') as f:
#         json.dump(config, f)
        