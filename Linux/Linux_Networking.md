### Network Interfaces ###

Network interfaces are software or hardware components that allow a system to connect to a network. In Linux-based systems, you can manage and configure network interfaces using different tools

**ip a**
- `ip` is a powerful utility for managing network interfaces, IP addresses, routes, and other network-related settings.
- `ip a` is short for ip address and is used to display the current state of all network interfaces on your system.

```bash
ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: enp3s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
    link/ether 2c:f0:5d:68:0b:80 brd ff:ff:ff:ff:ff:ff
3: wlo1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether ac:12:03:03:a0:5c brd ff:ff:ff:ff:ff:ff
    altname wlp0s20f3
    inet 192.168.145.192/24 brd 192.168.145.255 scope global dynamic noprefixroute wlo1
       valid_lft 2475sec preferred_lft 2475sec
    inet6 2401:4900:a153:8a63:284c:cc1f:cfc2:3743/64 scope global temporary dynamic 
       valid_lft 6961sec preferred_lft 6961sec
    inet6 2401:4900:a153:8a63:3c5c:44b3:9667:dfc5/64 scope global dynamic mngtmpaddr noprefixroute 
       valid_lft 6961sec preferred_lft 6961sec
    inet6 fe80::9fdb:8aaa:308f:32de/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
4: br-93339b4f6609: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
    link/ether 02:42:57:b6:42:3f brd ff:ff:ff:ff:ff:ff
    inet 192.168.58.1/24 brd 192.168.58.255 scope global br-93339b4f6609
       valid_lft forever preferred_lft forever
5: br-a474915b2ee3: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
    link/ether 02:42:e6:0b:f3:f8 brd ff:ff:ff:ff:ff:ff
    inet 172.19.0.1/16 brd 172.19.255.255 scope global br-a474915b2ee3
       valid_lft forever preferred_lft forever
6: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
    link/ether 02:42:c8:88:a5:64 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
7: br-f639f072bc77: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
    link/ether 02:42:d7:22:f8:e9 brd ff:ff:ff:ff:ff:ff
    inet 192.168.49.1/24 brd 192.168.49.255 scope global br-f639f072bc77
       valid_lft forever preferred_lft forever
8: br-37e875adbcd7: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
    link/ether 02:42:a9:bd:8c:ea brd ff:ff:ff:ff:ff:ff
    inet 172.20.0.1/16 brd 172.20.255.255 scope global br-37e875adbcd7
       valid_lft forever preferred_lft forever
9: br-3b0cc0b1a12f: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
    link/ether 02:42:78:73:52:a2 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.1/16 brd 172.18.255.255 scope global br-3b0cc0b1a12f
       valid_lft forever preferred_lft forever
```

