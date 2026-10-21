"""Read CSV files from ``input/`` and write Plotly HTML plots to ``output/``."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"


def find_csv_files(input_dir: Path) -> list[Path]:
    """Return all ``*.csv`` files in ``input_dir`` (non-recursive), sorted by name."""
    return sorted(input_dir.glob("*.csv"))


def load_csv(csv_path: Path) -> pd.DataFrame:
    """Load a single CSV file into a DataFrame."""
    return pd.read_csv(csv_path)


def plot_dataframe(df: pd.DataFrame, title: str) -> "px.Figure":
    """Create a line plot of all numeric columns against the DataFrame index."""
    numeric = df.select_dtypes("number")
    if numeric.empty:
        raise ValueError(f"{title!r} has no numeric columns to plot")
    return px.line(numeric, title=title)


def process_file(csv_path: Path, output_dir: Path) -> Path:
    """Evaluate one CSV file and write its plot as HTML. Returns the output path."""
    df = load_csv(csv_path)
    figure = plot_dataframe(df, title=csv_path.stem)
    output_path = output_dir / f"{csv_path.stem}.html"
    figure.write_html(output_path)
    return output_path


def main() -> None:
    """Process every CSV in ``input/`` and write a plot per file to ``output/``."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    csv_files = find_csv_files(INPUT_DIR)
    if not csv_files:
        print(f"No CSV files found in {INPUT_DIR}")
        return

    for csv_path in csv_files:
        try:
            output_path = process_file(csv_path, OUTPUT_DIR)
        except (pd.errors.ParserError, ValueError, OSError) as error:
            print(f"Skipped {csv_path.name}: {error}")
            continue
        print(f"Wrote {output_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
