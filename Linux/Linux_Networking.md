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
