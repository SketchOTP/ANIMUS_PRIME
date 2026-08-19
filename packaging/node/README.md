# PRIME Node native service packaging

The Node is a native service on repository-hosting machines. It must be installed
with a private control-plane bind and a state directory outside the repository.
The service never receives arbitrary shell commands and only exposes the bounded
repository/read and health routes in `apps/node/main.py`.

## Linux

1. Install the pinned Python runtime and `requirements-phase1.txt` in a dedicated
   virtual environment.
2. Set `PRIME_NODE_ALLOWED_ROOTS`, `PRIME_NODE_STATE_FILE`, `PRIME_NODE_NAME`,
   `PRIME_NODE_ID`, `PRIME_NODE_BIND_HOST`, `PRIME_NODE_TLS_CERT_FILE`,
   `PRIME_NODE_TLS_KEY_FILE`, `PRIME_NODE_TLS_CA_FILE`, and
   `PRIME_NODE_BOOTSTRAP_PUBLIC_KEY_FILE` in the service
   environment. The packaged entrypoint refuses to start without the TLS/mTLS
   files; `PRIME_NODE_ALLOW_INSECURE_HTTP` is reserved for disposable local
   qualification only.
3. Install `packaging/node/prime-node.service` for the dedicated service account.
4. Bind the listener only to an explicitly configured private interface and put
   TLS/mTLS termination in the approved private Core↔Node plane.

## Windows

Run `install-node.ps1` from an elevated PowerShell session. It installs a
versioned application copy, registers the genuine Windows SCM wrapper, applies
machine-scoped Node configuration supplied through its parameters, and protects
the private key and state directory for `SYSTEM` and Administrators only. The
short-lived one-time enrollment credential is delivered over the initial mTLS
channel and is never persisted in the service environment or installer logs.
Rerun with `-Repair` to update the installed application and service command
without replacing Node identity or state. The Windows service must bind to a
specific private interface, never a wildcard address.

These files describe the supported installation shape; Phase-15 release status
remains open until the clean Linux and Windows installation/restart/reconnect
walkthroughs are executed and their evidence is recorded.
