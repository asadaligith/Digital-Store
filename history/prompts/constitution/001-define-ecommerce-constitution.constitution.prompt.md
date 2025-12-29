---
id: 001
title: Define E-Commerce Constitution
stage: constitution
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5-20251029
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["constitution", "architecture", "standards", "ecommerce", "react", "fastapi", "mongodb"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

```text
You are an expert full-stack software architect and UI/UX engineer.
Define the constitutional principles for building a modern, scalable E-commerce web application using React, Tailwind CSS, GSAP (frontend) and FastAPI with MongoDB (backend).

The constitution must enforce:

Clean architecture (separation of concerns between UI, state, API, and database)

Mobile-first, fully responsive design

High-performance animations using GSAP without blocking UI

Secure API design (JWT authentication, validation, error handling)

Scalable MongoDB schema design

Reusable React components and hooks

Accessibility (ARIA, keyboard navigation)

Production-ready coding standards and naming conventions

Output a clear list of non-negotiable rules and best practices that must be followed throughout the project lifecycle.
```

## Response snapshot

Created comprehensive Digital Store E-Commerce Constitution v1.0.0 with 10 core principles:

**Core Principles:**
1. **Clean Architecture** - Strict separation of concerns (UI, state, API, services, repository, models) with clear interfaces
2. **Mobile-First Responsive Design** - Development starts at 320px, progresses to tablet/desktop; Tailwind responsive utilities required
3. **Performance-First GSAP Animations** - GPU-accelerated transforms/opacity only, 60fps target, reduced motion support
4. **Secure API Design** - JWT auth, RBAC, Pydantic validation, rate limiting, HTTPS, CORS, XSS/injection prevention
5. **Scalable MongoDB Schema Design** - Embedding vs referencing strategy, indexing, schema validation, migration versioning
6. **Reusable React Components and Hooks** - Single responsibility, TypeScript interfaces, composition over inheritance, custom hooks
7. **Accessibility** - Semantic HTML, ARIA labels, keyboard navigation, WCAG AA contrast, screen reader testing
8. **Test-Driven Development** - Unit (>80% coverage), integration, E2E tests required; test pyramid approach
9. **Production-Ready Coding Standards** - TypeScript strict mode, Python type hints, Prettier/Black, ESLint/Ruff, conventional commits
10. **Dependency Management and Security** - Minimize dependencies, npm/pip-audit, version pinning, bundle size <200KB gzipped

**Architecture Constraints:**
- Technology stack locked: React 18+, TypeScript 5+, Tailwind CSS 3+, GSAP 3+, FastAPI, MongoDB 7+, Python 3.11+
- Performance budgets: FCP <1.5s, LCP <2.5s, API p95 <200ms reads/<500ms writes
- Security: JWT auth, bcrypt ≥12 rounds, account lockout, HTTPS, CSRF protection, GDPR/PCI-DSS compliance

**Development Workflow:**
- Git workflow: main (production), develop (integration), feature/bugfix/hotfix branches
- Code review checklist: constitutional compliance, tests, security, performance, accessibility
- CI/CD: 7-step CI (linting, formatting, type checking, tests, security, build), automated staging, manual prod approval

**Governance:**
- Constitution is supreme authority; violations rejected in code review
- Amendment process requires proposal, review by tech lead + 2 senior devs, majority approval, ADR documentation
- Semantic versioning for constitution updates
- Compliance audits: monthly (automated), quarterly (manual architecture review), pre-release (full audit)

## Outcome

- ✅ Impact: Established foundational governance document for entire Digital Store E-Commerce project
- 🧪 Tests: N/A (constitution document)
- 📁 Files: Created .specify/memory/constitution.md (357 lines)
- 🔁 Next prompts: /sp.specify (create feature spec), /sp.plan (architecture planning), /sp.tasks (task breakdown)
- 🧠 Reflection: Constitution provides comprehensive, enforceable standards covering all aspects of modern e-commerce development; principles are specific, measurable, and actionable with clear rationale

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All constitutional principles are specific, measurable, non-negotiable, with clear rationale
- Prompt variant (if applicable): Standard /sp.constitution workflow
- Next experiment (smallest change to try): N/A - Initial constitution creation successful
