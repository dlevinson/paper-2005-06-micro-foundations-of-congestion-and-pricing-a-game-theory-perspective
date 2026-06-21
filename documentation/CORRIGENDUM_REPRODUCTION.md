# Corrigendum Reproduction

The 2015 corrigendum is a substantive part of this paper's computational record:

- David Levinson (2005), DOI: https://doi.org/10.1016/j.tra.2005.02.021
- David Levinson and Nicholas Janusch (2015), DOI: https://doi.org/10.1016/j.tra.2015.05.009

## What Was Wrong With The Uploaded Legacy Workbook

The deposited `game3player_pricing_model_original` workbook is the 2003 model used for the original article. It retains the error corrected on page 700: when Player A departs late and Players B and C depart early and late, respectively, the probability that A arrives really late is recorded as `0` rather than `0.5`. The resulting probability distribution sums to `0.5`.

Its three-player priced-equilibrium results are therefore not the corrected Table 11 and should be treated as historical source code, not as the corrected reproduction workbook.

## Reconstructed Materials

- `code/reproduce_corrigendum.py` reconstructs FIFO arrival outcomes, private costs, the Janusch note's toll placements, the arithmetic implied by its stated `ISC - IPC` method, and weak pure-strategy Nash equilibria. It also reports the result from the note's displayed `+0.5E` sign for comparison.
- `code/model_workbooks/corrected_xlsx/three_player_corrigendum_reconstruction.xlsx` provides the same reconstruction in an auditable spreadsheet.
- `metadata/CORRIGENDUM_BENCHMARKS.csv` records the exact corrected Table 11 as published.

The corrected probability is implemented directly by the FIFO queue logic rather than as a special-case patch.

## The Epsilon Toll Sign

For the `eeo` congestion scenario, the source table states:

- incremental social cost: `ISC = 2D + L`;
- incremental private cost: `IPC = 0.5(E + D)`; and
- toll: `ISC - IPC`.

The subtraction is therefore:

`epsilon = MAX(1.5D + L - 0.5E, 0)`.

The displayed formula instead has `+0.5E`. That sign cannot result from the
stated subtraction and is treated as a typographical error in the corrected
reconstruction.

## What Assumptions Explain The Two Residual Discrepancies?

No standard or documented model assumption explains them.

With `D=0` and the arithmetic-correct epsilon toll, the two disputed pattern
families are weak equilibria because their relevant unilateral deviations are
cost ties:

- in `eeo`, all three players have generalized cost `L`; changing an `e` to
  `o` or `l`, or changing the `o` to `e` or `l`, does not reduce cost below
  `L`;
- in `eoo`, the early player has cost `E` and the on-time players have cost
  `L`; for the three benchmark parameter sets, no player has a strictly
  lower-cost unilateral deviation.

Consequently the arithmetic model includes `eee`, all three `eeo`
permutations, all three `eoo` permutations, and all six `eol` permutations:
13 priced weak equilibria in each of the positive-`E`, `D=0` benchmark cases.

The corrigendum reports:

- `E=1, D=0, L=1`: `eeo` included but `eoo` omitted;
- `E=4, D=0, L=3`: `eoo` included but `eeo` omitted;
- `E=3, D=0, L=4`: both included.

Changing from weak to strict equilibrium does not recover the table: it yields
zero strict equilibria in all three cases because cost ties remain. The
published pattern therefore requires an unstated, case-specific selection
among tied weak equilibria. The most parsimonious interpretation is two
remaining enumeration or transcription omissions in corrected Table 11.

The corrected mathematical results are:

- `E=1, D=0, L=1`: 13 priced equilibria, adding the three `eoo` permutations;
- `E=4, D=0, L=3`: 13 priced equilibria, adding the three `eeo` permutations.

The `E=3, D=0, L=4` row's published count of 13 is reproduced once the epsilon
sign is corrected.

For transparency, the workbook separates the exact published table, the
arithmetic-correct reconstruction, the printed-sign comparison, and explicit
pass/fail checks.

No undocumented rule has been invented to force the two residual rows to pass.
