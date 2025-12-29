<!--
Sync Impact Report:
Version: 1.0.0 (Initial ratification)
Modified Principles: N/A (new constitution)
Added Sections: All sections (new constitution)
Removed Sections: N/A
Templates Requiring Updates:
  ✅ .specify/templates/plan-template.md - Constitution Check section will reference these principles
  ✅ .specify/templates/spec-template.md - Requirements align with accessibility and security principles
  ✅ .specify/templates/tasks-template.md - Task organization reflects architectural and testing principles
Follow-up TODOs: None
-->

# Digital Store E-Commerce Constitution

## Core Principles

### I. Clean Architecture (NON-NEGOTIABLE)

**Separation of Concerns MUST be strictly enforced across all layers:**

- **Frontend**: UI components (React), state management (Context/Redux), animations (GSAP), and API clients MUST be separated into distinct modules
- **Backend**: API routes (FastAPI), business logic (services), data access (repositories), and models MUST be independently testable
- **No cross-layer violations**: UI components MUST NOT directly access database; API routes MUST NOT contain business logic
- **Dependencies flow inward**: UI → State → API Client → Services → Repository → Models
- **Each layer MUST have clear interfaces**: Contracts defined before implementation

**Rationale**: Clean architecture enables independent testing, parallel development, technology swaps, and long-term maintainability without cascading changes.

### II. Mobile-First Responsive Design (NON-NEGOTIABLE)

**All UI MUST be designed and implemented mobile-first:**

- **Development order**: Mobile (320px) → Tablet (768px) → Desktop (1024px+)
- **Tailwind CSS responsive utilities MUST be used**: Start with base styles, add `sm:`, `md:`, `lg:`, `xl:` breakpoints progressively
- **Touch targets MUST be ≥44px** for interactive elements on mobile
- **Responsive images MUST use**: `srcset`, `sizes`, or Tailwind responsive classes
- **Testing MUST verify**: All user flows work on mobile devices before desktop optimization
- **No desktop-first designs allowed**: If a design starts with desktop, it MUST be rejected and redesigned mobile-first

**Rationale**: Mobile traffic dominates e-commerce; mobile-first ensures optimal experience for the majority of users and prevents desktop-biased designs that fail on small screens.

### III. Performance-First GSAP Animations

**All animations MUST be performant and non-blocking:**

- **GPU-accelerated properties only**: Transform (translate, scale, rotate) and opacity; avoid animating width, height, top, left, margin
- **GSAP Timeline management**: Complex sequences MUST use `gsap.timeline()` with proper cleanup on unmount
- **Non-blocking requirement**: Animations MUST NOT delay user interactions; `pointer-events` and event listeners MUST remain responsive
- **60fps target**: All animations MUST maintain 60fps; use Chrome DevTools Performance profiler to verify
- **Lazy loading animations**: Animation libraries MUST be code-split; animations on below-fold content MUST load on demand
- **Reduced motion support**: MUST respect `prefers-reduced-motion` media query; provide instant transitions for users who request reduced motion

**Rationale**: Poor animation performance destroys user experience and SEO; GPU acceleration and non-blocking animations ensure smooth interactions even on low-end devices.

### IV. Secure API Design (NON-NEGOTIABLE)

**Security MUST be built into every API endpoint:**

- **Authentication**: JWT tokens MUST be used; access tokens (15min expiry) + refresh tokens (7 days) stored in httpOnly cookies
- **Authorization**: Role-based access control (RBAC) MUST be enforced at service layer, not just routes
- **Input validation**: Pydantic models MUST validate ALL inputs; reject invalid data with 400 status and clear error messages
- **Error handling**: NEVER expose stack traces or internal details in production; use structured error responses with error codes
- **Rate limiting**: MUST implement rate limiting per user/IP; e.g., 100 req/min for authenticated, 20 req/min for anonymous
- **HTTPS only**: All production APIs MUST use HTTPS; redirect HTTP to HTTPS
- **CORS configuration**: MUST whitelist specific origins; NEVER use `*` in production
- **SQL injection prevention**: MUST use parameterized queries or ORM; NEVER concatenate user input into queries
- **XSS prevention**: MUST sanitize all user-generated content before storage and rendering; use Content Security Policy headers

**Rationale**: E-commerce applications handle sensitive payment and personal data; security breaches destroy trust and violate compliance regulations (GDPR, PCI-DSS).

### V. Scalable MongoDB Schema Design

