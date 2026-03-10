# 🖥️ Linux & Bash Mastery for DevOps/SRE/Platform Engineer Interviews
## CATEGORY 2: Process Management — Complete Interview Preparation Guide

> **How to use this guide:** Each topic follows a strict teaching format — concept → internals → interview answer → production example → gotchas. After each topic, decide: **Quiz Me | Go Deeper | Next Topic**.

---

## 📍 Roadmap: Category 2 — Process Management

| # | Topic | Level | Interview Frequency |
|---|-------|-------|-------------------|
| 2.1 | Process basics — PID, PPID, `ps`, `pstree`, foreground/background | 🟢 Beginner | 🔥 Very High |
| 2.2 | Job control — `fg`, `bg`, `jobs`, `&`, `nohup`, `disown` | 🟢 Beginner | 🔥 High |
| 2.3 | `top` and `htop` — load average, CPU, memory columns | 🟢 Beginner | 🔥 Very High |
| 2.4 | Signals & `kill` — SIGTERM, SIGKILL, SIGHUP, SIGINT, trapping | 🟡 Intermediate | 🔥 Very High |
| 2.5 | Process states — R, S, D, Z, T | 🟡 Intermediate | 🔥 High |
| 2.6 | `nice` & `renice` — CPU scheduling priority | 🟡 Intermediate | 🟡 Medium |
| 2.7 | `/proc/PID` internals — cmdline, maps, fd, status, limits | 🟡 Intermediate | 🧠 Deep |
| 2.8 | Linux scheduler — CFS, time slices, cgroups CPU limits | 🔴 Advanced | 🧠 Deep |
| 2.9 | Zombie & orphan processes | 🔴 Advanced | 🔥 High |
| 2.10 | `strace` & `ltrace` — syscall tracing | 🔴 Advanced | 🔥 High |
| 2.11 | `lsof` — open files, sockets, fd leaks | 🔴 Advanced | 🔥 Very High |

---

---

# 🟢 2.1 — Process Basics: PID, PPID, `ps`, `pstree`, Foreground/Background

## 📖 What It Is (Simple Terms)

A **process** is a running instance of a program. When you run `ls`, the kernel creates a process with its own memory space, CPU registers, and file descriptors. Every process gets:

- A **PID** (Process ID) — unique numeric identifier
- A **PPID** (Parent Process ID) — who spawned it
- An **owner** (UID/GID)
- A **state** (running, sleeping, stopped, etc.)

Think of it like a job ticket: each running program gets a unique ticket number (PID), and the ticket records who issued it (PPID).

---

## 🔍 Why It Exists / Problem It Solves

The kernel needs a way to:
1. **Track** all running programs
2. **Allocate** CPU time fairly between them
3. **Isolate** their memory so they don't stomp on each other
4. **Allow communication** between processes (signals, pipes, sockets)
5. **Enable cleanup** — when a process dies, release its resources

---

## ⚙️ How It Works Internally

```
User runs: $ python app.py
          │
          ▼
    bash (PID 1234)
    calls fork()
          │
          ▼
    child process (PID 1235, PPID=1234)
    calls execve("python", ...)
          │
          ▼
    Kernel allocates:
    - Virtual memory space
    - File descriptor table (stdin/stdout/stderr inherited)
    - Entry in /proc/1235/
    - Scheduling slot in the run queue
```

**fork() + exec() model:**
- `fork()` — duplicates the parent process (copy-on-write)
- `exec()` — replaces the process image with the new program
- This is how every process is born in Linux (except PID 1 — init/systemd)

---

## 🔑 Key Concepts

### Process Hierarchy (pstree view)
```
systemd(1)
├── sshd(892)
│   └── sshd(2341)
│       └── bash(2342)
│           └── python(2500) ← your app
├── cron(1204)
└── dockerd(1500)
    └── containerd(1520)
```

### Essential `ps` Commands

```bash
# Snapshot of all processes (BSD-style flags — most universal)
ps aux

# With full path and args
ps auxww

# Show process tree with parent-child relationships
ps auxf

# Show specific PID
ps -p 1234 -o pid,ppid,cmd,%cpu,%mem

# Find process by name
ps aux | grep nginx

# All processes, full format (POSIX-style)
ps -ef

# Show threads too
ps -eLf

# Custom output: pid, name, state, cpu, mem, start time
ps -eo pid,comm,stat,pcpu,pmem,lstart --sort=-%cpu | head -20
```

### `pstree` — Visual Process Tree

```bash
pstree                    # Whole system tree
pstree -p                 # Include PIDs
pstree -u                 # Include usernames
pstree 1234               # Tree rooted at PID 1234
pstree -ap                # Full args + PIDs
```

### Foreground vs Background

```bash
# Run in foreground (blocks the terminal)
python app.py

# Run in background (shell returns immediately)
python app.py &           # & sends to background
# Output: [1] 2500 ← job number, PID

# Check background jobs
jobs
# [1]+  Running    python app.py &

# Bring back to foreground
fg %1                     # %1 = job number 1

# Send running foreground job to background
# Ctrl+Z → suspends it
bg %1                     # resume it in background
```

### Finding PIDs — The Cheat Sheet

```bash
pidof nginx               # All PIDs of processes named nginx
pgrep nginx               # Same, more flexible
pgrep -l nginx            # With names
pgrep -u www-data         # All PIDs owned by www-data
pgrep -P 1234             # All children of PID 1234
```

---

## 🎤 Short Interview Answer

> "A process is a running instance of a program — the kernel creates it via fork()+exec(), assigns it a unique PID, tracks its parent with PPID, and manages its lifecycle through the process table. I use `ps aux` for snapshots, `pstree` to visualize hierarchy, and `pgrep`/`pidof` to find specific processes. In production, understanding PIDs and PPIDs is essential for debugging cascading failures — if a parent dies, you need to know what happens to the children."

---

## 🧬 Deep Dive Version

**The Process Control Block (PCB):**
Every process is represented in the kernel as a `task_struct` (C struct in Linux source). It contains:
- PID, PPID, process group ID, session ID
- State (TASK_RUNNING, TASK_INTERRUPTIBLE, etc.)
- Memory map (mm_struct)
- File descriptor table
- Signal handlers
- CPU registers (saved when context-switching)
- Scheduling priority

**`/proc` filesystem:**
Every process gets a directory `/proc/PID/`:
```bash
ls /proc/$(pgrep nginx | head -1)/
# cmdline  cwd  environ  exe  fd  maps  mem  net  stat  status
```

**Copy-On-Write (COW) fork:**
When fork() is called, the kernel doesn't immediately copy the parent's memory pages — it marks them as shared and read-only. Only when either process tries to write does it copy that specific page. This makes fork() fast — forking a 2GB process is nearly instant.

---

## 🏭 Real Production Example

**Scenario: App server appears hung, users getting 502s**

```bash
# Step 1: Find the process
pgrep -l gunicorn
# 1847 gunicorn
# 1849 gunicorn
# 1850 gunicorn

# Step 2: Check process tree — is master still running?
pstree -p 1847
# gunicorn(1847)─┬─gunicorn(1849)
#                └─gunicorn(1850)

# Step 3: Check what state they're in
ps -p 1847,1849,1850 -o pid,stat,pcpu,pmem,etime,cmd
# PID  STAT  %CPU  %MEM  ELAPSED  CMD
# 1847 S      0.0   1.2  02:15:42 gunicorn master
# 1849 D      99.9  12.4 00:00:03 gunicorn worker  ← D-state! stuck in I/O!
# 1850 S      0.0   1.1  02:15:40 gunicorn worker

# Step 4: Worker 1849 is stuck in D-state (uninterruptible sleep)
# Likely cause: NFS mount hung, disk I/O wait, or DB connection blocked
# Cannot be killed with SIGKILL while in D-state
# → Restart the worker, investigate I/O subsystem
```

---

## 💬 Common Interview Questions

**Q: What's the difference between `ps aux` and `ps -ef`?**
> Both list all processes, but they use different flag styles. `ps aux` uses BSD-style flags (no dash) and shows %CPU/%MEM columns. `ps -ef` uses POSIX/SysV-style (with dash) and shows STIME (start time) and C (CPU usage). In practice, `ps aux` is more commonly used in DevOps contexts. The underlying data comes from `/proc` in both cases.

**Q: How does a child process get created?**
> Via `fork()` followed by `exec()`. `fork()` creates a copy of the parent process using copy-on-write semantics — both parent and child share the same memory pages until one writes to them. Then `exec()` replaces the child's program image with the new program. This fork+exec model is fundamental to how shells spawn commands.

**Q: What happens to child processes when the parent dies?**
> They become **orphans** and are re-parented to PID 1 (init/systemd). This is by design — init/systemd will then reap them when they exit. If a parent exits without waiting for its children's exit status, those children become **zombie processes** (covered in 2.9).

---

## ⚠️ Gotchas & Edge Cases

1. **`ps aux` shows a snapshot, not real-time** — if a process is spawning and dying rapidly, you might miss it. Use `watch -n 0.5 'ps aux | grep app'` for near-realtime.

2. **Zombie processes show in `ps` with state `Z`** — they have a PID entry but no resources. You **cannot kill** a zombie — only its parent can reap it via `wait()`.

