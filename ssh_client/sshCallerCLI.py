#!/usr/bin/python3

import sshCaller
import argparse
import sys

# Define command-line arguments using argparse
example_text="""inventory-file format:
[servers.group.subgroup.enviroment]
  host = "hostname"
  user = "username"

exmaples:
# Execute a command on a specific remote host
sshCaller -m myhost.at -u myuser -c "ls -l"
  
# Execute a script on a specific remote host
sshCaller -s /path/to/script.sh -m myhost.at -u myuser
  
# Execute a command on multiple hosts (using filtered groups) in a specific inventory file
sshCaller -c "pwd" -i /path/to/inventory.toml -f "14Pr"

"""

parser = argparse.ArgumentParser(description="""SSH Caller using Paramiko and Inventory File""",
                                  epilog=example_text,
                                  prog='sshCaller.py',
                                  formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-m","--machine", help="The hostname or IP address of the remote machine",default=None)
parser.add_argument("-c","--command", help="The command to execute on the remote machine")
parser.add_argument("-s", "--script", help="Path to a script to execute on the remote host", default=None)
parser.add_argument("-u","--username", help="The username for the SSH connection", default=None)
parser.add_argument("-i","--inventory", help="Path to the inventory.toml file", default=None)
parser.add_argument("-f","--filter", help="Filter to match specific host groups in the inventory (regex allowed)", default=None)
parser.add_argument("-q", "--quiet", help="Quiet mode: suppress additional output", action="store_true")

# Check if no arguments are provided
if len(sys.argv) == 1:
    parser.print_help()  
    sys.exit(1)  

# Parse the arguments
args = parser.parse_args()
    
host_list = sshCaller.parse_inventory(args.inventory,args.filter)

if args.machine and args.username:
    if args.script:
        args.command = sshCaller.script_as_command(args.script)
        
    output = sshCaller.ssh_call(args.machine, args.command, args.username)
    
    # Print the output
    print(output)    
else:
    if args.script:
        args.command = sshCaller.script_as_command(args.script)
        
    # Perform the SSH call
    for group in host_list:
        host = host_list[group]["host"]
        username = host_list[group]["user"]
        
        if not args.quiet:
            print("")
            print("=" * 50)
            print(f"Group:  {group}")  
            print(f"Host:   {host}")
            print(f"User:   {username}")
            if args.script:
                print(f"Script: {args.script}")
            else:
                print(f"Cmd:    {args.command}")
            print("Output:")
            print("")
            
        output = sshCaller.ssh_call(host, args.command, username)
        
        # Print the output
        print(output)
        
