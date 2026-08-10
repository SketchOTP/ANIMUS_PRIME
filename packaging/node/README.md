# PRIME Node native service packaging

The Node is a native service on repository-hosting machines. It must be installed
with a private control-plane bind and a state directory outside the repository.
The service never receives arbitrary shell commands and only exposes the bounded
repository/read and health routes in `apps/node/main.py`.

## Linux

1. Install the pinned Python runtime and `requirements-phase1.txt` in a dedicated
   virtual environment.
2. Set `PRIME_NODE_ALLOWED_ROOTS`, `PRIME_NODE_BOOTSTRAP_CREDENTIAL`,
   `PRIME_NODE_STATE_FILE`, and `PRIME_NODE_NAME` in the service environment.
3. Install `packaging/node/prime-node.service` for the dedicated service account.
4. Bind the listener only to an explicitly configured private interface and put
   TLS/mTLS termination in the approved private Core↔Node plane.

## Windows

Run `install-node.ps1` from an elevated PowerShell session. It creates a
dedicated service wrapper configuration and does not store the bootstrap or
long-lived credential in the repository. The Windows service must be bound to a
private interface and protected by the same protocol identity headers and TLS
configuration as Linux.

These files describe the supported installation shape; Phase-15 release status
remains open until the clean Linux and Windows installation/restart/reconnect
walkthroughs are executed and their evidence is recorded.
