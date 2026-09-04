# AI Engineering Lab — Agent Instructions

## Purpose

This repository is a sandbox for learning AI-assisted software engineering and production development.

The goal is to understand the engineering decisions and concepts, not simply to generate code.

## General Rules

- Inspect the existing project before making changes.
- Do not make unnecessary architectural changes.
- Do not add dependencies unless they are justified.
- Prefer simple solutions over premature complexity.
- Explain important technical decisions when they are introduced.
- Never expose or commit secrets, API keys, passwords, or credentials.
- Do not modify unrelated files.
- Keep changes small and reviewable.
- Add or update tests when behavior changes.
- Do not assume requirements that have not been specified.

## Learning Rules

When asked to teach or explain something:
- Explain the concept before implementing it.
- Explain why a technology or pattern is being used.
- Explain important tradeoffs.
- Do not hide complexity behind unnecessary abstractions.

When asked to implement something:
- First inspect the relevant files.
- State the implementation plan briefly.
- Make the smallest appropriate change.
- Run relevant tests or checks.
- Report what changed and whether verification passed.

## Git Rules

- Do not make commits unless explicitly asked.
- Do not force-push.
- Do not rewrite Git history.
- Do not use destructive Git commands without explicit approval.

## Architecture Rules

- Keep the architecture simple until a real requirement justifies additional complexity.
- Document significant architectural decisions.
- Do not introduce services such as Redis, message queues, load balancers, or additional infrastructure without explaining the problem they solve.

## Current Learning Priorities

This project will progressively teach:

1. Application fundamentals
2. Authentication
3. Authorization and RBAC
4. PostgreSQL and database migrations
5. Database indexing
6. Caching
7. Rate limiting
8. Background processing
9. Docker
10. Reverse proxies and HTTPS
11. CI/CD
12. Cloud deployment
13. Scaling and load balancing