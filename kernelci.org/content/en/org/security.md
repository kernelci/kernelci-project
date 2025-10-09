---
title: "Security"
date: 2025-01-09
description: "Security policy and vulnerability reporting for KernelCI"
weight: 50
---

## Security Policy

KernelCI is committed to maintaining the security and integrity of our infrastructure and services. We take security vulnerabilities seriously and appreciate the efforts of security researchers and community members who help us maintain a secure platform.

## Reporting Security Vulnerabilities

If you discover a security vulnerability in any KernelCI project, please report it responsibly by emailing:

**[kernelci-sysadmin@groups.io](mailto:kernelci-sysadmin@groups.io)**

When reporting a vulnerability, please include:

- A detailed description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Any suggested remediation steps (if available)
- Your contact information for follow-up questions

## Response Process

Once a security report is received:

1. The KernelCI system administration team will acknowledge receipt
2. The team will investigate and assess the severity of the reported issue
3. We will work on a fix and coordinate disclosure timeline with the reporter
4. Once resolved, we will publish appropriate security advisories

## Scope

Security reports should focus on vulnerabilities in:

- KernelCI infrastructure and services
- KernelCI web applications (Dashboard, API, etc.)
- KernelCI tools and command-line utilities
- Authentication and authorization mechanisms
- Data exposure or privacy issues

## Bug Bounty Program

**KernelCI does not currently offer a bug bounty program or monetary rewards for security vulnerability reports.**

We greatly appreciate responsible disclosure and will publicly acknowledge security researchers who report valid vulnerabilities (unless they prefer to remain anonymous).

## Security Best Practices

For KernelCI contributors and users:

- Keep your API tokens and credentials secure
- Use strong authentication methods
- Report suspicious activity to the sysadmin team
- Follow secure coding practices when contributing code
- Regularly update dependencies and tools

## Public Disclosure

We request that security researchers:

- Provide us reasonable time to address vulnerabilities before public disclosure
- Avoid accessing, modifying, or deleting data that does not belong to you
- Do not perform testing that could degrade or disrupt KernelCI services
- Limit testing to your own accounts or test data when possible

Thank you for helping keep KernelCI and the Linux kernel testing community secure.


## Out of Scope

**KernelCI is not responsible for security issues in the Linux kernel itself or in projects we test.**

Do not report to KernelCI:

- **Linux kernel vulnerabilities** - Report these to the kernel community by following their [security process](https://docs.kernel.org/process/security-bugs.html)
- **Vulnerabilities in upstream projects** being tested by KernelCI (e.g., specific kernel trees, bootloaders, etc.) - Report these directly to the respective upstream project maintainers
- **Hardware security issues** - Contact the hardware vendor directly
- **Issues with test results or CI failures** - These are not security vulnerabilities; please use regular bug reporting channels

KernelCI provides testing infrastructure and tooling. We test the Linux kernel and related projects but are not responsible for security issues found within the code being tested.