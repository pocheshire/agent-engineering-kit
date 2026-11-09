# Adding a platform adapter

Use the host's current official documentation. Add only its required manifest
and discovery metadata; point to the existing self-contained skill and core.
Do not copy CONTRACT.md into another adapter or add capabilities via hidden hooks.

Validate metadata, then install in an isolated host profile. Test discovery,
natural-language activation, core version resolution, one setup operation, update,
removal and missing-source diagnostics. Inspect actual actions independently.
Record the host/version, raw evidence and unresolved limitations in the platform
matrix. Static-only adapters remain candidates. Official directory review is a
separate process from a repository marketplace. Never imply endorsement.