3. **PID 1 is special** — init/systemd. If PID 1 dies, the system panics. Inside Docker containers, your entrypoint process IS PID 1 — which means if it doesn't handle signals properly, `docker stop` hangs for 10 seconds before SIGKILL.

4. **`ps aux` column header `VSZ` vs `RSS`** — VSZ is virtual memory (includes mmap'd files, not all in RAM), RSS is Resident Set Size (actually in RAM). VSZ is almost always much larger than RSS and can be misleading.

5. **`%CPU` in `ps` is averaged over process lifetime**, not instantaneous. Use `top` for current CPU usage.

---

## 🔗 Connected Concepts

- **Signals (2.4)** — How you communicate with or terminate processes
- **Process states (2.5)** — What `STAT` column in `ps` means
- **`/proc/PID` internals (2.7)** — Where all process info really lives
- **Zombie processes (2.9)** — What happens when parents don't reap children
- **cgroups (2.8)** — How container runtimes isolate process resources
- **`lsof` (2.11)** — Inspecting what files/sockets a process has open

---
---

# 🟢 2.2 — Job Control: `fg`, `bg`, `jobs`, `&`, `nohup`, `disown`

## 📖 What It Is (Simple Terms)

**Job control** is the shell's ability to manage multiple processes from a single terminal. You can run commands in the background, suspend them, bring them back, and detach them completely from the terminal session.

Think of it like a restaurant kitchen — you're the head chef (shell), and jobs are dishes at different stages: some actively cooking on the stove (foreground), some in the oven (background), some paused waiting for ingredients (stopped).

---

## 🔍 Why It Exists / Problem It Solves

Before job control, if you started a long-running command (e.g., `tar` a large directory), you were stuck — you couldn't do anything else until it finished. Job control lets you:
- Run multiple things in one terminal
- Suspend and resume tasks
- Detach processes from the terminal so they survive logout

---

## ⚙️ How It Works Internally

```
Terminal (TTY)
    │
    ▼
bash (session leader, PID 1234)
    │
    ├── Foreground process group ← gets keyboard input, signals from Ctrl+C/Z
    │   └── command_1 (PID 1300)
    │
    └── Background process groups ← no keyboard input
        ├── command_2 (PID 1400) [Running]
        └── command_3 (PID 1500) [Stopped/Suspended]
```

**Key mechanism: Process Groups + TTY**
- Each shell job is a **process group** (PGID)
- The terminal's foreground process group receives keyboard signals (SIGINT from Ctrl+C, SIGTSTP from Ctrl+Z)
- Background jobs don't get these signals — they run silently

---

## 🔑 Key Commands

```bash
# Run a command in the background
sleep 100 &
# [1] 1847 ← job number, PID

# List current jobs
jobs
# [1]+  Running    sleep 100 &
# [2]-  Stopped    vim file.txt

jobs -l   # Include PIDs
jobs -p   # PIDs only

# Bring job 1 to foreground
fg %1
fg        # Brings the "current" job (marked +) to foreground

# Send a foreground job to background
# First: Ctrl+Z   → suspends the job
# Then:
bg %1             # resumes it in background

# Shorthand for job references
fg %sleep         # by command name
fg %%             # current job
fg %+             # current job (same)
fg %-             # previous job

# Disconnect a job from the shell completely
nohup python long_task.py &
# Output goes to nohup.out by default

# Redirect nohup output explicitly
nohup python long_task.py > /var/log/task.log 2>&1 &

# Disown — remove job from shell's job table
python app.py &
disown %1         # Shell no longer tracks it, won't send SIGHUP on logout
disown -h %1      # Mark as "no SIGHUP" but keep in jobs table
disown -a         # Disown all jobs
```

### `nohup` vs `disown` — Side by Side

| Feature | `nohup cmd &` | `cmd & disown` |
|---------|--------------|----------------|
| Immune to SIGHUP | ✅ Yes | ✅ Yes |
| Appears in `jobs` | ✅ Initially | ❌ After disown |
| Output handling | Redirects to nohup.out | Unchanged (may lose output) |
| Can use with existing process | ❌ No (must prefix) | ✅ Yes (after starting) |
| Use case | Starting a new daemonized task | Already-running process you forgot to nohup |

---

## 🎤 Short Interview Answer

> "Job control lets you manage multiple processes from one terminal. `&` puts a job in the background, `Ctrl+Z` suspends it, `fg`/`bg` move jobs between foreground and background. For processes that need to survive terminal logout, I use `nohup cmd &` before starting, or `disown` on an already-running background job. In production I'd prefer systemd services or tmux for long-running tasks, but `nohup`/`disown` are lifesavers when you're on a remote server and accidentally started something in a shell that's about to close."

---

## 🏭 Real Production Example

**Scenario: You SSH into a server and start a database migration, then realize your VPN might drop**

```bash
# You already started it in foreground — oops
# Ctrl+Z to suspend
^Z
# [1]+  Stopped    python migrate.py

# Move to background and detach
bg %1
disown %1

# Verify it's running (no longer in jobs, but in ps)
jobs         # empty
ps aux | grep migrate.py   # still there!

# Better: use screen or tmux next time
# But for the already-running case, disown saves you
```

---

## 💬 Common Interview Questions

**Q: What's the difference between `nohup` and `disown`?**
> `nohup` is used when starting a process — it sets the process to ignore SIGHUP and redirects output to nohup.out. `disown` works on an already-running background job in the current shell — it removes it from the shell's job table so the shell won't send SIGHUP to it on logout. The protection is similar, but the use case differs: `nohup` = proactive, `disown` = retroactive.

**Q: What happens to background jobs when you close the terminal?**
> The shell sends **SIGHUP** to all jobs in its job table when the controlling terminal closes. By default, this terminates them. `nohup` ignores SIGHUP at process start; `disown` removes the job from the table so it never receives the signal. Processes started without these precautions will die when you log out.

**Q: What is `Ctrl+Z` actually doing?**
> It sends **SIGTSTP** (signal 20) to the foreground process group, causing the processes to stop (not terminate). The process stays in memory in a `T` (stopped) state, preserving all state and memory, until it receives SIGCONT to resume.

---

## ⚠️ Gotchas & Edge Cases

1. **`nohup` doesn't background the process** — `nohup cmd` still runs in foreground. You need `nohup cmd &` to background it.

2. **Output from disowned jobs can corrupt your terminal** — if you `disown` a job that's writing to stdout, it'll still write to your terminal. Redirect first: `cmd > output.log 2>&1 & disown`.

3. **`jobs` is shell-specific** — it only shows jobs of the current shell instance. If you open a new terminal, you won't see jobs from the old one. This catches people off-guard when SSHing into a server from multiple windows.

4. **Job numbers reset** — job numbers `[1]`, `[2]` are per-shell-session. PIDs are system-wide and permanent (until process dies).

5. **`screen` and `tmux` are better for production** — job control is fine for ad-hoc tasks, but for anything important use a terminal multiplexer so you can reattach from any session.

---

## 🔗 Connected Concepts

- **Signals (2.4)** — SIGHUP, SIGTSTP, SIGCONT are the signals job control sends
- **`nohup` and daemons** — how background services avoid terminal dependency
- **Process groups and sessions** — the kernel mechanism behind job control
- **`tmux`/`screen`** — production alternative to raw job control

---
---

# 🟢 2.3 — `top` and `htop`: Reading Load Average, CPU, Memory

## 📖 What It Is (Simple Terms)

`top` is a real-time system monitor — it shows you what's consuming CPU and memory right now, updated every few seconds. `htop` is a more user-friendly, interactive version.

Think of `top` as the **dashboard of a running car** — it shows you speed (CPU), fuel level (memory), engine temperature (load average), all at a glance.

---

## 🔍 Why It Exists / Problem It Solves

When a system is slow or a server is struggling, you need to quickly answer:
- Is CPU the bottleneck or memory?
- Which process is the culprit?
- Is the system actually overloaded or just momentarily busy?
- Is there memory pressure causing swapping?

`top` answers all of this in one screen.

---

## ⚙️ How It Works Internally

`top` reads from `/proc` every refresh interval:
- `/proc/stat` — system-wide CPU stats
- `/proc/meminfo` — memory stats
- `/proc/[PID]/stat` — per-process CPU/memory
- `/proc/[PID]/status` — per-process state

It calculates the **delta** between reads to get CPU% (how much of each interval a process used).

---

## 🔑 Key Concepts

### 🔥 Load Average — The Most Misunderstood Metric

```
top - 14:23:01 up 42 days,  3:15,  2 users,  load average: 1.85, 2.10, 1.93
```

**Load average = average number of processes that are RUNNABLE or in UNINTERRUPTIBLE wait (D-state) over the last 1, 5, 15 minutes.**

```
Load average: 1.85  (last 1 min)
              2.10  (last 5 min)  ← trend going down from 5-min peak
              1.93  (last 15 min)
```

**How to interpret:**
```
# Single-core machine:
Load = 1.0  → 100% utilized, no queue
Load = 2.0  → 200% = 1 running + 1 waiting → overloaded!

# 4-core machine:
Load = 1.0  → 25% utilized → no problem
Load = 4.0  → 100% utilized → fully loaded but manageable
Load = 8.0  → 200% = overloaded!

# Rule: Load / CPU cores = real utilization
# If ratio > 1.0 persistently → system is overloaded
```

```bash
# Get CPU count
nproc
grep -c processor /proc/cpuinfo

# Quick load check
uptime
# 14:23:01 up 42 days, load average: 1.85, 2.10, 1.93
```

### `top` Header — Annotated

```
top - 14:23:01 up 42 days,  2 users,  load average: 1.85, 2.10, 1.93
Tasks: 312 total,   1 running, 311 sleeping,   0 stopped,   0 zombie
%Cpu(s):  5.2 us,  1.3 sy,  0.0 ni, 92.1 id,  1.1 wa,  0.0 hi,  0.3 si
MiB Mem :  15842.8 total,   1204.4 free,  11382.2 used,   3256.2 buff/cache
MiB Swap:   2048.0 total,   1834.2 free,    213.8 used.   2845.3 avail Mem
```

**CPU line breakdown:**
| Field | Meaning | Alert if... |
|-------|---------|------------|
| `us` | User space CPU % | > 70% sustained |
| `sy` | Kernel/system CPU % | > 30% (too many syscalls) |
| `ni` | Niced processes % | Informational |
| `id` | Idle % | < 10% = system is busy |
| `wa` | I/O Wait % | **> 10% = I/O bottleneck** |
| `hi` | Hardware interrupt % | High = driver or HW issue |
| `si` | Software interrupt % | High = network overload |

**Memory line breakdown:**
```
MiB Mem: 15842 total, 1204 free, 11382 used, 3256 buff/cache
                                              ↑
                            This is "available" for processes if needed
                            Free + buff/cache = effectively free
                            
avail Mem: 2845  ← This is what matters! Real available memory
```

> ⚠️ **Common mistake:** `free` memory looks low but `avail Mem` is fine — Linux aggressively uses free RAM for buffer/cache (which can be reclaimed). Panicking about low `free` without checking `avail` is a classic junior mistake.

### Process Columns in `top`

```
  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 1234 www-data  20   0 1.2g    500m   10m R  89.3   3.2   2:15.33 python
```

| Column | Meaning |
|--------|---------|
| `PID` | Process ID |
| `PR` | Kernel priority (20 = default, lower = higher priority) |
| `NI` | Nice value (-20 to 19, lower = higher priority) |
| `VIRT` | Virtual memory (total address space, includes all mmap'd files) |
| `RES` | Resident Set Size — actual RAM used |
| `SHR` | Shared memory (shared libs, etc.) |
| `S` | State (R/S/D/Z/T) |
| `%CPU` | CPU usage since last refresh |
| `%MEM` | RES / total RAM |
| `TIME+` | Total CPU time consumed |

### `top` Interactive Keys

```bash
top
# Inside top:
k          # Kill a process (prompts for PID + signal)
r          # Renice a process
q          # Quit
1          # Toggle per-CPU breakdown
M          # Sort by memory
P          # Sort by CPU (default)
T          # Sort by cumulative time
f          # Field/column selector
u          # Filter by user
H          # Toggle thread view
s          # Change refresh interval
```

### `htop` Advantages

```bash
# Install if not present
apt install htop   # Debian/Ubuntu
yum install htop   # RHEL/CentOS

htop
# Features over top:
# - Color-coded CPU/memory bars
# - Mouse support
# - F3: search by name
# - F4: filter
# - F5: tree view (like pstree)
# - F6: sort column
# - F9: kill menu (shows signal choices)
# - Horizontal scroll to see full commands
```

### One-Liners for Production

```bash
# Top 5 CPU-consuming processes right now (non-interactive)
ps aux --sort=-%cpu | head -6

# Top 5 memory consumers
ps aux --sort=-%mem | head -6

# Check load every second
watch -n 1 uptime

# Log load average every minute
while true; do date; uptime; sleep 60; done >> /var/log/load.log

# Non-interactive top output (batch mode, 1 iteration)
top -b -n 1 | head -20

# Show per-CPU stats
mpstat -P ALL 1 3   # requires sysstat package
```

---

## 🎤 Short Interview Answer

> "Load average represents the average number of processes competing for CPU or blocked in uninterruptible I/O over 1, 5, and 15 minutes. To interpret it meaningfully you divide by the number of CPU cores — a load of 4.0 on a 4-core machine is 100% utilized, while on a single-core machine it's 4x overloaded. When I look at `top`, I focus first on the CPU `wa` (I/O wait) and `us` columns, then memory's `avail Mem` — not `free`, because Linux caches disk I/O in unused RAM which looks like low free memory but is actually healthy."

---

## 🏭 Real Production Example

**Scenario: Alert fires — app response time spiked from 50ms to 5s**

```bash
# SSH to server, immediately run top
top

# See: load average: 18.2, 12.1, 8.5 (server has 8 cores → 2x overloaded)
# CPU: us 4.2, sy 2.1, wa 89.3  ← 89% I/O WAIT
# Memory: avail 12GB → not the problem

# High wa = I/O bottleneck. Something is hammering disk or network storage.

# Find the D-state processes (waiting on I/O)
ps aux | awk '$8 ~ /D/ {print}'

# Check disk I/O
iostat -x 1 3

# Output shows /dev/sdb at 100% utilization
# Identify which process is writing to /dev/sdb
iotop -o    # Shows only active I/O processes

# Root cause: Log rotation script running tar on 100GB logs to NFS
# Fix: Move log rotation to off-peak hours, use async compression
```

---

## 💬 Common Interview Questions

**Q: Server load average is 25 — is that a problem?**
> It depends on how many CPU cores the server has. Run `nproc` to find out. If it's a 32-core machine, load 25 means ~78% utilized — totally fine. If it's a 4-core machine, load 25 means 6x overloaded — severe problem. Also check the trend: is load 25 coming down from 40 (recovering) or going up from 10 (getting worse)?

**Q: Memory shows only 200MB free — should I be worried?**
> Not necessarily. Linux uses spare RAM as disk cache (buff/cache). The key metric is `avail Mem` (or `free -h`'s available column), which shows how much memory can be given to applications. If `avail Mem` is healthy (say 4GB), the system is fine even with only 200MB "free." Only worry if `avail Mem` is critically low and swap is being heavily used.

**Q: What does high `wa` (I/O wait) mean?**
> It means CPUs are idle waiting for I/O operations to complete — disk reads/writes or network-attached storage. The fix is almost never "add more CPU" — it's to identify and reduce the I/O bottleneck: optimize queries to avoid full table scans, move to faster storage, reduce write amplification, or schedule I/O-heavy tasks during off-peak hours.

---

## ⚠️ Gotchas & Edge Cases

1. **Load average includes D-state processes** — a stuck NFS mount with 10 processes blocked on it can spike load average to 10+, even with CPUs idle. You'd see `wa` high but `us` low. Classic NFS/storage incident pattern.

2. **`%CPU` in top can exceed 100%** — on multi-core systems, a multi-threaded process can use 400% CPU on a 4-core machine (each core 100%). This is normal and good.

3. **top's CPU % is since last refresh, not total lifetime** — unlike `ps`'s TIME+ which is cumulative.

4. **Swap usage as a warning sign** — if swap is actively being used (check `si`/`so` in `vmstat`), the system is paging, which is orders of magnitude slower than RAM and will cause serious performance degradation.

5. **`VIRT` is almost always misleadingly large** — don't panic about a process showing 10GB VIRT if `RES` is only 500MB. VIRT includes mmap'd files, reserved but not allocated memory, shared libraries, etc.

---

## 🔗 Connected Concepts

- **Process states (2.5)** — explains the R/S/D/Z/T in top's S column
- **CFS scheduler (2.8)** — explains PR/NI columns and how CPU time is divided
- **`nice`/`renice` (2.6)** — controls the NI column
- **`/proc/meminfo`, `/proc/stat`** — raw data sources that top reads
- **`iotop`, `iostat`** — drill down on I/O when `wa` is high

---
---

# 🟡 2.4 — Signals & `kill`: SIGTERM, SIGKILL, SIGHUP, SIGINT, Trapping

## 🔥 High Frequency Interview Topic

## 📖 What It Is (Simple Terms)

Signals are **asynchronous notifications** sent to processes — the kernel's way of saying "something happened, deal with it." They're like a phone call to a process: it can answer (handle it), ignore it, or in some cases, the call can't be blocked (SIGKILL).

---

## 🔍 Why It Exists / Problem It Solves

You need a way to:
- Gracefully stop a process (let it clean up)
- Forcefully kill a hung process
- Tell a daemon to reload its config without restarting
- Notify a process that a terminal closed or user pressed Ctrl+C

Signals provide a standardized mechanism for all of these.

---

## ⚙️ How It Works Internally

```
Signal Flow:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source                   Kernel                    Target Process
──────               ─────────────              ─────────────────
kill -15 PID  ──►  Sets pending signal   ──►  Process checks signal
Ctrl+C        ──►  bit in task_struct    ──►  at next scheduling
Hardware      ──►                             point or syscall return
Kernel self   ──►                                │
                                                 ▼
                                         Signal handler runs:
                                         - DEFAULT action (kill/stop/ignore)
                                         - Custom handler (if registered)
                                         - SIG_IGN (if ignored)
```

**Signal delivery happens:**
- When returning from a system call
- When the process is scheduled after being in sleep state
- Immediately for signals that wake the process

---

## 🔑 Key Signals — The Essential Table

| Signal | Number | Default Action | Can Catch/Ignore? | Common Use |
|--------|--------|----------------|-------------------|------------|
| `SIGTERM` | 15 | Terminate | ✅ Yes | Graceful shutdown request |
| `SIGKILL` | 9 | Kill immediately | ❌ NO | Force kill — last resort |
| `SIGHUP` | 1 | Terminate | ✅ Yes | Reload config / terminal closed |
| `SIGINT` | 2 | Terminate | ✅ Yes | Ctrl+C — interrupt |
| `SIGQUIT` | 3 | Core dump | ✅ Yes | Ctrl+\ — quit with core |
| `SIGSTOP` | 19 | Stop process | ❌ NO | Pause (like Ctrl+Z) |
| `SIGTSTP` | 20 | Stop process | ✅ Yes | Ctrl+Z — soft stop |
| `SIGCONT` | 18 | Continue | ✅ Yes | Resume a stopped process |
| `SIGUSR1` | 10 | Terminate | ✅ Yes | User-defined (app-specific) |
| `SIGUSR2` | 12 | Terminate | ✅ Yes | User-defined (app-specific) |
| `SIGCHLD` | 17 | Ignore | ✅ Yes | Child process changed state |
| `SIGPIPE` | 13 | Terminate | ✅ Yes | Broken pipe (write to closed fd) |
| `SIGALRM` | 14 | Terminate | ✅ Yes | Timer expired |

> ⚠️ **SIGKILL (9) and SIGSTOP (19) CANNOT be caught, blocked, or ignored.** They are handled directly by the kernel, bypassing any process-level handlers.

---

## 🔑 `kill` Command Usage

```bash
# Send SIGTERM (default) — ask nicely
kill 1234
kill -15 1234
kill -TERM 1234
kill -SIGTERM 1234

# Send SIGKILL — force kill
kill -9 1234
kill -KILL 1234

# Send SIGHUP — reload config
kill -1 1234
kill -HUP 1234

# Kill all processes named nginx
killall nginx
killall -9 nginx

# Kill all processes matching pattern
pkill nginx
pkill -9 -f "gunicorn.*worker"   # -f matches full command line
pkill -HUP nginx                  # Send SIGHUP to reload

# List all signal names/numbers
kill -l
```

### Graceful Shutdown Sequence (Production Pattern)

```bash
# Step 1: Try graceful shutdown
kill -TERM $PID
sleep 10

# Step 2: Check if it's still running
if kill -0 $PID 2>/dev/null; then
    echo "Process still running after SIGTERM, forcing..."
    kill -KILL $PID
fi

# kill -0 doesn't send a signal — just checks if PID exists and you have permission
```

---

## 🔑 Trapping Signals in Bash Scripts

```bash
#!/bin/bash

# Clean up temp files if script is interrupted
TMPFILE=$(mktemp)

cleanup() {
    echo "Cleaning up..."
    rm -f "$TMPFILE"
    exit 0
}

# Register signal handlers
trap cleanup SIGTERM SIGINT SIGHUP

# Also handle: trap cleanup EXIT  (runs on any exit)

echo "Working with $TMPFILE"
# ... do work ...
sleep 60

# The cleanup function will run if you Ctrl+C or kill -15 this script
```

### Advanced Trap Patterns

```bash
# Trap EXIT to always clean up
trap 'rm -f /tmp/lockfile; echo "Exiting"' EXIT

# Trap ERR to catch script errors
trap 'echo "Error on line $LINENO"; exit 1' ERR

# Ignore a signal
trap '' SIGINT    # Makes Ctrl+C do nothing

# Reset to default
trap - SIGINT     # Restore default SIGINT behavior

# Reload config on SIGHUP (daemon pattern)
reload_config() {
    echo "Reloading config..."
    source /etc/myapp/config.conf
}
trap reload_config SIGHUP

# Self-signal for deferred actions
defer_action() { echo "Deferred!"; }
trap defer_action SIGUSR1
kill -USR1 $$   # $$ = current script PID
```

---

## 🎤 Short Interview Answer

> "Signals are asynchronous notifications the kernel sends to processes. SIGTERM (15) asks a process to terminate gracefully — it can be caught and handled. SIGKILL (9) cannot be caught or ignored and immediately destroys the process. SIGHUP (1) traditionally meant the terminal hung up — daemons reuse it as a 'reload config' signal. In Bash scripts I use `trap` to register cleanup handlers so temp files and locks are cleaned up even if the script is interrupted. In production, I always try SIGTERM first with a timeout, then SIGKILL as a last resort — killing with -9 first can leave databases in inconsistent states or leave lock files behind."

---

## 🏭 Real Production Example

**Scenario: Graceful rolling restart of a web application**

```bash
#!/bin/bash
# graceful_restart.sh — restarts app workers one at a time

APP_NAME="gunicorn"
MASTER_PID=$(pgrep -f "gunicorn.*master")

echo "Master PID: $MASTER_PID"

# Get worker PIDs
WORKERS=$(pgrep -P $MASTER_PID)

for pid in $WORKERS; do
    echo "Gracefully restarting worker $pid..."
    
    # SIGUSR1 = gunicorn worker graceful stop (finish current request, then stop)
    kill -USR1 $pid
    
    # Wait for it to stop and new worker to start
    sleep 5
    
    # Verify it stopped
    if kill -0 $pid 2>/dev/null; then
        echo "Worker $pid didn't stop, forcing..."
        kill -9 $pid
    fi
done

echo "All workers restarted"

# nginx: reload config without downtime
nginx -t && kill -HUP $(cat /var/run/nginx.pid)
```

---

## 💬 Common Interview Questions

**Q: When would you use SIGKILL vs SIGTERM?**
> Always try SIGTERM first — it gives the application a chance to flush buffers, close database connections, release locks, and write a clean shutdown log. SIGKILL is for processes that are hung and not responding to SIGTERM, or processes in an infinite loop that are ignoring signals. The risk of SIGKILL is data corruption (if the process was mid-write), dirty database states, and orphaned lock files.

**Q: What happens to child processes when the parent receives SIGKILL?**
> SIGKILL only kills the target process — its children are NOT automatically killed. They become orphans and get re-parented to PID 1 (systemd/init). If you need to kill an entire process tree, use `kill -- -PGID` (send signal to the process group) or `pkill -P $PID` to kill children first.

**Q: How do daemons use SIGHUP?**
> Originally, SIGHUP meant "the controlling terminal hung up" — which was a reason to terminate. Since daemons don't have a controlling terminal, developers repurposed SIGHUP as a "reload your configuration" signal. Examples: `nginx -s reload` sends SIGHUP to the master process; `kill -HUP $(pidof sshd)` reloads sshd config; logrotate uses SIGHUP to tell apps to reopen log files after rotation.

**Q: What is `kill -0`?**
> Signal 0 is a special "null signal" — it doesn't actually send a signal, but it performs all the error checking (permission checks, process existence). If `kill -0 $PID` returns 0, the process exists and you have permission to signal it. Return code 1 means either the process doesn't exist or you don't have permission. Used in scripts to check if a process is alive.

---

## ⚠️ Gotchas & Edge Cases

1. **SIGKILL on a D-state process** — A process in uninterruptible sleep (D state, waiting on I/O) will NOT be killed by SIGKILL immediately. The signal is pending but can't be delivered until the process returns from the I/O wait. If the I/O never completes (hung NFS mount), the process cannot be killed without fixing the underlying I/O issue or rebooting.

2. **`killall` is dangerous** — `killall nginx` kills ALL processes named nginx, including potential nginx processes belonging to other users or running in containers with shared PID namespaces. Use `pkill -f` with a more specific pattern or kill by PID.

3. **Bash traps are inherited by subshells** (sometimes) — trap handlers set in a parent script may or may not be inherited by subshells depending on how they're invoked. Use `( trap - SIGTERM; exec child_command )` to reset traps in a subshell.

4. **SIGPIPE gotcha** — a pipeline like `curl | grep | head -1` will get SIGPIPE sent to `curl` when `head` exits after the first line. Many tools ignore SIGPIPE, but some don't. If your script has `set -e` (exit on error), a non-zero exit from a SIGPIPE can cause unexpected script termination.

5. **Docker SIGTERM timeout** — `docker stop` sends SIGTERM, waits 10 seconds, then sends SIGKILL. If PID 1 in your container doesn't handle SIGTERM (e.g., you're using a shell script as entrypoint without `exec`), the 10-second grace period is wasted and the container is force-killed.

---

## 🔗 Connected Concepts

- **Process states (2.5)** — D state processes can't be killed
- **Job control (2.2)** — SIGTSTP, SIGCONT used by fg/bg
- **Zombie processes (2.9)** — SIGCHLD is how parents know children died
- **Bash scripting** — `trap` for cleanup and resilience
- **Docker/containers** — proper PID 1 signal handling

---
---

# 🟡 2.5 — Process States: R, S, D, Z, T

## 🔥 High Frequency Topic — Direct Connection to Production Debugging

## 📖 What It Is (Simple Terms)

Every process is in exactly one state at any moment — it tells you what the process is currently doing (or waiting for). The state appears in `ps` output under the `STAT` or `S` column.

---

## ⚙️ State Machine Diagram

```
                    ┌────────────────────────────────┐
                    │                                │
          fork()    ▼          schedule()            │
[Created] ──────► [R - Runnable] ◄──────────── [S - Sleeping]
                    │     ▲                          ▲
               CPU  │     │ preempt                  │  event
               runs ▼     │                          │  arrives
                  [Running]─────────────────────────►│
                    │          I/O, sleep()           │
                    │
                    ├──── slow I/O, kernel wait ────► [D - Uninterruptible Sleep]
                    │                                      │
                    ├──── Ctrl+Z / SIGSTOP ─────────► [T - Stopped]
                    │                                      │
                    │                              SIGCONT │
                    │◄─────────────────────────────────────┘
                    │
                    └──── exit() ────────────────── [Z - Zombie]
                                                         │
                                               parent wait() ──► [Gone]
```

---

## 🔑 Process State Reference

### R — Running or Runnable

```bash
ps aux | awk '$8 == "R" {print}'
```

- Process is currently on a CPU OR is in the run queue ready to run
- Normal for active processes
- Multiple `R` state processes = CPU contention if more than CPU cores

### S — Interruptible Sleep

```bash
# Most processes are in S state most of the time
ps aux | awk '$8 == "S" {print}' | wc -l
```

- Waiting for an event: keyboard input, network data, timer, signal
- Can be woken up by a signal (hence "interruptible")
- This is healthy — processes should spend most of their time here
- Example: nginx worker waiting for a connection, bash waiting for you to type

### ⚠️ D — Uninterruptible Sleep (DISK WAIT)

```bash
# Find D-state processes — critical for diagnosing I/O hangs
ps aux | awk '$8 ~ /^D/ {print}'
```

- Waiting for I/O that **cannot be interrupted** by signals — not even SIGKILL
- Kernel needs this guarantee for consistency (e.g., can't interrupt mid-filesystem-write)
- **Brief D-state = normal** (disk writes happen)
- **Sustained D-state = severe problem**: hung NFS, slow disk, storage system issue
- High D-state count = the cause of high load average without high CPU

```bash
# Production diagnostic when load is high but CPUs idle:
ps -eo pid,stat,wchan,comm | grep "^[0-9]* D"
# WCHAN shows what kernel function the process is stuck in
# "nfs_execute_op" → NFS hang
# "jbd2_log_wait" → ext4 journal wait
```

### Z — Zombie

```bash
ps aux | awk '$8 == "Z" {print}'
```

- Process has exited but parent hasn't called `wait()` to collect exit status
- Has NO memory, NO CPU — just a row in the process table
- **Cannot be killed** (it's already dead!)
- The slot is reserved until parent reads the exit status
- Small number of zombies = normal; large numbers = parent has a bug
- Fix: Fix the parent application, or kill the parent (kernel re-parents to init which reaps them)

### T — Stopped

```bash
ps aux | awk '$8 == "T" {print}'
```

- Suspended — received SIGSTOP or SIGTSTP (Ctrl+Z)
- Not using CPU, stays in memory
- Resumes with SIGCONT
- Also appears during debugging with `gdb` (ptrace stops the process)

### Additional State Flags (Modifiers)

```
STAT column can have multiple characters:
R    = Running
S    = Sleeping
D    = Uninterruptible sleep
Z    = Zombie
T    = Stopped

Modifiers:
s    = Session leader (e.g., Ss = sleeping session leader)
l    = Multi-threaded
+    = Foreground process group
<    = High priority (negative nice value)
N    = Low priority (positive nice value)
L    = Has locked pages in memory (real-time)

Example:
Ss   = sleeping, session leader (typical for master daemon)
S+   = sleeping, foreground
Sl   = sleeping, multi-threaded
R<   = running, high priority
```

---

## 🎤 Short Interview Answer

> "There are five main process states. R means running or ready to run. S means sleeping — waiting for an event like I/O or a signal — this is the normal state for most processes. D is uninterruptible sleep, waiting on kernel I/O — this state cannot be killed with SIGKILL and prolonged D-state usually indicates a storage problem like a hung NFS mount. Z is zombie — the process has exited but its parent hasn't called wait() to collect the exit status, leaving a dead process table entry. T is stopped, usually by Ctrl+Z or SIGSTOP. In production, I watch for D-state processes whenever load average is high but CPUs are mostly idle — it's the classic storage bottleneck signature."

---

## 🏭 Real Production Example

**Alert: Load average = 45 on a 16-core server. CPUs show 5% usage. What's happening?**

```bash
# Step 1: Count process states
ps -eo stat | sort | uniq -c | sort -rn
# 180 S    ← mostly sleeping (normal)
#  38 D    ← 38 D-state processes! This is the problem
#   2 R
#   1 Ss

# Step 2: Identify what D-state processes are waiting on
ps -eo pid,stat,wchan,comm | awk '$2~/D/{print}'
# PID   STAT  WCHAN            COMMAND
# 1234  D     nfs_execute_op   java
# 1235  D     nfs_execute_op   java
# ...38 total all stuck on NFS

# Step 3: Check NFS mount
df -h   # hangs! (df tries to stat all filesystems)
mount | grep nfs
# 10.0.1.50:/data on /mnt/nfs type nfs (rw,relatime)

# Step 4: Check connectivity to NFS server
ping 10.0.1.50    # no response → NFS server down!

# Step 5: Mitigation
# Can't kill those processes (they're in D-state with SIGKILL pending but not delivered)
# Options:
# 1. Restore NFS server → processes auto-recover
# 2. Force unmount: umount -l /mnt/nfs (lazy unmount)
# 3. Last resort: reboot

umount -l /mnt/nfs   # lazy unmount — detaches from filesystem namespace
# D-state processes now get EIO error, transition to R, then exit or handle error
```

---

## 💬 Common Interview Questions

**Q: Can you kill a zombie process?**
> No — a zombie is already dead. It has no memory, no CPU, no resources. You can't kill it directly. The only way to remove it is for its parent process to call `wait()` (or `waitpid()`) to collect its exit status, which removes the process table entry. If the parent is buggy and never calls wait, you can kill the parent — the kernel will then re-parent the zombies to PID 1 (systemd), which periodically reaps orphaned zombies.

**Q: Why can't SIGKILL kill a D-state process?**
> D-state (uninterruptible sleep) means the process is executing a kernel code path that cannot be safely interrupted — for example, it's in the middle of a filesystem operation where stopping partway would leave data structures inconsistent. SIGKILL is technically delivered (pending bit is set), but it won't be acted on until the process exits the uninterruptible section. If the I/O operation never completes (e.g., NFS server is down), the process is stuck indefinitely. This is a kernel design decision for data integrity.

**Q: What does a high count of D-state processes tell you?**
> It strongly indicates an I/O subsystem problem. Most commonly: NFS mount is hung or slow, disk is failing or saturated, SAN/NAS latency has spiked, or a storage driver has a bug. The load average will be high (D-state contributes to load), but CPU usage will be low. This is a key diagnostic pattern — "high load, low CPU" → look for D-state processes.

---

## ⚠️ Gotchas & Edge Cases

1. **Zombie processes don't consume memory or CPU** — they're just a table entry. A few zombies are harmless. Only care if there are thousands (exhausts PID space or indicates a systemic parent bug).

2. **Process can be in D state on network I/O too** — not just disk. A `read()` on a TCP socket that's in kernel-level blocking I/O can show as D. More commonly seen with NFS (which uses kernel-level RPC), not regular user-space network I/O.

3. **Load average counts D-state processes** — this is why high load + low CPU is a storage problem, not a compute problem. Adding more CPUs won't fix it.

4. **Zombie processes can block reuse of PIDs** — Linux has a PID limit (default 32768, adjustable via `/proc/sys/kernel/pid_max`). If you have thousands of zombies, they consume PID table space. Eventually no new processes can be created.

---

## 🔗 Connected Concepts

- **Signals (2.4)** — D-state processes can't receive signals
- **Load average (2.3)** — D-state contributes to load
- **`/proc/PID/wchan`** — shows kernel function a D-state process is waiting in
- **Zombie processes (2.9)** — deep dive on zombie lifecycle

---
---

# 🟡 2.6 — `nice` & `renice`: CPU Scheduling Priority

## 📖 What It Is (Simple Terms)

`nice` and `renice` control a process's **priority hint** to the CPU scheduler. A "nicer" process (higher nice value) voluntarily yields CPU time to others. A less-nice process (lower value) demands more CPU.

Think of it as a politeness scale: a process with a high nice value is very polite and lets others go first; one with a low nice value is aggressive and pushes to the front of the line.

---

## ⚙️ How It Works Internally

```
Nice Value Scale:
-20 ────────────────────────────────── +19
Highest Priority              Lowest Priority
(least nice)                  (most nice)

Default = 0

Relationship:
PR (kernel priority) = 20 + NI (nice value)
So: nice -20 → PR 0  (highest)
    nice 0   → PR 20 (default)
    nice +19 → PR 39 (lowest)
```

The kernel's CFS scheduler uses priority to allocate CPU time shares — higher priority processes get proportionally more CPU time when the system is contended.

---

## 🔑 Commands

```bash
# Start a process with a specific nice value
nice -n 10 python backup.py     # lower priority
nice -n -10 python realtime.py  # higher priority (requires root for negative)
nice -n 19 tar -czf backup.tgz /data/  # run backup at lowest priority

# Change priority of a running process
renice 10 -p 1234               # by PID
renice 10 -u www-data           # all processes of a user
renice -5 -p 1234               # requires root (negative = higher priority)

# Check current nice/priority values
ps -eo pid,ni,pri,comm --sort=-ni | head

# In top: NI column shows nice value, PR shows kernel priority
# Press r in top to renice interactively
```

### `ionice` — I/O Priority (Bonus)

```bash
# Set I/O scheduling class and priority
ionice -c 3 -p 1234              # Class 3: Idle (lowest, only runs when nothing else needs disk)
ionice -c 2 -n 7 tar czf b.tgz  # Class 2: Best-effort, priority 7 (lowest within class)

# Run backup with both CPU and I/O deprioritized
nice -n 19 ionice -c 3 rsync -av /data /backup/

# Classes:
# 0: None (uses CFQ default)
# 1: Real-time (highest, use carefully — can starve other I/O)
# 2: Best-effort (default, 0-7 priority within class)
# 3: Idle (only uses I/O when no other process needs it)
```

---

## 🎤 Short Interview Answer

> "Nice values range from -20 (highest priority) to +19 (lowest). The default is 0. Regular users can only increase nice values (be nicer to others). Root can set negative values for higher priority. I use `nice -n 19` for background jobs like backups or log compression that shouldn't compete with production traffic. For already-running processes, `renice` changes priority on the fly. I also use `ionice -c 3` alongside `nice 19` for backup tasks so they don't impact disk I/O either — a doubly polite backup job."

---

## 🏭 Real Production Example

```bash
#!/bin/bash
# Low-impact backup script — won't starve production processes

# Run tar backup at lowest CPU and I/O priority
nice -n 19 ionice -c 3 \
    tar -czf /backup/data-$(date +%Y%m%d).tgz \
    /var/lib/mysql/data/ \
    2>>/var/log/backup.log

echo "Backup completed: $?"
```

---

## ⚠️ Gotchas

1. **Nice values only matter under CPU contention** — if the CPU is mostly idle, nice values have no effect. A nice 19 process runs just as fast as a nice 0 process on an idle system.

2. **Only root can set negative nice values** — regular users can only go from their current priority toward +19, not toward -20.

3. **Nice is a hint, not a guarantee** — it influences the scheduler's weighting but doesn't guarantee exact CPU time ratios.

4. **Threads inherit nice values** — setting nice on a process affects all its threads.

---
---

# 🟡 2.7 — `/proc/PID` Internals: `cmdline`, `maps`, `fd`, `status`, `limits`

## 🧠 Deeply Tied to Linux Kernel Internals

## 📖 What It Is (Simple Terms)

`/proc` is a **virtual filesystem** — it doesn't exist on disk. The kernel generates its contents on-the-fly when you read from it. Each process gets a directory `/proc/PID/` containing everything the kernel knows about that process.

---

## 🔑 Key Files in `/proc/PID/`

```bash
PID=1234
ls /proc/$PID/
# cmdline  cwd  environ  exe  fd  fdinfo  limits  maps  mem  net  
# oom_adj  oom_score  root  smaps  stat  status  task  wchan
```

### `/proc/PID/cmdline` — Full Command

```bash
cat /proc/$PID/cmdline | tr '\0' ' '
# Args are null-byte separated, tr converts to spaces
# Example: python /app/server.py --port 8080 --workers 4

# Equivalent to:
ps -p $PID -o cmd=
```

### `/proc/PID/status` — Process Summary

```bash
cat /proc/$PID/status
# Name:   python
# State:  S (sleeping)
# Tgid:   1234      ← Thread Group ID (= PID for single-threaded)
# Pid:    1234
# PPid:   1000      ← Parent PID
# Uid:    1000 1000 1000 1000   ← Real, Effective, Saved, FS UID
# VmRSS:  512000 kB ← Resident memory (what's actually in RAM)
# VmSize: 2048000 kB ← Virtual memory total
# Threads: 8        ← Number of threads
# SigBlk: 0000000000000000  ← Blocked signals (bitmask)
# SigIgn: 0000000000001000  ← Ignored signals
# SigCgt: 0000000182000000  ← Caught signals (custom handlers)
```

### `/proc/PID/fd/` — Open File Descriptors

```bash
ls -la /proc/$PID/fd/
# lrwxrwxrwx 1 user user 64  fd/0 -> /dev/pts/0        ← stdin
# lrwxrwxrwx 1 user user 64  fd/1 -> /dev/pts/0        ← stdout
# lrwxrwxrwx 1 user user 64  fd/2 -> /dev/pts/0        ← stderr
# lrwxrwxrwx 1 user user 64  fd/3 -> /var/log/app.log  ← log file
# lrwxrwxrwx 1 user user 64  fd/4 -> socket:[12345]    ← TCP connection
# lrwxrwxrwx 1 user user 64  fd/5 -> /tmp/app.lock     ← lock file

# Count open FDs
ls /proc/$PID/fd | wc -l

# Find if process has a deleted file still open (fd leak diagnostic)
ls -la /proc/$PID/fd | grep deleted
# lrwx  fd/6 -> /var/log/old.log (deleted)
# → The file is deleted from disk but still open — taking up disk space!
# Fix: HUP the process to reopen log files (logrotate does this)
```

### `/proc/PID/maps` — Memory Map

```bash
cat /proc/$PID/maps
# 7f8a42000000-7f8a42400000 r-xp 00000000 08:01 123456  /usr/lib/python3.10/lib-dynload/...
# 7f8a42600000-7f8a42601000 rw-p 00000000 00:00 0       [heap]
# 7ffe01234000-7ffe01256000 rw-p 00000000 00:00 0       [stack]
# 7f8a42800000-7f8a42801000 r--p 00000000 fd:01 789     /etc/localtime
#
# Format: start-end perms offset dev inode pathname
# Permissions: r=read, w=write, x=execute, p=private(COW), s=shared
```

### `/proc/PID/limits` — Resource Limits

```bash
cat /proc/$PID/limits
# Limit               Soft Limit  Hard Limit  Units
# Max open files      65536       65536       files
# Max processes       31429       31429       processes
# Max locked memory   65536       65536       bytes
# Max stack size      8388608     unlimited   bytes
# Max cpu time        unlimited   unlimited   seconds

# These are the ulimit values for this process
# If a process hits "Max open files" → Too many open files error
# Fix: increase with ulimit -n or /etc/security/limits.conf
```

### `/proc/PID/net/tcp` — Network Connections

```bash
cat /proc/$PID/net/tcp
# Gives raw hex socket state data
# Easier to use: ss -tp | grep $PID
# or: lsof -p $PID -i
```

---

## 🎤 Short Interview Answer

> "/proc is a virtual filesystem where the kernel exposes process information as files. /proc/PID/ contains everything about a running process. I use fd/ to check for file descriptor leaks and find deleted-but-open files. I check status for memory usage (VmRSS for actual RAM), limits to diagnose 'too many open files' errors, and maps to understand a process's memory layout. In production, the most common use is checking fd/ when an application runs out of file descriptors — you can see exactly which files it has open and identify the leak."

---

## 🏭 Real Production Example

**Scenario: App throws "Too many open files" error**

```bash
# Find the PID
PID=$(pgrep java)

# Check current FD count vs limit
echo "Open FDs: $(ls /proc/$PID/fd | wc -l)"
echo "Limit: $(cat /proc/$PID/limits | grep 'open files' | awk '{print $4}')"

# See what's open
ls -la /proc/$PID/fd/ | awk '{print $NF}' | sort | uniq -c | sort -rn | head -20
# 847 socket:[...]     ← Too many sockets! Connection leak
#  12 /var/log/app.log
#   3 /dev/pts/0

# Many sockets → connection pool leak or not closing connections
# Investigate: ss -tp | grep $PID
```

---

## ⚠️ Gotchas

1. **Reading `/proc/PID/mem`** directly requires `ptrace` permission — you can't just `cat` it.
2. **`/proc/PID/` disappears** when the process dies — race condition if you're scripting against it.
3. **`/proc/PID/fd/` symlinks point to deleted files** if the file was deleted while open — check for `(deleted)` suffix.
4. **Limits are per-process at fork time** — changing `/etc/security/limits.conf` only affects new login sessions, not running processes.

---
---

# 🔴 2.8 — Linux Scheduler: CFS, Time Slices, cgroups CPU Limits

## 🧠 Deeply Tied to Kernel Internals

## 📖 What It Is (Simple Terms)

The **Completely Fair Scheduler (CFS)** is the Linux kernel's default CPU scheduler. Its goal: give every process a "fair" share of CPU time proportional to its priority weight.

Instead of fixed time slices, CFS tracks **virtual runtime (vruntime)** for each process — the process with the smallest vruntime (got the least CPU time recently) runs next.

---

## ⚙️ How CFS Works Internally

```
CFS uses a Red-Black Tree (self-balancing BST):

        [vruntime=100, bash]
              /          \
[vruntime=50, nginx]   [vruntime=200, python]
        /
[vruntime=10, java]  ← leftmost = next to run

Rule: The leftmost node (minimum vruntime) ALWAYS runs next.
When a process runs, its vruntime increases.
When it's preempted, it's re-inserted at its new vruntime.
```

**Key parameters:**
```bash
# Scheduling parameters
cat /proc/sys/kernel/sched_latency_ns    # Target scheduling period (6ms default)
cat /proc/sys/kernel/sched_min_granularity_ns  # Minimum time slice per process
cat /proc/sys/kernel/sched_wakeup_granularity_ns
```

---

## 🔑 cgroups CPU Limits (Container Context)

```bash
# cgroups v1 — CPU limits
cat /sys/fs/cgroup/cpu/docker/$CONTAINER_ID/cpu.cfs_quota_us   # quota in microseconds
cat /sys/fs/cgroup/cpu/docker/$CONTAINER_ID/cpu.cfs_period_us  # period (100ms = 100000)

# If quota=50000, period=100000 → 50% CPU limit (0.5 CPUs)
# If quota=200000, period=100000 → 200% = 2.0 CPUs

# cgroups v2
cat /sys/fs/cgroup/system.slice/cpu.max
# 50000 100000  → max 50000us per 100000us period = 50% CPU

# Docker CPU limits
docker run --cpus=0.5 nginx     # 50% of one CPU
docker run --cpu-shares=512 nginx  # Relative weight (1024 = default)

# Kubernetes CPU limits/requests
# requests: guaranteed minimum, used for scheduling decisions
# limits: hard cap via cgroups CFS quota
```

### Observing CPU Throttling

```bash
# Check if a container is being CPU throttled
cat /sys/fs/cgroup/cpu/docker/$CID/cpu.stat
# nr_periods 1000        ← total CFS periods evaluated
# nr_throttled 342       ← periods where quota was exhausted
# throttled_time 1234567 ← nanoseconds spent throttled

# High throttled_time → container is hitting its CPU limit
# Fix: increase CPU limit or optimize the application
```

---

## 🎤 Short Interview Answer

> "CFS — the Completely Fair Scheduler — tracks virtual runtime for each process and always runs the one with the smallest vruntime next, stored in a red-black tree for O(log n) operations. This ensures fair CPU time distribution weighted by priority. In container environments, cgroups layer on top of CFS with CFS quota (cpu.cfs_quota_us / cpu.cfs_period_us) to enforce hard CPU limits — a container limited to 0.5 CPUs can only run 50ms per 100ms period. When troubleshooting container performance, I check cpu.stat's nr_throttled to see if the app is hitting CPU limits, which causes latency spikes even if CPU looks underutilized from the host perspective."

---

## ⚠️ Gotchas

1. **CPU throttling causes latency, not just throughput loss** — when a container is throttled mid-request, that request takes longer even though CPU usage looks fine from outside.

2. **CPU requests ≠ CPU limits in Kubernetes** — requests affect scheduling placement; limits enforce cgroup quotas. A container can burst above requests (up to limits) on a busy node.

3. **Noisy neighbor problem** — on shared hosts, if one cgroup exhausts CPU, others with lower shares suffer. cgroups weights help but don't eliminate contention.

---
---

# 🔴 2.9 — Zombie & Orphan Processes

## 📖 Zombie Process

```
Parent (PID 100) ──fork()──► Child (PID 200)
                                   │
                               child does work
                                   │
                               child exits()
                                   │
                    Kernel: "I'll keep PID 200's entry
                             in the process table until
                             parent calls wait()"
                                   │
                    Parent never calls wait()
                                   │
                              PID 200 = ZOMBIE (Z state)
                              - No memory
                              - No CPU  
                              - Just a process table entry
                              - Shows as <defunct> in ps
```

```bash
# Find zombies
ps aux | awk '$8=="Z" {print}'
# USER  PID  STAT  COMMAND
# app   8234  Z    [python] <defunct>

# Find the zombie's parent
ps -p $(ps -o ppid= -p 8234) -o pid,cmd

# Options to clear:
# 1. Fix the parent application to call wait()
# 2. Send SIGCHLD to parent (might trigger wait())
kill -CHLD $PPID
# 3. Kill the parent — zombies get re-parented to init, which reaps them
kill -TERM $PPID
```

## 📖 Orphan Process

```
Parent dies ──────► Child is alive but parentless
                         │
                    Kernel re-parents to PID 1 (systemd/init)
                         │
                    init/systemd becomes the new parent
                    and will call wait() when child eventually exits
```

Orphans are **not problematic** — they continue running, just with PID 1 as parent. This is actually how daemons work: they deliberately orphan themselves (double-fork technique) to run independently.

---

## 🎤 Short Interview Answer

> "A zombie process has exited but its parent hasn't called wait() to collect its exit status, leaving a defunct entry in the process table. Zombies hold no memory or CPU — they're harmless in small numbers but can exhaust PID space if there are thousands. You can't kill a zombie directly since it's already dead; you fix the parent app or kill the parent so init re-parents and reaps them. An orphan is the opposite — a child whose parent died. The kernel automatically re-parents orphans to PID 1 (systemd), which will eventually reap them. Orphans are normal and by design in daemon creation patterns."

---

## 🏭 Production Example

```bash
#!/bin/bash
# Proper parent that avoids creating zombies

# BAD: Fork child and never wait
child_pid=$!
# ... never wait for it ... → zombie

# GOOD: Reap children properly
child_pid=$!
wait $child_pid   # synchronous wait
echo "Child exited: $?"

# GOOD: Async reaping with trap
trap 'wait' SIGCHLD  # reap any child that exits

# GOOD: Double-fork daemon pattern (avoids zombies entirely)
# Parent forks → child forks grandchild → child exits
# Grandchild is orphaned → adopted by init → runs as daemon
```

---
---

# 🔴 2.10 — `strace` & `ltrace`: Syscall Tracing

## 🔥 High-Frequency Advanced Topic

## 📖 What It Is (Simple Terms)

- **`strace`** — traces **system calls** (kernel API calls) made by a process
- **`ltrace`** — traces **library calls** (libc and other shared library function calls)

When a program misbehaves and you have no source code and no logs, strace is your X-ray machine — it shows exactly what the program is asking the kernel to do.

---

## ⚙️ How It Works Internally

```
User Process                  Kernel
────────────                  ──────
open("/etc/config", ...)  ──► sys_open()
                               │
                          strace intercepts here
                          using ptrace() syscall
                               │
                          Returns to process with fd
```

`strace` uses `ptrace()` to intercept each syscall entry/exit and print it. This makes the process run ~100x slower — use with caution in production.

---

## 🔑 Commands

```bash
# Trace a new command
strace ls /tmp

# Attach to running process (non-destructive)
strace -p 1234

# Trace and follow child processes
strace -f python app.py

# Filter by syscall type
strace -e trace=open,read,write ls
strace -e trace=network python app.py    # network calls only
strace -e trace=file python app.py       # file-related calls

# Summarize syscall counts and time (best for profiling)
strace -c python app.py
# % time     seconds  usecs/call     calls    errors syscall
# ─────── ───────── ─────────── ───────── ───────── ──────────
#  45.23    0.123456         10     12345         0 read
#  30.11    0.082000          5     16400         0 write
#  10.05    0.027350        273       100        10 open

# Timestamp each syscall
strace -t python app.py    # wall clock time
strace -T python app.py    # time spent in each syscall

# Write to file instead of stderr
strace -o /tmp/trace.txt python app.py

# Full string output (default truncates at 32 chars)
strace -s 1024 python app.py

# Production-safe: summary only, attach to existing
strace -p $PID -c -f    # get stats without flooding output
```

### Reading `strace` Output

```
open("/etc/myapp/config.yaml", O_RDONLY) = 3
read(3, "server:\n  port: 8080\n", 4096) = 21
close(3)                                = 0
connect(4, {sa_family=AF_INET, sin_port=htons(5432), sin_addr="10.0.1.50"}, 16) = -1 ECONNREFUSED
```

Reading this:
1. Opened config file → got fd 3 ✅
2. Read 21 bytes from it ✅
3. Closed fd 3 ✅
4. Tried to connect to 10.0.1.50:5432 (PostgreSQL) → **ECONNREFUSED** ❌

This tells you the app can't reach the database — without any app-level logs!

---

## 🎤 Short Interview Answer

> "strace intercepts system calls using ptrace() — it shows you every interaction between a process and the kernel: file opens, network connections, memory allocations, process forks. I use it when an application fails silently or has no useful logs. The `-c` flag gives a summary of which syscalls are consuming time — useful for performance profiling. The `-p PID` flag attaches to a running process non-destructively. A classic use case: app says 'permission denied' but you don't know which file — strace shows the exact open() call and the path that's failing."

---

## 🏭 Real Production Example

**App silently fails to start, no logs anywhere:**

```bash
strace -e trace=file -o /tmp/start_trace.txt ./myapp

grep "ENOENT\|EACCES\|EPERM" /tmp/start_trace.txt
# open("/etc/ssl/certs/ca-bundle.crt", O_RDONLY) = -1 ENOENT (No such file or directory)
# open("/etc/myapp/config.yaml", O_RDONLY) = -1 EACCES (Permission denied)

# Found it: missing SSL cert bundle AND config permission issue
# Fix: install ca-certificates, fix config file permissions
```

---

## ⚠️ Gotchas

1. **strace significantly slows down the process** — 2-100x overhead from ptrace. Don't leave it attached to production processes.
2. **Use `-c` for production profiling** — it only shows a summary at the end, minimizing interference.
3. **Multithreaded processes** — use `-f` to follow threads. Output can be interleaved; use `-ff -o trace_prefix` to write each thread to a separate file.
4. **strace requires ptrace permission** — root, or the process must be owned by the calling user. In containers, ptrace may be disabled by seccomp policies.

---
---

# 🔴 2.11 — `lsof`: Open Files, Socket States, FD Leak Debugging

## 🔥 High-Frequency Production Tool

## 📖 What It Is (Simple Terms)

`lsof` = **List Open Files**. In Linux, everything is a file — regular files, directories, sockets, pipes, devices. `lsof` shows you every open file for every process (or a filtered subset).

It's the go-to tool for: "what process has this file open?", "why can't I unmount this filesystem?", "how many sockets does this app have?", "is there a file descriptor leak?"

---

## 🔑 Commands — The Cheat Sheet

```bash
# List all open files (very verbose — usually filter!)
lsof | head -20

# Files opened by a specific process
lsof -p 1234

# Files opened by a specific user
lsof -u www-data

# Find which process has a specific file open
lsof /var/log/nginx/access.log

# Find which process is listening on a port
lsof -i :80
lsof -i :443
lsof -i TCP:8080

# All network connections for a process
lsof -i -p 1234

# All TCP connections in LISTEN state
lsof -i TCP -s TCP:LISTEN

# All ESTABLISHED connections
lsof -i TCP -s TCP:ESTABLISHED

# Find what's preventing unmount of /mnt/data
lsof /mnt/data

# Find deleted files still held open (disk space leak!)
lsof | grep deleted

# Count open file descriptors per process
lsof -n | awk '{print $2}' | sort | uniq -c | sort -rn | head -10
# 1234  8234   ← process 8234 has 1234 open FDs!

# Files opened by processes matching name pattern  
lsof -c nginx
lsof -c python

# Combined filters (AND by default, OR with -a flag)
lsof -u www-data -c nginx    # nginx processes owned by www-data

# Show only IPv4
lsof -i 4

# Show numeric addresses (faster, no DNS lookup)
lsof -n -i TCP
```

### Reading `lsof` Output

```
COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF   NODE NAME
nginx    1234    root    cwd  DIR  8,1    4096       2    /
nginx    1234    root    txt  REG  8,1    1234567    123  /usr/sbin/nginx  (exec)
nginx    1234    root    mem  REG  8,1    2345678    456  /lib/x86_64.../libc.so.6
nginx    1234    root    0u   CHR  1,3    0t0        789  /dev/null
nginx    1234    root    1w   REG  8,1    102400     890  /var/log/nginx/access.log
nginx    1234    root    2w   REG  8,1    4096       891  /var/log/nginx/error.log
nginx    1234    root    5u   IPv4 12345  0t0        TCP  *:80 (LISTEN)
nginx    1234    root    6u   IPv4 12346  0t0        TCP  10.0.0.1:80->10.0.0.2:54321 (ESTABLISHED)
```

| FD field | Meaning |
|----------|---------|
| `cwd` | Current working directory |
| `txt` | Executable text |
| `mem` | Memory-mapped file |
| `0u` | fd 0, open for read+write (u=read/write, r=read, w=write) |
| `1w` | fd 1, open for writing |
| `5u` | fd 5, read/write (a socket) |

---

## 🎤 Short Interview Answer

> "lsof lists all open files for processes — and in Linux, everything is a file, including sockets, pipes, and devices. I use it constantly in production: `lsof -i :80` to find what's listening on a port, `lsof -p PID` to inspect a process's file descriptors, `lsof | grep deleted` to find disk space being held by deleted-but-open files, and `lsof /mnt/data` to figure out why a filesystem won't unmount. When an application hits 'too many open files', lsof shows me exactly what it has open so I can identify the leak pattern."

---

## 🏭 Real Production Example

**Scenario: Disk is 100% full but `du -sh /*` shows only 40% used**

```bash
# This classic discrepancy = deleted files still held open by processes
lsof | grep deleted

# Output:
# java  8234 app 47u REG 8,1 10737418240 /tmp/heap-dump-8234.hprof (deleted)
# java  8234 app 48u REG 8,1  5368709120 /var/log/app/app.log (deleted)

# Java heap dump = 10GB, and a log file = 5GB, both deleted but still open by java!
# The disk space is not freed until java closes those file descriptors.

# Solutions:
# 1. Restart the java process (closes all FDs, space is freed)
# 2. If can't restart: truncate via /proc
echo "" > /proc/8234/fd/47    # Truncate the deleted file in-place
# → Disk space freed immediately without restarting!

# 3. For log files: logrotate with postrotate HUP to reopen
```

---

## 💬 Common Interview Questions

**Q: How do you find which process is using port 8080?**
> `lsof -i :8080` or `ss -tlnp | grep 8080`. lsof shows the full process details; ss is faster and doesn't require root for your own processes.

**Q: Disk is 100% full but du shows only 60% — what's happening?**
> Classic deleted-but-open files problem. A process opened a file, the file was deleted (from the directory), but the process still holds an open file descriptor. The kernel keeps the disk blocks allocated until all FDs are closed. `lsof | grep deleted` identifies the culprit. Fix: restart the process, or truncate via `/proc/PID/fd/N` if you can't restart.

**Q: How do you check if a process is leaking file descriptors?**
> Monitor `ls /proc/$PID/fd | wc -l` over time. If it grows monotonically without bound, there's a leak. Use `lsof -p $PID | sort` to see what types of FDs are accumulating — if it's sockets, you have a connection leak; if it's regular files, a file handle leak.

---

## ⚠️ Gotchas

1. **`lsof` can be slow** — it parses `/proc` for every process. Use `-n` (no DNS) and `-P` (no port name lookup) to speed it up significantly.
2. **`lsof` needs root** for complete output — without root, you only see your own processes.
3. **`ss` is faster than `lsof` for network inspection** — `ss -tlnp` or `ss -tnp` are preferred for quick network checks.
4. **Race condition** — between listing a process and it dying, `/proc/PID/` disappears. lsof handles this gracefully but may print warnings.
5. **`lsof` output is text and inconsistent** — don't rely on column positions; use `lsof -F` for machine-parseable output when scripting.

---
---

# 📋 Quick Reference Card — Process Management

## Signal Quick Reference
```bash
kill -15 PID  # SIGTERM: graceful stop
kill -9 PID   # SIGKILL: force kill
kill -1 PID   # SIGHUP: reload config
kill -0 PID   # Check if PID exists (no signal sent)
kill -- -PGID # Kill entire process group
pkill -f pattern  # Kill by full command match
```

## Diagnostic One-Liners
```bash
# Find top CPU consumers
ps aux --sort=-%cpu | head -10

# Find all D-state (I/O blocked) processes
ps -eo pid,stat,comm | awk '$2~/^D/{print}'

# Check load vs CPU cores
echo "Load: $(uptime | awk -F'average:' '{print $2}') | CPUs: $(nproc)"

# Find deleted files holding disk space
lsof | grep deleted | awk '{print $2, $7, $NF}' | sort -k2 -rn

# Count FDs per process
lsof -n | awk '{print $2}' | sort | uniq -c | sort -rn | head -10

# Trace what files a process opens
strace -e trace=file -p PID 2>&1 | grep -E "open|openat"

# Find process listening on port
lsof -i :PORT -s TCP:LISTEN

# Kill entire process tree
kill -- -$(ps -o pgid= -p PID | tr -d ' ')
```

## Process State Quick Ref
```
R = Running/Runnable          → Normal, active CPU use
S = Sleeping (interruptible)  → Normal, waiting for event
D = Uninterruptible sleep     → ⚠️ I/O blocked — check storage!
Z = Zombie                    → Parent hasn't called wait()
T = Stopped                   → Ctrl+Z'd or debugger attached
```

---

# 🎯 Interview Cheat Sheet: Key Answers to Memorize

| Question | One-Line Answer |
|----------|-----------------|
| What's load average? | Average processes running OR waiting for I/O over 1/5/15 min |
| Load average of 4 on 4-core = ? | 100% utilized — fully loaded but manageable |
| Can you kill a zombie? | No — fix the parent or kill it so init reaps the zombie |
| Can you kill a D-state process? | Not until it returns from I/O — SIGKILL is pending but not delivered |
| SIGTERM vs SIGKILL | SIGTERM = polite request (catchable), SIGKILL = immediate force (uncatchable) |
| What does SIGHUP do for daemons? | Convention: reload config file without restart |
| What does kill -0 do? | Tests if PID exists and you have permission — sends no signal |
| Why is "free" memory misleading? | Linux uses free RAM for cache; check "avail Mem" instead |
| What causes high load + low CPU? | D-state processes stuck on I/O (usually storage) |
| Disk full but du shows less? | Deleted files still open by processes — `lsof | grep deleted` |

---

*📌 After reading each topic: Quiz Me / Go Deeper / Next Topic*
