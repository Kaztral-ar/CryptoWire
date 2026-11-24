# CryptoWire Implementation Plan

## Stage 1 — Architecture and repository scaffold
- [x] Define Discord-to-Binance Square workflow
- [x] Select Python and discord.py
- [x] Define approval-first publishing policy
- [x] Establish initial repository structure

## Stage 2 — Discord foundation
- [x] Implement Discord client and lifecycle
- [x] Register and synchronize slash commands
- [x] Implement default-deny submitter authorization
- [x] Restrict intake to the configured submission channel
- [x] Add help/status commands and graceful shutdown
- [x] Add permission tests and setup documentation

## Stage 3 — Intake and drafts
- [ ] Accept text submissions into persistent drafts
- [ ] Download attachments safely with size limits
- [ ] Validate MIME type and publishing compatibility
- [ ] Create versioned drafts
- [ ] Render Discord previews

## Stage 4 — Approval workflow
- [ ] Add approve/reject/edit/cancel controls
- [ ] Bind approvals to immutable draft versions
- [ ] Enforce administrator-only decisions
- [ ] Add queue state transitions
- [ ] Prevent concurrent approval and duplicate enqueue

## Stage 5 — Binance Square adapter
- [ ] Verify current official integration requirements
- [ ] Document Node.js runtime and installation
- [ ] Implement Python adapter and subprocess isolation
- [ ] Keep API credentials out of command arguments and logs
- [ ] Map supported text, image, article, and video formats
- [ ] Handle rate limits and ambiguous outcomes safely
- [ ] Add dry-run mode before live publishing

## Stage 6 — Persistence and audit
- [ ] Add SQLAlchemy models and migrations
- [ ] Persist drafts, attachments, approvals, jobs, and history
- [ ] Add structured audit events
- [ ] Add retention and cleanup policies

## Stage 7 — Testing and deployment
- [ ] Unit and integration tests
- [ ] Mock Binance adapter tests
- [ ] Permission and abuse-case tests
- [ ] Deployment and recovery guide
- [ ] Production readiness checklist

## Safety invariants

1. Receiving content never publishes it.
2. Only an authorized administrator can approve.
3. Editing a draft invalidates approval for its previous version.
4. Publishing requires an approved, current draft version.
5. Secrets are never written to logs or committed.
6. A timeout after a publish request is an unknown outcome until reconciled; do not blindly retry.
