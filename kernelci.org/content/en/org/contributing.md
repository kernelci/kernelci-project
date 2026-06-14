---
title: "Contributing Policy"
date: 2026-06-14
description: "KernelCI project contribution policy"
weight: 6
---

This page defines the project-level contribution policy for KernelCI
repositories. Individual repositories may include additional contribution
instructions in their `CONTRIBUTING.md` file, but they should follow this
policy unless the repository documents an established workflow that is
intentionally kept. Repository-specific contribution instructions should link
back to this page for the shared baseline.

## Goals

KernelCI projects should be easy to contribute to across repositories. The
baseline should reduce review noise, avoid repeated formatter and linter
discussions, and keep contributors from having to learn a different set of
style rules for each repository.

The goal is a minimal shared baseline, not uniformity for its own sake.
Contributors should spend time on features, fixes, tests, and reviews rather
than resolving avoidable tooling conflicts.

## AI-Assisted Contributions

As a Linux Foundation project working with the Linux kernel ecosystem,
KernelCI follows the approach used by the Linux kernel project for
AI-assisted and tool-generated contributions. Contributors should read the
upstream guidance in the Linux kernel documentation:

- [AI Coding Assistants](https://docs.kernel.org/process/coding-assistants.html)
- [Kernel Guidelines for Tool-Generated Content][tool-generated-content]
- [Using Assisted-by](https://docs.kernel.org/process/submitting-patches.html#using-assisted-by)

[tool-generated-content]: https://docs.kernel.org/process/generated-content.html

AI tools may assist with contributions, but they cannot own, certify, or take
responsibility for a contribution. A human contributor must review and
understand all submitted changes, ensure that the contribution is compatible
with the target repository's license, and take full responsibility for the
result.

If a repository requires a `Signed-off-by` tag or Developer Certificate of
Origin certification, only a human contributor may add it. AI agents must not
add `Signed-off-by` tags.

Contributors should disclose meaningful AI or advanced tool assistance using an
`Assisted-by` tag when the tool generated, rewrote, analyzed, or otherwise
materially affected the contribution. Basic editor completions, formatting, and
purely mechanical changes do not normally require disclosure, but contributors
should prefer transparency when disclosure would help reviewers understand the
origin of the work.

Repository owners and maintainers retain ownership of what is accepted into
their repositories. They may reject AI-assisted submissions, request additional
testing or explanation, ask for details about the tool or prompts used, or apply
extra review scrutiny when needed. Submitters must be able to explain and
defend every part of an AI-assisted contribution; otherwise they should not
submit it.

## Python Linting and Formatting

New Python projects, and existing Python projects that do not already have an
established automated style workflow, should use Ruff for linting and import
sorting.

The [kernelci-pipeline pre-commit configuration][pipeline-pre-commit] provides
an example Ruff setup that other repositories can use as a reference.

Python style checks must be automated in CI. They should also be available
locally through pre-commit hooks so contributors can run the same checks before
opening a pull request.

Project configurations may relax Ruff defaults when needed, but each exception
must be intentional. Project-level ignore lists should include a short rationale
for every ignored rule so future contributors understand whether the exception
is permanent, legacy-related, or expected to be removed later.

Line length should use a soft limit of 80 columns and a hard limit of 110
columns. The soft limit is a formatting preference; the hard limit is the point
where CI should fail unless the line is covered by an explicit exception.

## Tool Conflicts

Repositories must not enforce multiple tools whose rules contradict each other.
If fixing one tool's suggestion triggers a violation in another tool, one of
the tools must be removed or reconfigured.

For example, a repository may keep an existing Black, isort, tox, Poetry, or
similar workflow when it is already automated and maintainers prefer to keep it.
That workflow must still be documented and must not leave contributors stuck
between competing formatters or linters.

## Pre-commit Hooks

All repositories should include a `.pre-commit-config.yaml` or an equivalent
documented local check workflow.

The [kernelci-pipeline pre-commit configuration][pipeline-pre-commit] can be
used as a starting point for repositories that need a template.

Pre-commit hooks must run the same linting and formatting checks that CI
enforces. A pull request should not pass CI only because CI and local checks use
different rules.

Hooks should be practical to run on common contributor systems. If a repository
requires containerized checks, project-specific package managers, or other
non-default tooling, the repository's contribution instructions should explain
how to run them.

## Type Checking

Static type checking is optional. A repository may enable mypy, pyright, or a
similar type checker when maintainers decide it is appropriate for that project.

Type checking must not block adoption of the shared linting and formatting
baseline. Projects with substantial legacy code may adopt linting and formatting
first, then add or tighten type checking later.

## Exceptions

KernelCI repositories include legacy code and projects with established
development workflows. Existing projects may retain their current tooling if
the maintainer prefers it and contributors do not object.

Scoped exceptions are allowed for legacy modules, generated code, complex
entrypoints, command or subcommand setup functions, and other code that would be
riskier to rewrite than to exempt. These exceptions should be narrow, documented
in the repository configuration where possible, and revisited when the affected
code is changed.

Complexity exceptions are allowed when refactoring would create unnecessary
risk. For example, a targeted `noqa` for a high-complexity entrypoint is
acceptable when the surrounding code is stable and the exception is documented.

[pipeline-pre-commit]: https://github.com/kernelci/kernelci-pipeline/blob/main/.pre-commit-config.yaml
