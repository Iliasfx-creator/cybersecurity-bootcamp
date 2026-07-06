
## SSH keypair lab

### What file is private?

The private file is:

~/.ssh/cyber_bootcamp_ed25519

This file must stay secret.

It proves ownership of the keypair and should never be uploaded to GitHub, pasted into notes, sent in chat, or shared publicly.

### What file is public?

The public file is:

~/.ssh/cyber_bootcamp_ed25519.pub

The public key can be shared with systems that should allow this key to authenticate.

For example, a public key can be added to a server's authorized_keys file.

### Why private keys must not be committed

Private keys must not be committed because anyone who gets the private key may be able to authenticate as the key owner.

A leaked private key can give an attacker access to servers, repositories, or other systems where that key is trusted.

Even if the key is later deleted from the repository, it may still exist in Git history.

### What a fingerprint is

A fingerprint is a short representation of a public key.

It helps identify a key without printing the entire key.

Fingerprints are useful for checking that the key being used is the expected key.
