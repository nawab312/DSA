A process is a running instance of a program. When you type `ls` in your terminal, the *kernel* creates a process — gives it memory, a CPU time slot, a unique ID (PID), and lets it execute. When `ls` finishes, the process dies. Every process in Linux has:
- PID -> unique process ID (number)
- PPID -> parent process ID (who created it)
- UID -> user ID (who owns it)
- Memory space -> its own virtual memory (isolated from other processes)
- File descriptors -> open files, sockets, pipes
- Environment variables -> inherited from parent
- State -> running, sleeping, stopped, zombie, etc.

A **kernel** is the core part of an operating system (OS). It acts like a bridge between your applications and the computer hardware.
- Apps (like Chrome, VS Code) -> make requests
- Kernel -> talks to hardware (CPU, RAM, disk) and fulfills those requests

<img width="527" height="376" alt="image" src="https://github.com/user-attachments/assets/497e4c1a-3bfa-435c-b510-8224c3418623" />

What kernel actually does:
- Process management: Decides which program runs on CPU and for how long
- Memory management: Allocates RAM to programs. Ensures one program doesn’t access another’s memory
- Device management: Talks to hardware like keyboard, disk, network via drivers
- File system management: Handles reading/writing files

---

### How processes are born: fork + exec

Step 1: fork() — the parent process creates an exact copy of itself. Now there are two identical processes — parent and child. They have the same code, same memory contents, same open files. The only difference is the return value of `fork():` parent gets the child's PID, child gets 0.

Step 2: exec() — the child process replaces itself with a new program. The child's memory, code, and stack are wiped and replaced with the new program. The PID stays the same.

Example: what happens when you type `ls` in your terminal:

```
1. Shell (bash, PID 1000) calls fork()
2. Kernel creates child process (PID 1001) — exact copy of bash
3. Child (PID 1001) calls exec("/bin/ls")
4. Kernel replaces child's memory with the ls program
5. ls runs, prints output, exits
6. Parent (bash, PID 1000) calls wait() to collect child's exit status
7. Child is cleaned up, PID 1001 is freed
```

```
bash (PID 1000)
       |
    fork()
       |
  ┌────┴────┐
  │         │
bash      bash copy
(parent)  (child, PID 1001)
  │         │
  │      exec("/bin/ls")
  │         │
  │       ls runs
  │         │
  │       ls exits
  │         │
wait() ◄────┘
  │
bash continues
```

---

### PID 1 — init / systemd

The very first process started by the kernel is PID 1. On modern Linux, this is **systemd**. Every other process is a descendant of PID 1.

```
PID 1 (systemd)
├── PID 500 (sshd)
│   └── PID 1200 (bash — your SSH session)
│       └── PID 1250 (your command)
├── PID 600 (nginx master)
│   ├── PID 601 (nginx worker)
│   └── PID 602 (nginx worker)
├── PID 700 (postgres)
│   ├── PID 701 (postgres worker)
│   └── PID 702 (postgres worker)
└── PID 800 (dockerd)
    └── PID 900 (containerd)
```

Why PID 1 matters for containers:

In a container, YOUR application is PID 1. This has two consequences:
- Signal handling — the kernel sends SIGTERM to PID 1 when the container is stopped. If your app doesn't handle SIGTERM, it won't shut down gracefully.
- Zombie reaping — PID 1 is supposed to call `wait()` on orphaned child processes. If your app doesn't do this, zombie processes accumulate. This is why people use `tini` or `dumb-init` as PID 1 in containers — they handle signal forwarding and zombie reaping.

```dockerfile
# Without init — your app is PID 1 (might not handle signals/zombies)
CMD ["python", "app.py"]

# With tini — tini is PID 1, forwards signals, reaps zombies
RUN apt-get install -y tini
ENTRYPOINT ["tini", "--"]
CMD ["python", "app.py"]
```

---

### Process states 

Every process is in one of these states at any moment. You can see them in the STAT column of `ps aux`.

