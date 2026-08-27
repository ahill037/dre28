# Presidential Campaign Project Plan

- Status: Draft planning artifact
- Prepared: 2026-08-26
- Format: Standalone HTML campaign planning document
- Primary file: `index.html`

## Purpose

- This repository contains a source-backed project plan for exploring and preparing a U.S. presidential campaign.
- It covers filing readiness, campaign compliance setup, official website requirements, platform-development workstreams, first 90-day actions, deliverables, risks, and source links to refresh.

## Contents

- `index.html`: Browser-friendly version of the campaign project plan.
- `Presidential_Campaign_Project_Plan.html`: Named copy of the same HTML artifact for provenance.
- `mcp/`: Narrow onboarding MCP server for the GX10.

## Public Links

- Repository: https://github.com/ahill037/dre28
- Primary domain: https://ayemane.com
- GitHub Pages source URL: https://ahill037.github.io/dre28/ redirects to the custom domain after GitHub Pages custom-domain configuration.

## Domain Setup

- Intended production domain: `ayemane.com`
- GitHub Pages custom-domain file: `CNAME`
- DNS status on 2026-08-27: `ayemane.com` and `www.ayemane.com` resolve to Squarespace records, so registrar/DNS changes are still required before this repository serves the custom domain.
- Required apex `A` records for GitHub Pages:
  - `@` -> `185.199.108.153`
  - `@` -> `185.199.109.153`
  - `@` -> `185.199.110.153`
  - `@` -> `185.199.111.153`
- Optional apex `AAAA` records for IPv6:
  - `@` -> `2606:50c0:8000::153`
  - `@` -> `2606:50c0:8001::153`
  - `@` -> `2606:50c0:8002::153`
  - `@` -> `2606:50c0:8003::153`
- Required `www` record:
  - `www` -> `ahill037.github.io`
- After DNS propagates and GitHub issues the certificate, enable HTTPS enforcement in GitHub Pages settings.

## Important Notes

- This is a planning artifact, not legal advice.
- This is not an official declaration of candidacy.
- Do not treat placeholder filing, committee, treasurer, contribution, or FEC fields as active campaign facts.
- Federal, state, party, ballot-access, tax, employment, and campaign-finance counsel should review before fundraising, filing, public launch, donation processing, or publication of final policy claims.

## Policy Pillars In Draft

- Empowerment through economic opportunity.
- Equality and accountability in law enforcement.
- Equip and empower the military, teachers, students, and allies.
- Reduce the federal budget's reliance on debt.

## Local Viewing

- Open `index.html` in a browser to view the plan.

## GX10 Onboarding MCP

- Service name: `dre28-onboarding-mcp.service`
- Default endpoint on GX10: `http://127.0.0.1:8790/mcp`
- Health endpoint on GX10: `http://127.0.0.1:8790/healthz`
- Purpose: serve the dre28 onboarding prompt, project brief, and DreAnalytica communication policy.
- Boundary: onboarding/read-only only; no shell, DB, broker, filing, donation, or credential tools.

