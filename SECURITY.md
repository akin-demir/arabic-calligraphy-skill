# Security

The 0.1 development candidate is the only maintained series; no public stable release exists yet. Report vulnerabilities through GitHub private vulnerability reporting if enabled, or privately contact the owner. If no private channel is enabled, request a security contact without publishing exploit details.

Rendering is offline and does not evaluate Markdown code, HTML, shell substitutions or URLs. Only bundled hash-checked fonts are accepted; arbitrary user font parsing is not exposed. Native font/rendering libraries still need security updates. Process untrusted content in an isolated worker with resource/time limits; do not run it with elevated privileges. Validate output paths at the calling application's trust boundary and do not build them from untrusted names. Preserve originals when handling PDFs externally.

Limits: 100000 text characters, 1 MB CLI document input, 32 million canvas pixels, 200 document pages. PNG/SVG/PDF outputs replace explicit regular output paths atomically; symlinks are refused. There is no telemetry or external AI call. This is defense in depth, not a guarantee that native parsers are invulnerable.

CI audits Python dependencies and uses read-only workflow permissions. Dependency updates must pass the corpus, export and visual checks. Native OS security updates remain the deployer's responsibility. Live security scanning results and repository-level security features are recorded in GITHUB_SETUP.md; do not infer them from workflow files alone.
