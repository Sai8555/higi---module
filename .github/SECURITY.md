# Security Policy

We take security seriously and appreciate your help in keeping `higi` secure. This document outlines our policy on reporting vulnerabilities and how we handle them.

## Supported Versions

Only the latest major version is actively supported with security updates.

| Version | Supported |
| ------- | --------- |
| >= 0.1.x| Yes       |
| < 0.1.0 | No        |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please **do not open a public issue**. Instead, report it using one of the following methods:

1. **GitHub Private Vulnerability Reporting**: Use the "Report a vulnerability" button under the Security tab of the GitHub repository.
2. **Email**: Send a detailed report to the maintainer at [girisaidurgajanapareddy@gmail.com](mailto:girisaidurgajanapareddy@gmail.com).

### Please include:
- A description of the vulnerability and its potential impact.
- Detailed steps to reproduce the issue (proof-of-concept code or payloads are highly appreciated).
- Any details about your environment (Python version, OS, installed dependencies).

## Our Response Process

1. **Acknowledgment**: We will acknowledge receipt of your report within 48 hours.
2. **Investigation**: We will investigate the issue and determine the severity. We may contact you for further details.
3. **Fix and Advisory**: If verified, we will work on a fix. We will publish a security advisory alongside a patched release.
4. **Attribution**: Unless you request otherwise, we will credit you for the discovery in the release notes and advisory.

## Security Practices for `higi`

Because `higi` parses and sanitizes volatile data (such as AI/LLM outputs or webhooks), please be mindful of:
- **Input Sanitization**: Ensure that you use proper length limits when parsing highly volatile inputs to prevent memory consumption attacks.
- **Dependency Security**: Regularly update dependencies (such as `hatchling` and testing packages) to avoid vulnerability inheritance.