- **R — Running** — actively using CPU or waiting in the CPU run queue. This is the only state where the process is actually executing instructions.
- **S — Sleeping (interruptible)** — waiting for something — a network response, user input, a timer, a lock. Can be woken up by a signal. Most processes are in this state most of the time. A web server waiting for the next request is in S state.
- **D — Uninterruptible sleep** — waiting for I/O (usually disk). Cannot be interrupted, not even by SIGKILL. If you see a process stuck in D state, it's almost always a disk or NFS problem. You literally cannot kill a D-state process — you have to fix the underlying I/O issue or reboot.
- **Z — Zombie**
  - A zombie is a process that has exited but its parent hasn't called `wait()` to read its exit status.
  - When a child process exits, the kernel keeps a small entry in the process table containing the exit status. This stays until the parent reads it with `wait()`. The kernel does this so the parent can check "did my child succeed or fail?"
  - Zombies use zero CPU and zero memory. They only occupy a PID number and a tiny kernel data structure. A few zombies are completely normal.
  - If a parent keeps spawning children and never calls `wait()`, you get thousands of zombies. Eventually you run out of PIDs (default max is 32768 on Linux, configurable via `/proc/sys/kernel/pid_max`). No new processes can start.
```bash
# Count zombies
ps aux | grep 'Z' | grep -v grep | wc -l

# Find zombie PIDs and their parents
ps -eo pid,ppid,stat,cmd | grep '^.*Z'

# Example output:
# 1250  1200  Z+   [myapp] <defunct>
# 1251  1200  Z+   [myapp] <defunct>
# Parent is PID 1200 — that's the buggy process
```
  - How to fix:
    - Fix the parent — the parent process has a bug. It's not calling `wait()` or `waitpid()` on its children. Fix the code.
    - Kill the parent — if you kill the parent (PID 1200), all its zombie children become orphans. They get re-parented to PID 1 (systemd). systemd always calls wait() on adopted children, so the zombies are cleaned up.
    - You CANNOT kill a zombie directly — `kill -9 <zombie_pid>` does nothing because the process is already dead. There's nothing to kill. You must fix or kill the parent.
  - In containers: If your app is PID 1 and it spawns children without waiting, zombies accumulate with no systemd to clean them up. Use tini as PID 1 to reap zombies automatically.
- **T — Stopped** — paused by a signal (SIGSTOP or SIGTSTP from Ctrl+Z). The process is frozen in memory. It can be resumed with SIGCONT (`fg` command).
- **I — Idle** — kernel thread waiting for work. You'll see this for kernel worker threads. Not relevant for application debugging.

**How to read process states in ps**
```bash
$ ps aux
USER    PID  %CPU %MEM   STAT  COMMAND
root      1  0.0  0.1    Ss    /sbin/init
www     500  2.0  1.5    Sl    nginx: worker process
bob    1200  0.0  0.3    S+    vim file.txt
root   1500  0.0  0.0    D     [kworker/u8:2+flush-8:0]
root   1600  0.0  0.0    Z     [defunct]
```

The STAT column has extra characters:
```
s — session leader
l — multi-threaded
+ — foreground process group
< — high priority (nice value < 0)
N — low priority (nice value > 0)
```

So `Ssl` means: sleeping + session leader + multi-threaded. This is typical for a daemon like nginx or postgres.

---

### Orphan processes
When a parent exits before its children, the children become orphans. The kernel re-parents them to PID 1 (systemd). systemd adopts them and cleans them up when they exit.
Orphans are not a problem — systemd handles them. Zombies are the problem — they need the original parent to call `wait()`.

---

### File descriptors — what processes carry with them
Every process has a table of file descriptors (fds) — integers that point to open files, sockets, pipes, or devices.
```
fd 0 — stdin  (standard input)
fd 1 — stdout (standard output)
fd 2 — stderr (standard error)
fd 3+ — any other open files, sockets, connections
```

**fd leaks** — if your application opens files or sockets and never closes them, fd count grows. Eventually it hits the limit (`ulimit -n`, typically 1024 or 65535) and the process can't open new connections. This is a very common production issue — "too many open files" error.

