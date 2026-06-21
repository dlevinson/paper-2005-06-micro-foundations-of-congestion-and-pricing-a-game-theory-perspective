# Micro-Foundations Of Congestion And Pricing: Article And Corrigendum

## Publications Covered By This Repository

- Row ID: `paper-2005-06`
- Original article: David Levinson (2005), “Micro-Foundations Of Congestion And Pricing: A Game Theory Perspective,” *Transportation Research Part A* 39(7–9), 691–704. https://doi.org/10.1016/j.tra.2005.02.021
- Corrigendum: David Levinson and Nicholas Janusch (2015), “Corrigendum to ‘Micro-Foundations Of Congestion And Pricing: A Game Theory Perspective’,” *Transportation Research Part A* 78, 144–145. https://doi.org/10.1016/j.tra.2015.05.009
- Repository handle/source pointer: https://hdl.handle.net/11299/179927

This is the single data-and-code repository for both linked publications. The
2015 corrigendum corrects the 2005 article and shares its computational record;
it should not be assigned a separate GitHub repository. A machine-readable
publication crosswalk is in `metadata/PUBLICATIONS.csv`.

## Reproduction Status

The historical 2003 three-player workbook in this repository does **not** reproduce the 2015 corrigendum. It retains the original probability error and the pre-corrigendum priced-equilibrium calculations.

This package now separates three things:

1. the untouched historical Excel workbooks used for the 2005 article;
2. the exact corrected Table 11 reported in the 2015 corrigendum; and
3. a new equation-based reconstruction using corrected FIFO arrival probabilities and the Janusch source note's stated `Toll = ISC - IPC` method.

The reconstruction reproduces ten of the twelve corrected Table 11 rows exactly. The two residual discrepancies are omissions in the published table:

- `E=1, D=0, L=1`: the weak-equilibrium model gives 13 priced equilibria; Table 11 reports 10 and omits the three `eoo` permutations;
- `E=4, D=0, L=3`: the weak-equilibrium model gives 13 priced equilibria; Table 11 reports 10 and omits the three `eeo` permutations.

The source note prints an `eeo` toll with a `+0.5E` term even though its stated
`ISC - IPC` arithmetic gives `-0.5E`. Using the arithmetic-correct sign makes
both `eeo` and `eoo` weak equilibria in all three positive-`E`, zero-delay
benchmark cases. Strict equilibrium is not the missing assumption: it produces
no equilibria in those cases. Reproducing Table 11 would require an unstated,
case-specific selection among cost-tied weak equilibria.

## Corrected And Reconstructed Materials

- `code/reproduce_corrigendum.py`: dependency-free Python reconstruction and benchmark audit.
- `code/model_workbooks/corrected_xlsx/three_player_corrigendum_reconstruction.xlsx`: editable, formula-driven workbook with all 64 profiles, all twelve benchmark cases, corrected arrival probabilities, toll rules, and pass/fail checks.
- `metadata/CORRIGENDUM_BENCHMARKS.csv`: machine-readable transcription of the corrected Table 11.
- `metadata/PUBLICATIONS.csv`: citations and DOI relationship for the original article and corrigendum.
- `documentation/CORRIGENDUM_REPRODUCTION.md`: detailed provenance and interpretation.

Run:

```bash
python3 code/reproduce_corrigendum.py
```

## Historical Source Workbooks

- `code/model_workbooks/original/microfoundations_queue_model_original.xls`
- `code/model_workbooks/original/game2player_pricing_model_v2_original.xls`
- `code/model_workbooks/original/game3player_pricing_model_original.xls`
- `code/model_workbooks/original/marginal_delay_supporting_original.xls`
- `code/model_workbooks/modernized_xlsx/*.xlsx`: LibreOffice conversions of the historical files.

The historical workbooks are retained for provenance and should not be described as corrected.

## Archive Status

- Pipeline: `UPLOADED`
- Upload action: `code_only_candidate`
- Rights status: `likely_clear_with_provenance`
- Human subjects: none
- Controlled access: none
- Asset match: `historical_source_plus_corrigendum_reconstruction`
- Reproduction assessment: corrected probability and published benchmark table are captured; the arithmetic `ISC - IPC` reconstruction is exact for 10 of 12 rows and identifies two residual table omissions.

## Exclusions

- Publisher PDFs are local audit references and are not relicensed here.
- Correspondence, reviewer material, presentations, publisher paperwork, and manuscript drafts remain excluded.
- The 2014 `Janusch/Game3player-priced1 copy.xls` was inspected. It fixes the key probability cell but still retains the old equilibrium/toll implementation, so it is evidence rather than the corrected model.

## License

- Code and model workbooks: MIT.
- Benchmark data and repository documentation: CC BY 4.0.
- Publisher PDF: not relicensed.

See `LICENSE.md`.

Corrected package review: 2026-06-22.
