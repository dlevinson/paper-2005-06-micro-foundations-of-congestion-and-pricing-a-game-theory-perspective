# Package Status: Micro-Foundations Of Congestion And Pricing

Updated: 2026-06-21 AEST

## Audit State

- Row ID: `paper-2005-06`
- Pipeline: `UPLOADED`
- Upload action: `code_only_candidate`
- Packaging status: `corrected_reconstruction_added`
- Rights status: `likely_clear_with_provenance`
- Controlled access status: `none`
- Human subjects status: `no`
- Original DOI: https://doi.org/10.1016/j.tra.2005.02.021
- Corrigendum DOI: https://doi.org/10.1016/j.tra.2015.05.009

## Verification Result

- The historical three-player workbook is preserved but is not corrected.
- The corrigendum probability correction is implemented and all probability rows sum to one.
- The exact published corrected Table 11 is included as a benchmark.
- The arithmetic `ISC - IPC` reconstruction exactly matches 10 of 12 Table 11 rows.
- The remaining two discrepancies are cost-tied weak equilibria omitted from two published rows.
- The source note's printed `+0.5E` epsilon sign is preserved as a comparison, not used as the corrected rule.

## Package Checks

- Files in manifest: 19
- Paper reference files: 2
- Historical workbook files: 8
- Corrected/reconstruction code or workbook files: 2
- Benchmark data files: 1
- License files: 2
- No empirical or personal data are present.

## Upload Boundary

- Use `PACKAGE_MANIFEST.csv` as the file checklist.
- Treat files under `paper/` as local reference copies unless rights review explicitly clears them.
- Code and model workbooks are MIT licensed; benchmark data and documentation are CC BY 4.0.
