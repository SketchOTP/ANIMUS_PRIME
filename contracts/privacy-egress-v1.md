# Privacy and Egress Policy v1

Default posture is local-first and deny-by-default for external content egress.

- The operator selects an AI function profile and provider before model-backed work.
- Repository, `.agent`, memory, Notion, and Evidence content are untrusted data and are not sent to a provider unless the effective project policy permits it.
- Hindsight, Reflect, Mental Models, Ask, Progress, and Documentation Agent calls inherit the effective project privacy policy.
- No silent provider fallback, model substitution, embedding fallback, or public MCP exposure is permitted.
- Provider credentials are references to secure host storage, never plaintext repository values or logs.
- Context Export is used for unsupported/private-unreachable clients rather than weakening transport security.
- Tailscale is private-only; Funnel/public exposure is prohibited by policy.
- Redacted structured logs must not contain secrets, raw repository contents, prompts, memory bodies, or provider responses by default.
