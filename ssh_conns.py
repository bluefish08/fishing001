import paramiko
import threading

# Function to establish an SSH connection using key-based authentication
def ssh_connect_with_key(ip, username, key_path):
    try:
        # Initialize the SSH client
        client = paramiko.SSHClient()
        
        # Automatically add unknown host keys
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Load the private key from the provided path
        private_key = paramiko.RSAKey.from_private_key_file(key_path)
        
        # Connect to the server using the private key
        client.connect(ip, username=username, pkey=private_key, timeout=5)
        
        # Successful connection message
        print(f"Successfully connected to {ip} with username: {username} using key: {key_path}")
        
        # Optionally, execute a command on the remote server (example)
        # stdin, stdout, stderr = client.exec_command('hostname')
        # print(stdout.read().decode())
        
        # Close the connection
        client.close()
    except Exception as e:
        print(f"Failed to connect to {ip} with username: {username} using key {key_path}. Error: {e}")

# Function to initiate 100 SSH connections concurrently using key-based authentication
def initiate_ssh_connections_with_key(ip, username, key_path, num_connections=100):
    threads = []

    # Create and start threads for 100 SSH connections
    for i in range(num_connections):
        thread = threading.Thread(target=ssh_connect_with_key, args=(ip, username, key_path))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Example Usage
if __name__ == "__main__":
    target_ip = "target_ip_here"  # Replace with the IP of the target system
    target_username = "username_here"  # Replace with the username
    key_path = "/path/to/your/private_key"  # Replace with the path to your private key (e.g., /home/user/.ssh/id_rsa)
    
    # Start 100 SSH connection attempts using key-based authentication
    initiate_ssh_connections_with_key(target_ip, target_username, key_path, num_connections=100)
