# Linux Command Baseline

This document records basic Linux commands that are important for system administration, security inspection, troubleshooting, and incident response.

---

## Command: pwd

### What it does

Prints the current working directory.

### Why it matters in cybersecurity

When investigating a system, it is important to know exactly where you are in the filesystem. Running commands from the wrong directory can cause mistakes, especially when editing files, collecting evidence, or running scripts.

### Example

```bash
pwd
```

---

## Command: ls -la

### What it does

Lists files and directories, including hidden files, with permissions, owner, group, size, and timestamps.

### Why it matters in cybersecurity

Hidden files, file permissions, ownership, and timestamps are important during system inspection, privilege analysis, and incident response.

### Example

```bash
ls -la /etc
```

---

## Command: cd

### What it does

Changes the current directory.

### Why it matters in cybersecurity

Security work often requires moving through system directories, logs, user folders, configuration paths, and project folders. Knowing how to navigate safely is basic but critical.

### Example

```bash
cd /var/log
```

---

## Command: mkdir

### What it does

Creates a new directory.

### Why it matters in cybersecurity

Good folder structure is important when organizing scripts, evidence, logs, reports, and lab files. Poor organization makes investigations harder to reproduce.

### Example

```bash
mkdir evidence
```

---

## Command: touch

### What it does

Creates an empty file or updates the timestamp of an existing file.

### Why it matters in cybersecurity

It is useful for quickly creating test files, lab files, scripts, and evidence placeholders. Timestamps can also matter during investigation.

### Example

```bash
touch notes.txt
```

---

## Command: cat

### What it does

Prints the contents of a file to the terminal.

### Why it matters in cybersecurity

Analysts often need to quickly inspect configuration files, logs, scripts, or small text files.

### Example

```bash
cat /etc/hostname
```

---

## Command: less

### What it does

Opens a file in a scrollable viewer.

### Why it matters in cybersecurity

Large logs or configuration files are easier and safer to inspect with `less` than by printing everything directly to the terminal.

### Example

```bash
less /var/log/syslog
```

---

## Command: head

### What it does

Shows the first lines of a file.

### Why it matters in cybersecurity

Useful when quickly checking the beginning of logs, reports, exported data, or command outputs.

### Example

```bash
head /var/log/syslog
```

---

## Command: tail

### What it does

Shows the last lines of a file.

### Why it matters in cybersecurity

Useful for checking the most recent log entries. The `-f` option can monitor logs live.

### Example

```bash
tail /var/log/syslog
```

---

## Command: grep

### What it does

Searches for text patterns inside files or command output.

### Why it matters in cybersecurity

`grep` is one of the most useful commands for finding suspicious strings, usernames, IP addresses, errors, failed logins, or indicators of compromise.

### Example

```bash
grep "error" /var/log/syslog
```

---

## Command: find

### What it does

Searches for files and directories based on name, type, size, permissions, owner, or time.

### Why it matters in cybersecurity

`find` can locate suspicious files, world-writable files, SUID binaries, recently modified files, or misplaced sensitive data.

### Example

```bash
find /home -name "*.sh"
```

---

## Command: locate

### What it does

Searches for files using a prebuilt database.

### Why it matters in cybersecurity

`locate` is fast for finding known filenames, tools, logs, or configuration files. However, it depends on the database being updated.

### Example

```bash
locate passwd
```

---

## Command: chmod

### What it does

Changes file or directory permissions.

### Why it matters in cybersecurity

Incorrect permissions can expose sensitive files or allow unauthorized users to modify scripts, binaries, or configuration files.

### Example

```bash
chmod 600 private.txt
```

---

## Command: chown

### What it does

Changes the owner or group of a file or directory.

### Why it matters in cybersecurity

File ownership controls who can manage files. Wrong ownership can create privilege issues or allow users to control files they should not control.

### Example

```bash
sudo chown root:root important.conf
```

---

## Command: ps aux

### What it does

Shows running processes with detailed information.

### Why it matters in cybersecurity

Process inspection helps identify suspicious programs, unexpected services, malware-like behavior, or processes running under unusual users.

### Example

```bash
ps aux
```

---

## Command: top

### What it does

Shows live system resource usage and running processes.

### Why it matters in cybersecurity

Useful for spotting processes that consume unusual CPU or memory, which can indicate abuse, misconfiguration, or compromise.

### Example

```bash
top
```

---

## Command: kill

### What it does

Sends a signal to a process, usually to stop it.

### Why it matters in cybersecurity

During investigation or containment, it may be necessary to stop a suspicious or runaway process. It must be used carefully.

### Example

```bash
kill 1234
```

---

## Command: whoami

### What it does

Prints the current username.

### Why it matters in cybersecurity

Knowing which user you are operating as is critical. Many mistakes happen when users do not realize they are running commands as root or as the wrong account.

### Example

```bash
whoami
```

---

## Command: id

### What it does

Shows the current user's UID, GID, and group memberships.

### Why it matters in cybersecurity

Group membership affects permissions. For example, users in privileged groups may have access to administrative actions or sensitive files.

### Example

```bash
id
```

---

## Command: groups

### What it does

Shows the groups that a user belongs to.

### Why it matters in cybersecurity

Groups help determine access rights. Checking groups is useful during privilege review and account auditing.

### Example

```bash
groups
```

---

## Command: sudo

### What it does

Runs a command with elevated privileges, usually as root.

### Why it matters in cybersecurity

`sudo` is powerful and dangerous. It is needed for administration, but misuse can damage a system or expose sensitive data.

### Example

```bash
sudo apt update
```

---

## Command: ip a

### What it does

Shows network interfaces and IP addresses.

### Why it matters in cybersecurity

IP address information is needed for network troubleshooting, host identification, scanning labs, and understanding system exposure.

### Example

```bash
ip a
```

---

## Command: ss -tulpen

### What it does

Shows listening TCP/UDP sockets, ports, users, processes, and related network information.

### Why it matters in cybersecurity

Open ports show what services are exposed. This is important for attack surface analysis, service enumeration, and incident response.

### Example

```bash
sudo ss -tulpen
```

---

## Command: ping

### What it does

Tests network reachability using ICMP echo requests.

### Why it matters in cybersecurity

`ping` helps check whether a host is reachable. It is useful in troubleshooting, network mapping, and lab connectivity checks.

### Example

```bash
ping -c 4 8.8.8.8
```

---

## Command: traceroute

### What it does

Shows the network path packets take to reach a destination.

### Why it matters in cybersecurity

`traceroute` helps understand routing paths, network delays, filtering, and where connectivity problems may occur.

### Example

```bash
traceroute google.com
```
