A high CPU load is reported on a Linux server running a critical application. How would you systematically investigate and resolve the issue using Linux commands? Explain each step in detail.

**Solution**
- Check System Load and CPU Usage
  - `uptime` This command provides the *system load averages* over the last 1, 5, and 15 minutes. A value higher than the number of CPU cores suggests an overloaded system.
  - Check real-time CPU usage with: `top`
    - This displays CPU utilization and the most resource-intensive processes.
    - I would focus on:
      - `%Cpu(s)`: Breakdown of CPU usage (user, system, I/O wait).
      - Processes consuming the most CPU (sorted by `%CPU` using Shift + P).
- Identify CPU-Intensive Processes
  - I would use the following command to list top CPU-consuming processes. This shows *process ID (PID), parent PID (PPID), command, and CPU usage* sorted by the highest CPU consumers.
    ```bash
    ps -eo pid,ppid,cmd,%cpu --sort=-%cpu | head
    ```
  - If I need to filter for a specific application, I would use: `pgrep -fl <application_name>`
  - To check if a process is stuck in a loop or unresponsive, I would examine: `strace -p <PID>`. This helps in understanding system calls made by the process.
- Investigate System-Wide Resource Utilization
  - Check CPU usage history: `sar -u 5 10`
    - This reports CPU usage every 5 seconds for 10 iterations.
    - Helps determine if high CPU usage is a spike or a sustained issue.
  - Check if CPU is waiting for I/O operations: `iostat -c 2 5`
    - If `%iowait` is high, the CPU might be waiting on slow disk operations.
  - Check memory and swap usage: `free -m`. If memory usage is high and swap is heavily used, the system could be swapping, increasing CPU load.
- Examine Logs for Clues
  - I would check kernel logs for system errors: `dmesg | tail -50`. This helps identify *hardware issues, kernel crashes, or CPU throttling*.
  - I would inspect system logs for anomalies: `journalctl -p 3 -xe`. This filters logs for errors (priority 3 and higher).
- Take Corrective Actions
  - If a process is consuming too much CPU:
    - Reduce its priority: `renice +10 -p <PID>`
    - Or, if it's unresponsive, terminate it: `kill -9 <PID>`
  - If the issue is related to resource limits:
    - Restrict CPU usage for a process using `cpulimit -p <PID> -l 50`
    - Or apply CPU quotas with `cgroups`:
      ```bash
      cgcreate -g cpu:/limitgroup
      echo 50000 > /sys/fs/cgroup/cpu/limitgroup/cpu.cfs_quota_us
      cgclassify -g cpu:/limitgroup <PID>
      ```
  - If swap usage is high:
    - Clear cache to free memory:
      ```bash
      sync; echo 3 > /proc/sys/vm/drop_caches
      ```
- Prevent Future Issues
  - Set CPU limits using `ulimit`:
    ```bash
    ulimit -u 1000  # Limit max user processes
    ```
  - Use monitoring tools like `sar`, `top, or `Prometheus + Grafana` for real-time alerts.
  - Enable process auto-recovery with `systemd`. Configure `Restart=always` to restart a failed service.
    ```bash
    systemctl edit <service> --full
    ```
      