**ifconfig**
- `ifconfig` (interface configuration) is a legacy tool used to configure, manage, and display network interfaces on Unix-like systems.
```bash
ifconfig
br-37e875adbcd7: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 172.20.0.1  netmask 255.255.0.0  broadcast 172.20.255.255
        ether 02:42:a9:bd:8c:ea  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 33 overruns 0  carrier 0  collisions 0

br-3b0cc0b1a12f: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 172.18.0.1  netmask 255.255.0.0  broadcast 172.18.255.255
        ether 02:42:78:73:52:a2  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 33 overruns 0  carrier 0  collisions 0

br-93339b4f6609: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.58.1  netmask 255.255.255.0  broadcast 192.168.58.255
        ether 02:42:57:b6:42:3f  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 33 overruns 0  carrier 0  collisions 0

br-a474915b2ee3: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 172.19.0.1  netmask 255.255.0.0  broadcast 172.19.255.255
        ether 02:42:e6:0b:f3:f8  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 33 overruns 0  carrier 0  collisions 0

br-f639f072bc77: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.49.1  netmask 255.255.255.0  broadcast 192.168.49.255
        ether 02:42:d7:22:f8:e9  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 126 overruns 0  carrier 0  collisions 0

docker0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        ether 02:42:c8:88:a5:64  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 33 overruns 0  carrier 0  collisions 0

enp3s0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether 2c:f0:5d:68:0b:80  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 4261  bytes 1171283 (1.1 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 4261  bytes 1171283 (1.1 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlo1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.145.192  netmask 255.255.255.0  broadcast 192.168.145.255
        inet6 fe80::9fdb:8aaa:308f:32de  prefixlen 64  scopeid 0x20<link>
        inet6 2401:4900:a153:8a63:284c:cc1f:cfc2:3743  prefixlen 64  scopeid 0x0<global>
        inet6 2401:4900:a153:8a63:3c5c:44b3:9667:dfc5  prefixlen 64  scopeid 0x0<global>
        ether ac:12:03:03:a0:5c  txqueuelen 1000  (Ethernet)
        RX packets 15323  bytes 11094871 (11.0 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 11999  bytes 6190678 (6.1 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

**nmcli (NetworkManager Command Line Interface)**
- `nmcli` is a command-line interface for NetworkManager, a service that manages network connections in many Linux distributions.
- It provides more advanced network management features, including the ability to connect to wireless networks, configure VPNs, and manage multiple interfaces.

```bash
nmcli device status
DEVICE           TYPE      STATE                   CONNECTION                
wlo1             wifi      connected               OnePlus Nord CE 2 Lite 5G 
lo               loopback  connected (externally)  lo                        
br-37e875adbcd7  bridge    connected (externally)  br-37e875adbcd7           
br-3b0cc0b1a12f  bridge    connected (externally)  br-3b0cc0b1a12f           
br-93339b4f6609  bridge    connected (externally)  br-93339b4f6609           
br-a474915b2ee3  bridge    connected (externally)  br-a474915b2ee3           
br-f639f072bc77  bridge    connected (externally)  br-f639f072bc77           
docker0          bridge    connected (externally)  docker0                   
p2p-dev-wlo1     wifi-p2p  disconnected            --                        
enp3s0           ethernet  unavailable             --                  
```

### Firewall Management ###

**iptables – The Classic Firewall Tool**
- iptables is a user-space utility to configure the Linux kernel firewall implemented in Netfilter. It provides powerful and fine-grained control over inbound/outbound traffic. 
- Characteristics:
 - Low-level, rule-based
 - Persistent rules need manual saving/restoring
 - Complex syntax

**firewalld – Modern, Zone-Based Firewall**
- A dynamic firewall manager using `iptables` or `nftables` in the background. Easier to use and script than raw iptables.
- Characteristics:
 - Zone-based (trusted, public, etc.)
 - Dynamic rule updates (no restart needed)
 - Supports rich rules, services, interfaces

**ufw – Uncomplicated Firewall**
- A simple frontend for `iptables`, made for ease-of-use. Mostly used on Ubuntu/Debian systems.
- Characteristics:
 - Beginner-friendly syntax
 - Basic use-case focused
 - Suitable for desktops and small servers


### Checking Network Connectivity ###

**ping — Test if a host is reachable**
- Sends ICMP echo requests to check if a server is up.
```bash
ping google.com

# Add -c to limit packets sent:
ping -c google.com
```
- Look for packet loss and response time (time=xxx ms).

**curl — Test HTTP/HTTPS availability**
- Great for testing web servers, APIs, and downloading files.
```bash
curl http://example.com

# Follow redirects:
curl -L http://example.com

# Check headers only:
curl -I http://example.com

# Test a specific port:
curl http://example.com:8080

# Add verbose mode for debug:
curl -v http://example.com
```

**wget — Non-interactive file downloader**
- Downloads content via HTTP, HTTPS, or FTP.
```bash
wget http://example.com

# Check if the server is responding (headers only):
wget --spider http://example.com

