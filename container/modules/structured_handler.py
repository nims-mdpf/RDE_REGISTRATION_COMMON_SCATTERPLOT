from __future__ import annotations

from pathlib import Path

import pandas as pd

from modules.interfaces import IStructuredDataProcessor


class StructuredDataProcessor(IStructuredDataProcessor):
    """Class for handling header and data information.

    This class saves the header information and data part of the input file into separate files.
    Both the header information and measurement data are saved as CSV files.

    """

    def to_text(self, metadata: list[tuple[str, str]], save_path: Path) -> None:
        """Write the metadata to a text file.

        Args:
            metadata (list[tuple[str, str]]): The metadata to be written.
            save_path (Path): The path to save the text file.

        Returns:
            None

        """
        with open(save_path, "w") as f:
            for key, value in metadata:
                f.write(f"{key},{value}\n")

    def to_csv(self, dataframe: pd.DataFrame, save_path: Path, *, header: list[str] | None = None) -> None:
        """Save the given DataFrame to a CSV file.

        Args:
            dataframe (pd.DataFrame): The DataFrame to be saved.
            save_path (Path): The path where the CSV file will be saved.
            header (Optional[list[str]], optional): The list of column names to be used as the header in the CSV file. Defaults to None.

        Returns:
            None

        """
        if header is not None:
            if self.has_explicit_column_headers(dataframe):
                dataframe.to_csv(save_path, index=False)
            else:
                dataframe.to_csv(save_path, header=header, index=False)
        else:
            dataframe.to_csv(save_path, index=False)

    def has_explicit_column_headers(self, df: pd.DataFrame) -> bool:
        """Check if the DataFrame has explicit column headers.

        Args:
            df (pd.DataFrame): The DataFrame to check.

        Returns:
            bool: True if the DataFrame has explicit column headers, False otherwise.

        """
        return not all(isinstance(col, int) for col in df.columns)
