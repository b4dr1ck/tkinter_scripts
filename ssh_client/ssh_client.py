#!/usr/bin/python3

import paramiko
import time

def ssh_client(host, port, username, password):
    try:
        # Create an SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown host keys

        # Connect to the server
        print(f"Connecting to {host}:{port} as {username}...")
        client.connect(hostname=host, port=port, username=username, password=password)
        print("Connected successfully!")

        # Open an interactive shell session
        shell = client.invoke_shell()
        print("Interactive shell session started. Type your commands below:")

        # Keep the shell session open
        while True:
            # Read user input
            command = input(f"{username}@{host}> ")
            if command.lower() in ["exit", "quit"]:  # Exit the shell
                print("Exiting the shell...")
                break

            # Send the command to the shell
            shell.send(command + "\n")

            # Wait for the command to execute and fetch the output
            time.sleep(1)  # Allow some time for the command to execute
            if shell.recv_ready():
                output = shell.recv(1024).decode("utf-8")
                print(output)

        # Close the shell and the connection
        shell.close()
        client.close()
        print("Connection closed.")

    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your username and password.")
    except paramiko.SSHException as e:
        print(f"SSH error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    host = input("Enter the SSH server hostname or IP: ")
    port = int(input("Enter the SSH server port (default 22): ") or 22)
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    ssh_client(host, port, username, password)