**Database schemas MUST be designed for scale and performance:**

- **Document design**: Embed related data for 1:1 and 1:few relationships; reference for 1:many and many:many
- **Indexing strategy**: MUST create indexes on all query fields; compound indexes for multi-field queries; monitor index usage with `explain()`
- **Schema validation**: MUST use MongoDB schema validation rules; enforce required fields, data types, and constraints
- **Denormalization for reads**: Optimize for read-heavy operations; acceptable to duplicate data if it reduces joins/lookups
- **Avoid unbounded arrays**: NEVER allow arrays to grow indefinitely; use pagination or separate collections for large datasets
- **Migration strategy**: MUST version schemas; use migration scripts for schema changes; support backward compatibility during transitions
- **Connection pooling**: MUST configure connection pools appropriately; monitor connection usage

**Rationale**: Poorly designed schemas cause performance degradation at scale; proper indexing and document design ensure sub-100ms query times even with millions of documents.

### VI. Reusable React Components and Hooks

**All React code MUST prioritize reusability and composition:**

- **Component design**: Single Responsibility Principle; each component does ONE thing well
- **Props interface**: MUST define TypeScript interfaces for all props; use descriptive names
- **Composition over inheritance**: Build complex UIs by composing simple components; avoid deep inheritance hierarchies
- **Custom hooks**: Extract reusable logic into custom hooks; prefix with `use`; e.g., `useCart()`, `useAuth()`, `useProductFilters()`
- **No business logic in components**: Components MUST be presentational; business logic belongs in hooks or services
- **Prop drilling limit**: MAX 2 levels; use Context or state management for deeper data passing
- **Component file structure**: One component per file; co-locate tests, styles, and types
- **Storybook documentation**: All reusable components MUST have Storybook stories showing all variants and states

**Rationale**: Reusable components reduce development time, ensure consistency, simplify testing, and enable design system evolution.

### VII. Accessibility (ARIA, Keyboard, Screen Readers)

**Accessibility MUST be built in from the start, not added later:**

- **Semantic HTML**: Use `<button>`, `<nav>`, `<main>`, `<article>`, `<aside>` appropriately; NEVER use `<div>` for interactive elements
- **ARIA labels**: MUST add `aria-label`, `aria-labelledby`, `aria-describedby` for screen readers where text isn't visible
- **Keyboard navigation**: ALL interactive elements MUST be reachable via keyboard; test with Tab, Enter, Space, Escape, Arrow keys
- **Focus management**: MUST have visible focus indicators (outline or ring); manage focus on modals, dropdowns, route changes
- **Color contrast**: MUST meet WCAG AA standards (4.5:1 for normal text, 3:1 for large text); verify with axe DevTools
- **Screen reader testing**: MUST test with NVDA (Windows) or VoiceOver (Mac) for critical user flows
- **Form accessibility**: MUST associate labels with inputs; provide helpful error messages; use `aria-invalid` and `aria-describedby` for errors
- **Skip navigation links**: MUST provide "Skip to main content" link for keyboard users
- **Alt text for images**: MUST provide descriptive alt text; use empty alt="" for decorative images

**Rationale**: 15% of the global population has disabilities; accessible design is inclusive, improves SEO, and is often legally required (ADA, Section 508).

### VIII. Test-Driven Development (TDD)

**Testing MUST be prioritized; tests MUST exist before production deployment:**

- **Unit tests**: MUST test individual functions, hooks, and components in isolation; aim for >80% coverage on business logic
- **Integration tests**: MUST test API endpoints end-to-end; verify request/response contracts, authentication, error handling
- **E2E tests**: MUST test critical user journeys (signup, login, add to cart, checkout); use Playwright or Cypress
- **Test pyramid**: Many unit tests → Fewer integration tests → Few E2E tests
- **No untested code in production**: ALL new features MUST have tests; CI pipeline MUST fail if tests fail
- **Test naming convention**: `describe("Feature", () => { it("should behavior when condition", () => {}) })`
- **Mock external dependencies**: MUST mock third-party APIs, payment gateways, email services in tests
- **Regression tests**: MUST add tests for every bug fix to prevent recurrence

**Rationale**: Tests catch bugs early, enable confident refactoring, serve as documentation, and reduce long-term maintenance costs.

### IX. Production-Ready Coding Standards

**All code MUST meet production quality before merging:**

