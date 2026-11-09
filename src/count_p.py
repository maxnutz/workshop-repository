"""Count occurrences of the letter ``p`` (any case) in every Excel file in ``resources/``."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESOURCES_DIR = PROJECT_ROOT / "resources"
LETTER = "p"


def find_excel_files(resources_dir: Path) -> list[Path]:
    """Return all ``*.xlsx`` files in ``resources_dir`` (non-recursive), sorted by name."""
    return sorted(resources_dir.glob("*.xlsx"))


def load_sheets(excel_path: Path) -> dict[str, pd.DataFrame]:
    """Load every sheet as strings, keeping the header row as a regular cell row."""
    return pd.read_excel(excel_path, sheet_name=None, header=None, dtype=str)


def count_letter(df: pd.DataFrame, letter: str = LETTER) -> int:
    """Count case-insensitive occurrences of ``letter`` across all non-empty cells."""
    cells = df.stack()  # drops empty (NaN) cells
    return int(cells.str.lower().str.count(letter.lower()).sum())


def count_file(excel_path: Path) -> dict[str, int]:
    """Return the letter count per sheet for one Excel file."""
    return {name: count_letter(df) for name, df in load_sheets(excel_path).items()}


def main() -> None:
    """Print the per-sheet and total count of ``p`` for each Excel file in ``resources/``."""
    excel_files = find_excel_files(RESOURCES_DIR)
    if not excel_files:
        print(f"No Excel files found in {RESOURCES_DIR}")
        return

    for excel_path in excel_files:
        try:
            counts = count_file(excel_path)
        except (ValueError, OSError) as error:
            print(f"Skipped {excel_path.name}: {error}")
            continue
        for sheet, count in counts.items():
            print(f"{excel_path.name} [{sheet}]: {count}")
        print(f"{excel_path.name} total '{LETTER}': {sum(counts.values())}")


if __name__ == "__main__":
    main()
