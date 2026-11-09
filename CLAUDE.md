# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Batch tool that reads every CSV in `input/` and writes one Plotly line-chart HTML file per CSV to `output/`. Each chart plots all numeric columns against the DataFrame index.

## Commands

Dependencies are managed with [pixi](https://pixi.sh).

```bash
pixi install     # install dependencies into the local .pixi env
pixi run run      # process input/*.csv -> output/*.html (runs `python -m src.main`)
```

There is no test suite or linter configured. The only task defined in `pixi.toml` is `run`.

## Architecture

Single module, `src/main.py`, structured as a pipeline of small pure functions composed by `main()`:

- Paths are derived from `PROJECT_ROOT` (parent of `src/`), so `input/` and `output/` are resolved relative to the repo root regardless of the working directory.
- `find_csv_files` → `load_csv` → `plot_dataframe` → `process_file` is the per-file flow; `main()` creates `output/`, iterates sorted CSVs, and writes one HTML per file.
- Error isolation is intentional: `main()` catches `pd.errors.ParserError`, `ValueError` (raised by `plot_dataframe` when a file has no numeric columns), and `OSError` per file and prints a "Skipped" message, so one bad CSV never aborts the batch.

`input/` and `output/` are git-ignored data folders (not committed); create `input/` and add CSVs before running.