- **TypeScript**: MUST use TypeScript for all frontend code; `strict: true` mode required; NO `any` types except where absolutely necessary with justification
- **Python type hints**: MUST use type hints for all function signatures; enable mypy strict mode
- **Code formatting**: MUST use Prettier (frontend) and Black (backend); auto-format on save; CI MUST enforce formatting
- **Linting**: MUST use ESLint (frontend) and Ruff (backend); NO linting errors allowed in PRs
- **Naming conventions**:
  - **Components**: PascalCase (e.g., `ProductCard.tsx`)
  - **Functions/hooks**: camelCase (e.g., `useCart()`, `calculateTotal()`)
  - **Constants**: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)
  - **Files**: kebab-case (e.g., `user-profile.tsx`) or PascalCase for components
  - **API routes**: kebab-case (e.g., `/api/user-profiles`)
  - **Database collections**: snake_case (e.g., `user_profiles`)
- **Error handling**: MUST handle errors gracefully; NEVER let unhandled exceptions crash the app; log errors with structured logging
- **Environment variables**: MUST use `.env` files; NEVER commit secrets; validate required env vars on startup
- **Git commits**: MUST use conventional commits format: `type(scope): description` (e.g., `feat(cart): add quantity selector`)
- **Code reviews**: ALL code MUST be reviewed by at least one other developer before merging

**Rationale**: Consistent standards reduce cognitive load, prevent bugs, enable automation, and make onboarding new developers faster.

### X. Dependency Management and Security

**Dependencies MUST be managed carefully to prevent bloat and vulnerabilities:**

- **Minimize dependencies**: MUST justify every dependency; ask "Can we build this in-house easily?" before adding libraries
- **Security scanning**: MUST run `npm audit` and `pip-audit` regularly; fix critical and high vulnerabilities within 48 hours
- **Version pinning**: MUST pin exact versions in `package-lock.json` and `requirements.txt`; avoid `^` or `~` in production
- **Bundle size monitoring**: MUST monitor frontend bundle size; keep main bundle <200KB gzipped; use code-splitting for routes
- **Tree-shaking**: MUST use ES modules; avoid CommonJS imports that prevent tree-shaking
- **Regular updates**: MUST update dependencies monthly; test thoroughly after updates
- **No deprecated packages**: MUST NOT use deprecated or unmaintained packages; replace with active alternatives

**Rationale**: Dependency vulnerabilities are a top attack vector; bloated bundles hurt performance and user experience; unmaintained packages introduce security and compatibility risks.

## Architecture Constraints

### Technology Stack (Non-Negotiable)

**Frontend:**
- React 18+ (with Hooks, NO class components)
- TypeScript 5+
- Tailwind CSS 3+ (utility-first styling)
- GSAP 3+ (animations only; NO anime.js, Framer Motion, etc.)
- Vite (build tool)
- React Router (client-side routing)
- Axios or Fetch API (HTTP client)

**Backend:**
- Python 3.11+
- FastAPI 0.100+ (async/await required)
- MongoDB 7+ (with Motor async driver)
- Pydantic 2+ (validation)
- PyJWT (JWT authentication)
- Uvicorn (ASGI server)

**Testing:**
- Frontend: Vitest + React Testing Library + Playwright
- Backend: pytest + httpx (for async tests)

**Development:**
- Git (version control)
- Docker + Docker Compose (local development)
- Pre-commit hooks (formatting, linting)

### Performance Budgets

**Frontend:**
- First Contentful Paint (FCP): <1.5s
- Largest Contentful Paint (LCP): <2.5s
- Time to Interactive (TTI): <3.5s
- Cumulative Layout Shift (CLS): <0.1
- Main bundle size: <200KB gzipped
- Initial page load: <3s on 3G network

**Backend:**
- API response time (p95): <200ms for read operations, <500ms for write operations
- Database query time (p95): <100ms
- Authentication overhead: <50ms
- Memory usage per request: <50MB
- Concurrent users: 1000+ without degradation

### Security Requirements

**Authentication & Authorization:**
- JWT-based authentication MUST be implemented
- Password hashing MUST use bcrypt with ≥12 rounds
- MUST implement account lockout after 5 failed login attempts (15min lockout)
- MUST require email verification for new accounts
- MUST implement password reset with time-limited tokens (1hr expiry)

**Data Protection:**
- MUST encrypt sensitive data at rest (payment info, passwords)
- MUST use HTTPS for all communication
- MUST implement CSRF protection for state-changing operations
- MUST sanitize user inputs to prevent XSS and injection attacks
- MUST implement Content Security Policy (CSP) headers

