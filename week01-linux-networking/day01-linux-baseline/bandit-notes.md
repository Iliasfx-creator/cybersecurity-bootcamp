# Bandit Notes — Day 1

## Important rule

I did not write any Bandit passwords in this repository. Passwords should never be committed to GitHub.

---

## Bandit Level 0

### Goal
Connect to the Bandit server using SSH.

### Commands used
```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
What I learned

I learned how to connect to a remote Linux machine using SSH. The command includes a username, a hostname, and a custom port.

Mistake / difficulty

At first, password input can be confusing because the terminal does not show characters while typing the password.

Bandit Level 1
Goal

Find the password for the next level inside a file named readme.

Commands used
pwd
ls -la
cat readme
What I learned

I learned how to check my current directory, list files, and read a text file from the terminal.

Mistake / difficulty

I had to remember that I was working on a remote machine, not on my own Ubuntu system.

Bandit Level 2
Goal

Read a file with a special filename.

Commands used
ls -la
cat ./-
What I learned

I learned that a filename can look like an option to a command. The file was named -, so using cat - was wrong. Using ./- tells the shell to treat it as a file in the current directory.

Mistake / difficulty

I accidentally used cat -, which made the terminal wait for input instead of reading the file.

Bandit Level 3
Goal

Read a file with spaces and option-like characters in its name.

Commands used
ls -la
cat "./--spaces in this filename--"
What I learned

I learned that spaces split command arguments in the shell, so quotes are needed. I also learned that filenames starting with -- can be interpreted as options, so adding ./ makes it clear that I am referring to a file path.

Mistake / difficulty

The filename was not exactly spaces in this filename. It was --spaces in this filename--, so I had to use the exact filename shown by ls -la.

Bandit Level 4
Goal

Find and read a hidden file inside a directory.

Commands used
ls -la
cd inhere
ls -la
cat ./...Hiding-From-You
What I learned

I learned that hidden files in Linux start with a dot. I also learned that filenames are case-sensitive, so Hiding-From-You and hiding-from-you are different names.

Mistake / difficulty

I first tried the wrong filename. The correct file was ...Hiding-From-You, including the three dots and the capital letters.
