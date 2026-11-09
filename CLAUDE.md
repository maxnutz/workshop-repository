# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Batch tool that reads every CSV in `input/` and writes one Plotly line-chart HTML file per CSV to `output/`. Each chart plots all numeric columns against the DataFrame index.

## Commands

Dependencies are managed with [pixi](https://pixi.sh).

```bash
pixi install     # install dependencies into the local .pixi env
pixi run run      # process input/*.csv -> output/*.html (runs `python -m src.main`)
pixi run count-p  # count letter p (any case) in resources/*.xlsx (runs `python -m src.count_p`)
```

There is no test suite or linter configured. Tasks defined in `pixi.toml`: `run` and `count-p`.

## Architecture

Two independent modules in `src/`. `src/main.py` is the CSV plotting pipeline, structured as a pipeline of small pure functions composed by `main()`:

- Paths are derived from `PROJECT_ROOT` (parent of `src/`), so `input/` and `output/` are resolved relative to the repo root regardless of the working directory.
- `find_csv_files` → `load_csv` → `plot_dataframe` → `process_file` is the per-file flow; `main()` creates `output/`, iterates sorted CSVs, and writes one HTML per file.
- Error isolation is intentional: `main()` catches `pd.errors.ParserError`, `ValueError` (raised by `plot_dataframe` when a file has no numeric columns), and `OSError` per file and prints a "Skipped" message, so one bad CSV never aborts the batch.

`src/count_p.py` is a separate evaluation: it reads every sheet of each `resources/*.xlsx` as strings and prints per-sheet and total counts of `p`.

`input/`, `output/` and `resources/` are git-ignored data folders (not committed); create `input/` and add CSVs before running.
