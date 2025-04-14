import subprocess

def get_disk_usage():
    """
    Executes the 'df -h' command and parses the output to get disk usage information.

    Returns:
        A list of dictionaries, where each dictionary represents a mounted file system 
        and contains the following keys:
            - 'filesystem': Name of the file system.
            - 'size': Total size of the file system.
            - 'used': Used space on the file system.
            - 'available': Available space on the file system.
            - 'use%': Percentage of used space.
    """
    result = subprocess.run(['df', '-h'], capture_output=True, text=True)
    output = result.stdout

    lines = output.splitlines()[1:]  # Skip the header line
    disk_usage_list = []

    for line in lines:
        fields = line.split()
        filesystem, size, used, available, use_percent, mountpoint = fields[:6]
        disk_usage = {
            'filesystem': filesystem,
            'size': size,
            'used': used,
            'available': available,
            'use%': use_percent,
        }
        disk_usage_list.append(disk_usage)

    return disk_usage_list

if __name__ == "__main__":
    disk_usage_info = get_disk_usage()

    for disk in disk_usage_info:
        print(f"Filesystem: {disk['filesystem']}")
        print(f"Size: {disk['size']}")
        print(f"Used: {disk['used']}")
        print(f"Available: {disk['available']}")
        print(f"Use%: {disk['use%']}")
        print("-" * 20)