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
