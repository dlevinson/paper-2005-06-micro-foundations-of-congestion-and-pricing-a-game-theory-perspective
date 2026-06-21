# Micro-Foundations Of Congestion And Pricing: Article And Corrigendum

## Contribution

This paper develops congestion and congestion-pricing theory from the
strategic interaction of individual travelers. Using deliberately simple
two-player and three-player departure-time games, it connects travelers'
valuations of early arrival, late arrival, and journey delay to the emergence
of queues and Nash equilibria.

The analysis shows how congestion can arise from individually rational choices
and how pricing can act as a cooperation mechanism that aligns private
incentives with lower collective cost. The three-player extension also makes
the congestion externality especially clear: one traveler's action can impose
delay on another traveler who did not create the queue. This provides a
transparent micro-level bridge among game theory, bottleneck queuing, schedule
delay, and road pricing.

The 2015 corrigendum strengthens this contribution by revising the
three-player probability, cost, and equilibrium calculations. This repository
preserves the original computational history while providing a corrected,
auditable implementation of the model.

## Publications Covered By This Repository

- Row ID: `paper-2005-06`
- Original article: David Levinson (2005), “Micro-Foundations Of Congestion And Pricing: A Game Theory Perspective,” *Transportation Research Part A* 39(7–9), 691–704. https://doi.org/10.1016/j.tra.2005.02.021 — [repository copy](paper/Microfoundations.pdf)
- Corrigendum: David Levinson and Nicholas Janusch (2015), “Corrigendum to ‘Micro-Foundations Of Congestion And Pricing: A Game Theory Perspective’,” *Transportation Research Part A* 78, 144–145. https://doi.org/10.1016/j.tra.2015.05.009 — [repository copy](paper/Corrigendum.pdf)
- Repository handle/source pointer: https://hdl.handle.net/11299/179927

This is the single data-and-code repository for both linked publications. The
2015 corrigendum corrects the 2005 article and shares its computational record;
it should not be assigned a separate GitHub repository. A machine-readable
publication crosswalk is in `metadata/PUBLICATIONS.csv`.

## Computational Record

This package brings together:

1. the untouched historical Excel workbooks used for the 2005 article;
2. the exact corrected Table 11 reported in the 2015 corrigendum; and
3. a new equation-based reconstruction using corrected FIFO arrival probabilities and the Janusch source note's stated `Toll = ISC - IPC` method.

The historical workbook is retained as provenance for the original model. The
new reconstruction implements the corrected probability structure and
reproduces ten of the twelve published Table 11 rows exactly.

## Technical Reproduction Note

Two published rows omit weak equilibria implied by the corrected generalized
model:

- `E=1, D=0, L=1`: the weak-equilibrium model gives 13 priced equilibria; Table 11 reports 10 and omits the three `eoo` permutations;
- `E=4, D=0, L=3`: the weak-equilibrium model gives 13 priced equilibria; Table 11 reports 10 and omits the three `eeo` permutations.

The source note's stated `ISC - IPC` method gives an `eeo` toll with a
`-0.5E` term. Applying that arithmetic consistently makes both `eeo` and
`eoo` weak equilibria in all three positive-`E`, zero-delay benchmark cases.
The repository records the published results and the generalized
equation-derived results separately.

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

- The original article and corrigendum PDFs are included as publication
  reference copies and retain their publisher or repository terms.
- Correspondence, reviewer material, presentations, publisher paperwork, and manuscript drafts remain excluded.
- The 2014 `Janusch/Game3player-priced1 copy.xls` was inspected. It fixes the key probability cell but still retains the old equilibrium/toll implementation, so it is evidence rather than the corrected model.

## License

- Code and model workbooks: MIT.
- Benchmark data and repository documentation: CC BY 4.0.
- Publication PDFs: not relicensed.

See `LICENSE.md`.

Corrected package review: 2026-06-22.