# Download with retries:
curl -t 3 http://example.com
```

**traceroute — Trace route packets take to host**
- `traceroute` shows the path your packet takes to reach a destination (here, google.com), including each hop (router or gateway) and the time it takes to reach them.
- In Below Example:
 - We are tracing the route to `google.com`, which resolves to IP `142.250.195.14`. It allows a max of 30 hops to reach it.
 - 	`_gateway (192.168.145.240)` Your local router (default gateway). Times: ~3–7 ms (normal)
 - `192.168.17.10` Likely your ISP's first internal router. Times: ~234 ms (a bit high!)
 - `* * *` Timed out (packet blocked or dropped). Common in intermediate hops.
 - `192.168.19.19` Another internal ISP router. Times: 39–61 ms
 - 	`* * *` More timeouts. Not unusual in ISP networks due to ICMP restrictions
 - `128.185.12.93/97` Public IPs — now outside private ISP network. This hop answers with mixed IPs.
 - `182.79.208.13 / 116.119.109.8` Your traffic is now in the public internet, possibly crossing regional ISP backbones
 - `72.14.243.2` Google’s edge network (owned by Google). Fast response ~25–32 ms.
 - `192.178.83.245` Likely another Google transit point. Low latency.
 - `142.251.52.213/211` Inside Google Data Center (multiple responses due to load balancing)
 - `del12s09-in-f14.1e100.net` Final destination: a Google server in Delhi (based on del12...).

```bash
traceroute google.com
traceroute to google.com (142.250.195.14), 30 hops max, 60 byte packets
 1  _gateway (192.168.145.240)  3.520 ms  7.662 ms  7.662 ms
 2  192.168.17.10 (192.168.17.10)  235.479 ms  234.429 ms  235.286 ms
 3  * * *
 4  192.168.19.19 (192.168.19.19)  39.047 ms  51.171 ms  61.012 ms
 5  * * *
 6  * * *
 7  128.185.12.93 (128.185.12.93)  65.736 ms 128.185.12.97 (128.185.12.97)  45.779 ms  35.104 ms
 8  182.79.208.13 (182.79.208.13)  46.491 ms 116.119.109.8 (116.119.109.8)  46.062 ms  30.159 ms
 9  72.14.243.2 (72.14.243.2)  30.060 ms  25.067 ms  32.134 ms
10  192.178.83.245 (192.178.83.245)  30.510 ms  30.149 ms  28.286 ms
11  142.251.52.213 (142.251.52.213)  92.121 ms 142.251.52.211 (142.251.52.211)  90.247 ms 142.251.52.213 (142.251.52.213)  87.767 ms
12  del12s09-in-f14.1e100.net (142.250.195.14)  80.485 ms  44.961 ms  28.255 ms
```

**Use host, nslookup, or dig to test DNS resolution.**

**Use telnet or nc (netcat) to test port connectivity:**

### DNS Resolution ###
DNS (Domain Name System) resolution is the process of converting a domain name (like google.com) into an IP address (like 142.250.182.14) that computers use to communicate.

How DNS Resolution Works in Linux
- User Requests a Domain `ping google.com`
- Linux first checks the file: `/etc/hosts`
  - This file can have static IP ↔ domain mappings. For example:
  ```bash
  127.0.0.1   localhost
  192.168.1.100 myserver.local
  ```
- Check `/etc/nsswitch.conf`
  - This config tells Linux the order of lookup for name resolution.
  - Example line in `/etc/nsswitch.conf`: `hosts: files dns` . This means:
  - Check local `files` (i.e., `/etc/hosts`)
  - Then try `dns` (using `/etc/resolv.conf`)
- Use DNS Servers from `/etc/resolv.conf`
  - If the name wasn’t resolved using `/etc/hosts`, Linux uses the DNS servers listed in: `/etc/resolv.conf`. These are recursive resolvers like Google DNS or Cloudflare DNS. Linux sends a query to them.
  ```bash
  nameserver 8.8.8.8
  nameserver 1.1.1.1
  ```
- If in `/etc/resolv.conf` it is `nameserver 127.0.0.53`, it does not mean your system is resolving DNS queries entirely on its own. Instead, it means your Linux system is using a *local DNS stub resolver*—usually provided by `systemd-resolved`.
- `127.0.0.53` is a loopback IP address (just like 127.0.0.1). It is a local stub resolver that listens on port 53 (DNS port)
- Where does systemd-resolved forward the query. To check the actual DNS servers it will contact (like 8.8.8.8), run: `resolvectl status`. This will show: The DNS servers used for each interface (Ethernet, Wi-Fi, etc.)

