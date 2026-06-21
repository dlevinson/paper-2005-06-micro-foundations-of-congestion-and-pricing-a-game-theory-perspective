# Package Status: Micro-Foundations Of Congestion And Pricing

Updated: 2026-06-22 AEST

## Audit State

- Row ID: `paper-2005-06`
- Repository scope: one repository covering the 2005 article and its 2015 corrigendum
- Publications represented: 2
- Separate corrigendum repository: none; do not create one
- Pipeline: `UPLOADED`
- Upload action: `code_only_candidate`
- Packaging status: `corrected_reconstruction_added`
- Rights status: `likely_clear_with_provenance`
- Controlled access status: `none`
- Human subjects status: `no`
- Original DOI: https://doi.org/10.1016/j.tra.2005.02.021
- Corrigendum DOI: https://doi.org/10.1016/j.tra.2015.05.009

## Verification Result

- The paper develops a game-theoretic micro-foundation for congestion and
  shows how pricing can support cooperation and lower collective costs.
- Both the original article and corrigendum are included in `paper/`.
- The historical three-player workbook is preserved but is not corrected.
- The corrigendum probability correction is implemented and all probability rows sum to one.
- The exact published corrected Table 11 is included as a benchmark.
- The arithmetic `ISC - IPC` reconstruction exactly matches 10 of 12 Table 11 rows.
- The remaining two discrepancies are cost-tied weak equilibria omitted from two published rows.
- The source note's printed `+0.5E` epsilon sign is preserved as a comparison, not used as the corrected rule.

## Package Checks

- Files in manifest: 21
- Publications listed: 2
- Publication PDF files: 2
- Paper-reference documentation files: 1
- Historical workbook files: 8
- Corrected/reconstruction code or workbook files: 2
- Benchmark data files: 1
- License files: 2
- No empirical or personal data are present.

## Upload Boundary

- Use `PACKAGE_MANIFEST.csv` as the file checklist.
- Publication PDFs under `paper/` retain their publisher or repository terms.
- Code and model workbooks are MIT licensed; benchmark data and documentation are CC BY 4.0.
