# Migration Governance

This template follows a safety-first migration strategy.

## Principles

- Every schema change must be represented by a migration file
- Keep migrations small and reversible
- Avoid mixed changes (schema + unrelated refactor) in one migration

## Recommended Pattern

1. Expand: add nullable columns / new tables first
2. Migrate data in background or script
3. Contract: remove old columns only after application no longer depends on them

## Rollback Rules

- Every migration should provide a valid downgrade path
- Test upgrade + downgrade in staging before production rollout

## Release Checklist

- Migration SQL reviewed
- Backward compatibility evaluated
- Rollback plan documented
- Runtime metrics and alerts prepared
