# Releasing

1. Update VERSION, core/VERSION, adapter manifests and CHANGELOG.md together.
2. Run `python3 scripts/validate.py`, independent review and appropriate host and
   behavioral probes. Record categories and limitations in validation.md.
3. The release gate and ZIP builder use the same tracked-file inventory. The gate
   also scans eligible untracked files for privacy and link issues. Both reject
   tracked files under reserved local/generated paths such as `.scratch/` and
   `dist/`; do not force-add these paths to a release. Review the full publication
   file set and Git history for secrets, personal paths, private evidence and
   provenance. Do not publish unlicensed source.
4. With publication authority, commit, push main, verify remote SHA and wait for
   actual GitHub Actions results. A local green check is not server CI.
5. Create the matching `v<version>` tag, run `python3 scripts/package_release.py`,
   and attach the ZIP and SHA256SUMS to a GitHub Release. Use prerelease status
   whenever stable acceptance is incomplete. Verify assets and public file URLs.

The package script includes tracked files only. It does not upload or publish.
Directory submissions require a separate owner account/review and must never be
inferred from GitHub publication or a working repository marketplace.
