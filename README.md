# workshop-repository
This repository evaluates a csv-file and creates meaninful plots with plotly.

## Structure
- `input/` - folder: csv-files (not git versioned)
- `output/` - folder: html-output files (not git versioned)
- `src/main.py` - reads every CSV in `input/` and writes one Plotly HTML plot per file to `output/`

## Setup

This project uses [pixi](https://pixi.sh) for dependency management.

```bash
pixi install
```

## Usage

1. Put your CSV files into the `input/` folder.
2. Run the evaluation:

   ```bash
   pixi run run
   ```

3. Find the generated plots as `output/<csv-name>.html`.

Each CSV is plotted as a line chart of its numeric columns. Files with no
numeric columns (or that fail to parse) are skipped with a message, so one
bad file does not stop the batch.

This is a change. 