```bash
# Count open fds for a process
ls /proc/<pid>/fd | wc -l

# See what each fd points to
ls -la /proc/<pid>/fd
# lrwx------ 1 root root 64 ... 0 -> /dev/pts/0        (stdin)
# lrwx------ 1 root root 64 ... 1 -> /dev/pts/0        (stdout)
# lrwx------ 1 root root 64 ... 2 -> /dev/pts/0        (stderr)
# lrwx------ 1 root root 64 ... 3 -> socket:[12345]    (network conn)
# lr-x------ 1 root root 64 ... 4 -> /var/log/app.log  (log file)

# Check fd limits
ulimit -n          # soft limit for current shell
cat /proc/<pid>/limits  # limits for a specific process

# System-wide fd usage
cat /proc/sys/fs/file-nr
# output: 1234   0   65535
#         used   free  max
```

**Inheritance** — when fork() creates a child, the child inherits all parent's file descriptors. This is how pipes work — parent creates a pipe, forks, child inherits the pipe fd.

---

### /proc filesystem — the kernel's window
`/proc` is a virtual filesystem that exposes kernel and process information as files. Nothing in `/proc` is stored on disk — it's generated on the fly by the kernel.

Per-process information at `/proc/<pid>/`:
```
/proc/<pid>/status    # process status (name, state, PID, memory, threads)
/proc/<pid>/cmdline   # exact command line that started the process
/proc/<pid>/environ   # environment variables
/proc/<pid>/fd/       # directory of open file descriptors
/proc/<pid>/maps      # memory mappings (shared libraries, heap, stack)
/proc/<pid>/stat      # raw stats (CPU time, state, priority)
/proc/<pid>/io        # I/O statistics (bytes read/written)
/proc/<pid>/limits    # resource limits (max fds, max memory, etc.)
/proc/<pid>/cgroup    # which cgroups the process belongs to
/proc/<pid>/net/      # network info from this process's namespace
/proc/<pid>/smaps     # detailed memory map (RSS per mapping)
```

System-wide information:
```
/proc/meminfo         # system memory stats (MemTotal, MemFree, Buffers, Cached)
/proc/cpuinfo         # CPU details (model, cores, frequency)
/proc/loadavg         # load average (1, 5, 15 minute)
/proc/uptime          # system uptime in seconds
/proc/sys/            # tunable kernel parameters
/proc/sys/fs/file-max # max open file descriptors system-wide
/proc/sys/kernel/pid_max  # max PID number
/proc/sys/net/        # network tuning parameters
```

When an interviewer asks "how would you investigate a process," your answer should reference /proc. It shows you understand how Linux exposes process information at the kernel level, not just via wrapper tools.

---

### Process priority and nice values
Linux uses the Completely Fair Scheduler (CFS) to decide which process gets CPU time. Each process has a nice value from -20 (highest priority) to +19 (lowest priority). Default is 0.

```bash
# Start a process with low priority (nice = 10)
nice -n 10 ./my_batch_job

# Change priority of a running process
renice -n 5 -p <pid>

# See nice values
ps -eo pid,ni,comm
# PID  NI COMMAND
# 500   0 nginx
# 600  10 backup_job
# 700  -5 database

# Only root can set negative nice values (higher priority)
```

---

