# ATLAS Clarus × ARBE λ* — Independent Reviewer Packet v0.2

Status: `REVIEW_REQUEST — CONFIRMATORY RUN NOT AUTHORISED`

This packet supports an independent methodological review of Study A Protocol
v0.2 before any confirmatory analysis or external sample acquisition begins.

## Required review order

1. Verify `SHA256SUMS.txt` and `PROTOCOL_LOCK.json`.
2. Read `PILOT_BOUNDARY.md` before examining the protocol.
3. Review `PROTOCOL_V0_2.md` and `analysis_plan_v0_2.json` together.
4. Complete every item in `REVIEW_CHECKLIST.md`.
5. Record findings in `REVIEW_FORM.md` and `review_record_template.json`.
6. Sign and date the independence declaration.

## Decision classes

- `ACCEPT_WITHOUT_CHANGE`: no major methodological deficiency.
- `ACCEPT_WITH_MINOR_CLARIFICATIONS`: wording or implementation detail only;
  confirm that no success threshold or analytical degree of freedom changes.
- `REVISION_REQUIRED`: Protocol v0.3 is required before confirmation.
- `REJECT`: the proposed design cannot answer the stated research question.

An unresolved major finding keeps `confirmatory_run_authorised = false`.

## Independence requirement

The reviewer must not be an author of Protocol v0.2, must disclose relevant
relationships or interests, and must not use unpublished outcome information.
Review by the protocol authors may improve quality but is not independent
review.
