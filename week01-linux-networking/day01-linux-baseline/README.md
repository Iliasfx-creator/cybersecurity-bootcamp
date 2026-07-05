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

In symbolic form:

```text
rw-r--r--
