# Issue #2 QA v1

Reviewed implementation: `1606005a608f27074847573df069a699f3806be1`, base `e4e7cc4`.

| AC | Observable check | Result |
|---|---|---|
| 1 | Parse actual template frontmatter with safe YAML loader; check name/about/title and feature default | PASS |
| 2 | Check six standard headings, independent Verification prompts, unchecked criteria and exact None dependency | PASS |
| 3 | Check README request/board URLs, relative document targets and submission instructions; run factory and policy tests | PASS, 8 tests |

Rerun from the repository root:

```sh
python3 docs/super-board/runs/issue-2-qa-v1/check_request.py
python3 scripts/check_factory.py
python3 -m unittest discover -s tests -v
```

Evidence: [artifact checks](check.log), [factory checks](factory.log), [policy tests](tests.log), [rerunnable check](check_request.py).

Independent review performed inline per Codex lane instruction: standards 0, spec 0. Security pass: no exploitable findings; implementation is Markdown only, without executable input paths or permission changes. Compared the full base-to-head diff: only template and README changed before QA evidence.

Truth-check: YAML and actual Markdown checks support all three ACs; factory checks are reported only as factory checks. GitHub New issue loading is not exercised because the template is not on the default branch yet. No screenshots: documentation artifact checks, no application UI change. No app verifier map configured; ordinary issue-scoped checks used. No High test gaps; optional low gap is post-merge GitHub template-picker smoke testing. No merge or policy changes performed.

Existing author notes confirmed: 2 file summaries, 1 inline note, no human replies or QA findings. Original claim call partially succeeded (assignee present) but label was absent; reconciled with read-only issue evidence, created missing label, then applied label separately without replaying the claim.