**Compliance:**
- MUST comply with GDPR (data export, deletion, consent)
- MUST comply with PCI-DSS for payment processing (use Stripe/PayPal, NEVER store card numbers)
- MUST log security events (login attempts, password changes, permission changes)

## Development Workflow

### Git Workflow

**Branch Strategy:**
- `main`: Production-ready code; MUST always be deployable
- `develop`: Integration branch for features
- `feature/<ticket-id>-<description>`: Feature branches (e.g., `feature/123-add-cart`)
- `bugfix/<ticket-id>-<description>`: Bug fix branches
- `hotfix/<ticket-id>-<description>`: Emergency production fixes

**Commit Rules:**
- MUST use conventional commits: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- MUST reference ticket numbers in commits: `feat(cart): add quantity selector (#123)`
- MUST write meaningful commit messages; explain WHY, not just WHAT

**Pull Request Requirements:**
- MUST include description of changes and testing performed
- MUST pass all CI checks (tests, linting, formatting)
- MUST have at least one approval from another developer
- MUST link to related ticket/issue
- MUST update documentation if API or behavior changes

### Code Review Standards

**Reviewers MUST check for:**
- ✅ Code meets all constitutional principles
- ✅ Tests are included and passing
- ✅ No security vulnerabilities introduced
- ✅ Performance impact is acceptable
- ✅ Accessibility requirements met
- ✅ Error handling is comprehensive
- ✅ Documentation is updated
- ✅ No unnecessary dependencies added
- ✅ Code is readable and maintainable
- ✅ Naming conventions followed

**Review Response Time:**
- MUST review PRs within 24 hours on business days
- Critical bug fixes MUST be reviewed within 4 hours

### CI/CD Pipeline

**CI Requirements (MUST pass before merge):**
1. Linting (ESLint, Ruff)
2. Formatting (Prettier, Black)
3. Type checking (TypeScript, mypy)
4. Unit tests (>80% coverage)
5. Integration tests
6. Security scanning (npm audit, pip-audit)
7. Build verification

**CD Requirements:**
- Automated deployment to staging on merge to `develop`
- Manual approval required for production deployment
- MUST run smoke tests after deployment
- MUST be able to rollback within 5 minutes if issues detected

## Governance

### Constitution Authority

**This constitution is the supreme governing document for the Digital Store E-Commerce project:**

- ALL code, architecture, and processes MUST comply with these principles
- When conflicts arise, this constitution takes precedence over individual preferences or external conventions
- Violations MUST be caught in code review and rejected
- Repeated violations MUST be escalated to technical leads

### Amendment Process

**Constitutional amendments require:**

1. **Proposal**: Written proposal with rationale, impact analysis, and migration plan
2. **Review**: Technical lead and at least 2 senior developers MUST review
3. **Approval**: Requires consensus from majority of development team
4. **Documentation**: MUST document in ADR (Architecture Decision Record)
5. **Migration**: MUST provide migration plan for existing code
6. **Communication**: MUST announce changes to entire team before taking effect

### Version Updates

**Constitution versioning follows semantic versioning:**

- **MAJOR (X.0.0)**: Backward-incompatible changes (principle removal, fundamental policy changes)
- **MINOR (x.Y.0)**: New principles added, expanded guidance, new mandatory practices
- **PATCH (x.y.Z)**: Clarifications, wording improvements, typo fixes, no behavioral changes

### Complexity Justification

**Any deviation from these principles MUST be justified:**

- Create an ADR documenting the decision, alternatives considered, and tradeoffs
- Get approval from technical lead
- Add technical debt ticket to address deviation in the future (if temporary)
- Document the deviation in code comments with link to ADR

**Examples requiring justification:**
- Adding a dependency outside the approved stack
- Skipping tests for a feature (MUST have exceptional reason)
- Using class components instead of functional components
- Implementing custom authentication instead of JWT
- Storing sensitive data without encryption

### Compliance Review

**Periodic compliance audits MUST be conducted:**

- **Monthly**: Automated scans for linting, formatting, security vulnerabilities
- **Quarterly**: Manual architecture review to verify adherence to clean architecture
- **Before major releases**: Full audit of all principles; create compliance report

**Compliance Report MUST include:**
- Violations found and severity
- Remediation plan with timeline
- Risk assessment
- Sign-off from technical lead

---

**Version**: 1.0.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2025-12-29
