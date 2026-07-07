# Week 1 Capstone — Network Recon + Defensive Report

## Goal

The goal of this capstone was to combine Week 1 Linux and networking skills into a small defensive audit report.

The audit focused on my own local WSL environment and used only authorized local checks.

## Scope

In scope:

- local system identity
- local network configuration
- local routes
- DNS resolver configuration
- listening ports
- local Nmap scan of 127.0.0.1
- DNS checks for github.com and overthewire.org
- HTTPS header checks for github.com and overthewire.org

Out of scope:

- exploitation
- brute forcing
- scanning random public IPs
- scanning university, company, neighbor, or unauthorized systems

## Deliverables

- final-report.md
- risk-notes.md
- evidence files
- audit script

## Main lesson

A defensive audit is not just running commands.

The important part is comparing evidence, understanding what each tool actually checks, and avoiding unsupported conclusions.
