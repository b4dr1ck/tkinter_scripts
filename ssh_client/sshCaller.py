
import paramiko
import sys
import toml
import os
import toml
import re

def parse_inventory(file_path, filter=None):
    """
    Parse the inventory.toml file and extract host and user keys filtered by a regular expression.
    
    Inventory file format:  
    
    [servers.group.subgroup.enviroment]
        host = "hostname"
        user = "username"
    """
    if not file_path:
        file_path = f"{os.getenv('HOME')}/bin/inventory.toml"

    try:
        inventory = toml.load(file_path)
        servers = inventory.get("servers", {})
        server_data = {}
        
        for group in servers:
            for ta in servers[group]:
                for env in servers[group][ta]:
                    key = f"{group}.{ta}.{env}"
                    if filter:
                        if re.search(filter,key):
                            server_data[key] = servers[group][ta][env]
                    else:
                        server_data[key] = servers[group][ta][env]
        
        return server_data

    except Exception as e:
        print(f"Error parsing inventory file: {e}")
        return {}
    
    
def ssh_call(host, command, username=None):
    """
    Perform an SSH call to a specified host and execute a command using Paramiko.
    """
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()

        # Automatically add the host key if it's not already known
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote host
        ssh.connect(
            hostname=host,
            username=username,
            timeout=10  
        )

        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)

        # Read the output and error streams
        try:
            output = stdout.read().decode("utf-8", errors="replace").strip()
            error = stderr.read().decode("utf-8", errors="replace").strip()
        except UnicodeDecodeError as e:
            print(f"Decoding error: {e}", file=sys.stderr)
            output = stdout.read().decode("latin-1", errors="replace").strip()
            error = stderr.read().decode("latin-1", errors="replace").strip()

        # Close the SSH connection
        ssh.close()

        # Check for errors
        if error:
            return f"Error executing SSH command: {error}"
            
        return output

    except paramiko.AuthenticationException:
        return f"Authentication failed for {username}@{host}.\nPlease check your SSH keys or credentials"
    except paramiko.SSHException as e:
        return f"SSH error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def script_as_command(cmd):
    """
    Execute a script file as a command.
    """
    if not os.path.exists(cmd):
        print(f"Error: The script file '{cmd}' does not exist.")
        sys.exit(1)
    with open(cmd, "r") as file:
        script = file.read()
    
    return script

