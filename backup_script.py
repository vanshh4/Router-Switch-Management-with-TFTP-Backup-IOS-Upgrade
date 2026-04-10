import os
from datetime import datetime
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# ==========================================
# 1. NETWORK DEVICE INVENTORY
# ==========================================
# In a real enterprise, these credentials would be stored in environment 
# variables (.env) or a secure vault, not hardcoded in plain text.

# Shared credentials for the lab environment
USERNAME = 'admin'
PASSWORD = 'StrongPass123!'

# Dictionary list of all routers and switches in the Collapsed Core topology
devices = [
    {
        'device_type': 'cisco_ios',
        'host': '192.168.99.2',
        'username': USERNAME,
        'password': PASSWORD,
        'secret': PASSWORD,  # Enable password if needed
        'device_name': 'Dist-1'
    },
    {
        'device_type': 'cisco_ios',
        'host': '192.168.99.3',
        'username': USERNAME,
        'password': PASSWORD,
        'secret': PASSWORD,
        'device_name': 'Dist-2'
    },
    {
        'device_type': 'cisco_ios',
        'host': '192.168.99.4',  # Assuming you assigned this IP to Access-1 VLAN 1
        'username': USERNAME,
        'password': PASSWORD,
        'secret': PASSWORD,
        'device_name': 'Access-1'
    },
    {
        'device_type': 'cisco_ios',
        'host': '192.168.99.5',  # Assuming you assigned this IP to Access-2 VLAN 1
        'username': USERNAME,
        'password': PASSWORD,
        'secret': PASSWORD,
        'device_name': 'Access-2'
    }
]

# ==========================================
# 2. BACKUP FUNCTION
# ==========================================
def backup_device(device, backup_dir, current_date):
    """
    Connects to a single network device, retrieves the running configuration,
    and saves it to a text file in the specified directory.
    """
    device_name = device.pop('device_name') # Remove custom key before passing to Netmiko
    print(f"[{device_name}] Initiating connection to {device['host']}...")
    
    try:
        # Establish SSH connection
        net_connect = ConnectHandler(**device)
        
        # Enter enable mode if not already in privilege level 15
        net_connect.enable()
        
        # Execute the command to get the configuration
        print(f"[{device_name}] Connected successfully. Retrieving running configuration...")
        output = net_connect.send_command("show running-config")
        
        # Format the filename: e.g., Dist-1_192.168.99.2_2026-04-10_14-30.txt
        filename = f"{device_name}_{device['host']}_{current_date}.txt"
        filepath = os.path.join(backup_dir, filename)
        
        # Write the output to a text file
        with open(filepath, 'w') as backup_file:
            backup_file.write(output)
            
        print(f"[{device_name}] Success! Configuration saved to {filepath}\n")
        
        # Disconnect gracefully
        net_connect.disconnect()
        
    except NetmikoAuthenticationException:
        print(f"[{device_name}] ERROR: Authentication failed. Please check credentials.\n")
    except NetmikoTimeoutException:
        print(f"[{device_name}] ERROR: Connection timed out. Device may be offline or unreachable.\n")
    except Exception as e:
        print(f"[{device_name}] ERROR: An unexpected error occurred: {e}\n")

# ==========================================
# 3. MAIN EXECUTION BLOCK
# ==========================================
def main():
    print("-" * 50)
    print("Automated Network Backup Script Initialized")
    print("-" * 50)

    # Create a timestamp for the backup files
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # Ensure a backup directory exists in the current working directory
    backup_dir = "network_backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Created local backup directory: '{backup_dir}/'\n")

    # Loop through each device in the inventory and run the backup function
    for device in devices:
        # We pass a copy of the dictionary so the original remains intact
        backup_device(device.copy(), backup_dir, current_date)

    print("-" * 50)
    print("Backup process completed.")
    print("-" * 50)

# Python standard boilerplate to execute the main function
if __name__ == "__main__":
    main()