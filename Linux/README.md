**strace**

The `strace` command in Linux is a *diagnostic tool( used to trace system calls and signals made by a process. It helps debug and monitor how an application interacts with the kernel, allowing you to track file operations, network calls, and potential errors like segmentation faults. It's particularly useful for identifying issues like misbehaving system interactions or performance bottlenecks.
- Example: Suppose you have a program myapp and you want to trace its system calls.
```bash
strace ./myapp
```
This will output all system calls made by myapp, showing things like file operations, memory allocations, and network requests. For example, you might see something like this:
```bash
open("file.txt", O_RDONLY)             = 3
read(3, "Hello, World!", 13)           = 13
write(1, "Hello, World!", 13)          = 13
close(3)                               = 0
```
- `open` opens the file file.txt for reading.
- `read` reads data from the file.
- `write` writes the data to standard output (the terminal).
- `close` closes the file descriptor.

**nohup**
- *Usage*: `nohup` stands for "no hangup," and it is used to run a command that will continue executing even after the user logs out or the terminal session ends.
- *How It Works*: It prevents the process from receiving the SIGHUP (hangup) signal when the terminal session is closed. This allows the process to keep running in the background.
- *Typical Command*: `nohup <command> &`

### iptables ###
`iptables` is a user-space utility program that allows a system administrator to configure the IP packet filter rules of the Linux kernel. It is commonly used for:
- **Packet filtering:** Allows you to control the flow of network traffic based on various criteria (e.g., source IP, destination IP, protocol type, ports).
- **Network Address Translation (NAT):** Used for modifying IP addresses in packet headers (e.g., for masquerading or port forwarding).
- **Connection tracking:** Tracks the state of network connections and enables firewall rules to react based on connection states.
- **Firewalling:** Implements basic security measures to allow or block traffic based on conditions set by the user.

Example
```bash
# Allow incoming HTTP (port 80) traffic
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
```

### IPVS (IP Virtual Server) ###
`IPVS` is a layer 4 (transport layer) load balancing solution built into the Linux kernel. It is part of the Linux Virtual Server (LVS) project and is primarily used for:
- **Load balancing:** Distributing network traffic across multiple backend servers (real servers) to improve scalability and reliability.
- **High availability:** Used in clustered environments to provide a highly available, fault-tolerant system.
- **Scaling:** Helps distribute workloads among multiple servers to prevent overload and optimize resource usage.
IPVS operates at the transport layer (Layer 4), so it works with protocols like TCP, UDP, and SCTP. It uses different scheduling algorithms to direct traffic to the most appropriate backend server.
```bash
# Create a virtual server on IP 192.168.1.100 and port 80
ipvsadm -A -t 192.168.1.100:80 -s rr

# Add real servers to the virtual server pool
ipvsadm -a -t 192.168.1.100:80 -r 192.168.1.10:80 -g
ipvsadm -a -t 192.168.1.100:80 -r 192.168.1.11:80 -g
```