### Key process commands — your debugging toolkit
```bash

# ── LIST PROCESSES ──
ps aux                    # all processes with CPU/memory usage
ps -ef                    # all processes with PPID (parent PID)
ps aux --sort=-%cpu       # sort by CPU usage (highest first)
ps aux --sort=-%mem       # sort by memory usage
ps -eo pid,ppid,stat,ni,%cpu,%mem,cmd  # custom columns

# ── REAL-TIME MONITORING ──
top                       # live process monitor
  press 1                 # show per-CPU utilization
  press M                 # sort by memory
  press P                 # sort by CPU
  press k                 # kill a process by PID
htop                      # better version of top (install it)

# ── FIND SPECIFIC PROCESSES ──
pgrep nginx               # find PIDs of nginx processes
pgrep -a nginx            # find PIDs with full command line
pidof nginx               # same but different tool

# ── PROCESS TREE ──
pstree                    # show process hierarchy as a tree
pstree -p                 # with PIDs
pstree -p 1               # tree starting from PID 1

# ── SIGNALS ──
kill <pid>                # send SIGTERM (graceful stop)
kill -9 <pid>             # send SIGKILL (force kill)
kill -HUP <pid>           # send SIGHUP (reload config)
killall nginx             # kill all processes named nginx
pkill -f "python app.py"  # kill by command line pattern

# ── PROCESS DETAILS ──
cat /proc/<pid>/status    # detailed status
cat /proc/<pid>/cmdline | tr '\0' ' '   # full command
ls /proc/<pid>/fd | wc -l  # count open file descriptors
lsof -p <pid>             # all files/sockets open by process

# ── TRACING ──
strace -p <pid>           # trace system calls live
strace -c -p <pid>        # summarize system calls (count, time)
strace -e open,read,write -p <pid>  # trace specific syscalls only

# ── BACKGROUND JOBS ──
./script.sh &             # run in background
jobs                      # list background jobs
fg %1                     # bring job 1 to foreground
bg %1                     # resume job 1 in background
nohup ./script.sh &       # run in background, survive terminal close
disown %1                 # detach job from terminal
```

---

### cgroups — how Linux limits processes (critical for containers)
cgroups (control groups) allow you to limit and track resource usage for groups of processes. This is the foundation of container resource limits.

What cgroups control:
```
cpu        — CPU time allocation
memory     — memory usage limits (OOMKill happens here)
io         — disk I/O bandwidth
pids       — max number of processes
cpuset     — which CPUs the process can use
```

How Kubernetes uses cgroups:
```yaml
resources:
  requests:
    cpu: "500m"        # 0.5 CPU cores — used for scheduling
    memory: "256Mi"    # 256 MB — used for scheduling
  limits:
    cpu: "1000m"       # 1 CPU core — enforced by cgroup
    memory: "512Mi"    # 512 MB — enforced by cgroup (OOMKill if exceeded)
```

Kubernetes tells the container runtime to create a cgroup with these limits. If the container exceeds the memory limit, the kernel's cgroup(your container uses the host’s kernel. It does NOT have its own kernel.) OOM killer terminates it — that's the `OOMKilled` status you see in `kubectl describe pod`.

<img width="594" height="742" alt="image" src="https://github.com/user-attachments/assets/7ccd36e4-77d8-42c0-9ff4-0a138c075273" />

Checking cgroups for a process:
```bash
# Which cgroups does this process belong to?
cat /proc/<pid>/cgroup

# cgroup v2 memory limit
cat /sys/fs/cgroup/<group>/memory.max

# Current memory usage
cat /sys/fs/cgroup/<group>/memory.current

# CPU quota
cat /sys/fs/cgroup/<group>/cpu.max
```

---

### Namespaces — how Linux isolates processes (containers)
While cgroups limit how much a process can use, namespaces limit what a process can see. Namespaces are the other half of container isolation.

<img width="692" height="411" alt="image" src="https://github.com/user-attachments/assets/21230d60-77b7-418d-9775-543be97c52c1" />

```bash
# On the host, your container process might be PID 5432
# Inside the container, the same process sees itself as PID 1

# Host view:
ps aux | grep myapp
# root  5432  myapp

# Container view (exec into container):
ps aux
# PID  USER  COMMAND
#   1  root  myapp     ← same process, different PID
```

A VM virtualizes the entire hardware — it runs a complete OS kernel. A container uses the host kernel and isolates processes using Linux namespaces (what the process can see) and cgroups (how much resources it can use). Containers are lighter (no guest kernel overhead), start faster (no boot sequence), and share the host kernel. VMs are more isolated (separate kernel = stronger security boundary). Containers share the kernel, so a kernel vulnerability affects all containers on the host


