# Security Policy

## Supported Versions

The following versions of It's Friday are currently supported with security updates.

| Version | Supported |
| -------- | -------- |
| Latest | ✅ |
| Older Versions | ❌ |

---

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly.

### Please Include

- A detailed description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested mitigation (if known)
- Screenshots or logs if applicable

### Do Not

- Publicly disclose the vulnerability before it has been reviewed
- Share exploit code that could harm users
- Post security vulnerabilities in public issues

---

## Response Process

When a valid vulnerability report is received:

1. The report will be acknowledged as soon as possible.
2. The issue will be investigated and validated.
3. A fix will be developed and tested.
4. A security update will be released when appropriate.
5. Credit may be given to the reporter unless anonymity is requested.

---

## Project Security Considerations

It's Friday is designed to run locally on the user's machine.

Current security principles include:

- Local execution of AI models through Ollama
- No mandatory cloud services
- Conversation memory stored locally
- User-controlled data and configuration
- No intentional collection of personal information

However, users should be aware that:

- Stored memory files may contain personal information.
- Microphone access is required for voice interaction.
- Third-party libraries may introduce security risks.
- Users are responsible for protecting their local environment.

---

## Best Practices for Users

- Keep Python and dependencies updated.
- Use the latest version of Ollama.
- Review third-party packages before installation.
- Avoid sharing memory files containing personal information.
- Store sensitive credentials in environment variables and never commit them to GitHub.
- Use a `.gitignore` file to exclude secrets, virtual environments, and local data.

Example:

```gitignore
.env
jarvis-env/
__pycache__/
*.pyc
fridays_memory.json
```

---

## Disclaimer

This project is provided "as is" without warranty of any kind.

Users are responsible for evaluating the security and suitability of the software for their own environment.

---

## Contact

For security-related concerns, please use GitHub's private reporting feature or contact the repository maintainer directly.

Thank you for helping keep It's Friday secure.
