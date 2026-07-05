# Day 1 — Linux Baseline

## Goal

The goal of this lab is to set up a clean Linux working environment, practice basic shell commands, understand Linux permissions, and create a basic system inventory script.

## Permissions mini-lab

In this lab I created three files:

- public.txt
- private.txt
- executable.sh

Then I applied different permissions to understand how Linux controls access to files.

## What 644 means

644 means that the owner can read and write the file, while the group and others can only read it.

Symbolic form:

```text
rw-r--r--

This is common for normal files that should be readable but not executable.

What 600 means

600 means that only the owner can read and write the file. The group and others have no access.

Symbolic form:

rw-------

This is useful for private files, credentials, SSH keys, or sensitive notes.

What 755 means

755 means that the owner can read, write, and execute the file. The group and others can read and execute it, but they cannot modify it.

Symbolic form:

rwxr-xr-x

This is common for scripts and programs that need to be executable.

What rwx means

rwx stands for:

r = read
w = write
x = execute

For files, execute means the file can be run as a program or script. For directories, execute means the directory can be entered.

Owner, group, and others

Linux permissions are divided into three categories:

owner: the user who owns the file
group: users who belong to the file's group
others: everyone else on the system

This matters because Linux systems often have multiple users and services running at the same time.

Why wrong permissions are a security risk

Wrong permissions can expose private data or allow unauthorized changes.

For example, if a private key or password file is readable by everyone, another user or compromised process could steal it. If a script is writable by other users, an attacker could modify the script and wait for someone with more privileges to execute it.

Good permissions reduce the damage that can happen if a user account or process is compromised.
