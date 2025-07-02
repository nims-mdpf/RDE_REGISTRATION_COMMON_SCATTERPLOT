from __future__ import annotations

import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Sequence

import pandas as pd
from rdetoolkit.exceptions import StructuredError
from rdetoolkit.rde2util import CharDecEncoding, read_from_json_file


class FileOperator:

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def read(self) -> list[str]:
        """Read the content of a text file and return it as a list of strings, with each string representing a line from the file.

        Returns:
            list[str]: A list of strings, each representing a line from the file.

        """
        enc = CharDecEncoding.detect_text_file_encoding(self.file_path)
        with open(self.file_path, encoding=enc) as f:
            return [line.rstrip("\r\n") for line in f.readlines()]


def detect_separator(lines: list[str], separators: Sequence[str]) -> str | None:
    """Detect the separator used in the given lines.

    Args:
        lines (list[str]): The lines to check for the separator.
        separators (Sequence[str]): A sequence of possible separators to detect.

    Returns:
        str | None: The detected separator or None if no separator is found.

    """
    max_lines: int = 1000
    delimiter_field_counts: dict[str, list[int]] = {s: [] for s in separators}
    for line in lines[:max_lines]:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        for s in separators:
            fields = line.split(s)
            if len(fields) > 1:
                delimiter_field_counts[s].append(len(fields))

    delimiter_scores: dict[str, float] = {}
    for d, counts in delimiter_field_counts.items():
        if not counts:
            continue
        try:
            field_counts_counter = Counter(counts)
            _, mode_count = field_counts_counter.most_common(1)[0]
            delimiter_scores[d] = mode_count
        except statistics.StatisticsError:
            delimiter_scores[d] = float('inf')
            continue

    return max(delimiter_scores, key=lambda k: delimiter_scores[k]) if delimiter_scores else None


class HeaderParser:

    separators: tuple[str, ...] = ("\t", "|", ":", ";", ",")

    def __init__(self, user_mesurement_start_number: int | None = None):
        self.header: list[tuple[str, str]] = []
        self.end_line: int = 0
        self.sep: str | None = None
        self.user_mesurement_start_number = user_mesurement_start_number

    def parse(self, data: list[str]) -> list[tuple[str, str]]:
        """Parse the given data and return a list of tuples representing the header.

        Args:
            data (list[str]): A list of strings representing the data to be parsed.

        Returns:
            list[tuple[str, str]]: A list of tuples, where each tuple contains a key-value pair from the header.

        """
        _delimi = detect_separator(data, self.separators)
        self.sep = _delimi if _delimi else ","
        for i, line in enumerate(data):
            if self.__is_comment_or_empty(line):
                continue
            if self.is_mesurement_start(line) or (self.user_mesurement_start_number and i == self.user_mesurement_start_number):
                self.end_line = i
                break
            if self.__is_header_char(line):
                continue
            self.header.append(self.split_key_value(line))
        return self.header

    def split_key_value(self, line: str) -> tuple[str, str]:
        """Split a line into key and value using a separator.

        Args:
            line (str): The line to be split.

        Returns:
            tuple[str, str]: A tuple containing the key and value.

        Example:
            >>> parser = HeaderParser()
            >>> parser.split_key_value("name: John Doe")
            ('name', 'John Doe')

        """
        key, value = line.split(self.sep, 1)
        return key.strip(), value.strip()

    def __is_header_char(self, line: str) -> re.Match[str] | None:
        return re.search(r"[\[\(\{].*?[\]\)\}]|header", line, re.IGNORECASE)

    def __is_comment_or_empty(self, line: str) -> bool:
        return line.startswith(("#", "!", ";")) or not line.strip()

    def is_mesurement_start(self, line: str) -> bool:
        """Determine if a given line is the start of a measurement.

        Args:
            line (str): The line to check for the start of a measurement.

        Returns:
            bool: True if the line is the start of a measurement, False otherwise.

        """
        split_len = len(line.split(self.sep)) if self.sep else 0
        return (
            split_len == 1 and bool(re.match(r"[\[({]\s*(data|measurement)\s*[\])}]", line, re.IGNORECASE))
        ) or self.__is_numeric_line(line)

    def __is_numeric_line(self, line: str) -> bool:
        tokens = re.split(r"[,\s;]+", line.strip())
        return all(token.replace(".", "", 1).isdigit() for token in tokens)


class MeasurementParser:
    # The array is ordered by priority to ensure that non-space separators
    # (|, \t, ;, :, ,, ) are detected first. This is done to prioritize these
    # separators over spaces when they coexist in the same line.
    separators: tuple[str, ...] = ("\t", "|", ",", ";", ":", " ")
    MIN_PARTS_COUNT = 2

    def __init__(self) -> None:
        self.mesurements: pd.DataFrame = pd.DataFrame()
        self.sep: str = " "

    def parse(self, lines: list[str], start_line: int) -> pd.DataFrame:
        """Parse the input lines starting from the specified line number.

        Args:
            lines (list[str]): The list of input lines to be parsed.
            start_line (int): The line number from which to start parsing.

        Returns:
            dict: A dictionary containing the parsed data.

        """
        data: list[list[int | float]] = []
        data_header: list[str] = []

        _delimi = detect_separator(lines[start_line:], self.separators)
        self.sep = _delimi if _delimi else ","
        for idx, line in enumerate(lines[start_line:], start=start_line):
            if self.__is_comment_or_empty(line):
                continue
            if self.__is_header_char(line):
                continue
            if idx == start_line and self.is_comma_separated_alpha_strings(line):
                data_header = line.split(',')

            parsed_line = self.split_data_line(line)
            if parsed_line:
                data.append(parsed_line)
        self.mesurements = pd.DataFrame(data)
        if data_header:
            self.mesurements.columns = pd.Index(data_header)
        return self.mesurements

    def is_comma_separated_alpha_strings(self, s: str) -> bool:
        """Check if a given string is a comma-separated list of alphabetic strings.

        Args:
            s (str): The input string to check.

        Returns:
            bool: True if the string is a comma-separated list of alphabetic strings, False otherwise.

        """
        parts = s.split(',')
        if len(parts) < self.MIN_PARTS_COUNT:
            return False
        pattern = re.compile(r'^[A-Za-z]+$')
        for part in parts:
            _part = part.strip()
            if not _part or not pattern.match(_part):
                return False
        return True

    def split_data_line(self, line: str) -> list[int | float] | None:
        """Split a data line into parts.

        Args:
            line (str): The data line to be split.

        Returns:
            list[str]: A list of parts after splitting the data line.

        Raises:
            StructuredError: If the data line format is invalid.

        """
        parts = [part.strip() for part in line.split(self.sep)]
        if len(parts) <= 1:
            error_message = "Invalid data line format. Please check the format of the measurement data."
            raise StructuredError(error_message, 1)
        return [self.__convert_to_number(part) for part in parts if self.__is_numeric_char(part)]

    def __is_numeric_char(self, char: str) -> re.Match[str] | None:
        return re.fullmatch(r"\d+(\.\d+)?", char)

    def __is_header_char(self, line: str) -> re.Match[str] | None:
        return re.search(r"[\[\(\{].*?[\]\)\}]", line)

    def __is_comment_or_empty(self, line: str) -> bool:
        return line.startswith(("#", ";", "!")) or not line.strip()

    def __convert_to_number(self, part: str) -> int | float:
        try:
            return int(part)
        except ValueError:
            try:
                return float(part)
            except ValueError as e:
                raise StructuredError(emsg="Invalid data format", ecode=1) from e


class DataParser:
    def __init__(self, file_operator: FileOperator, header_parser: HeaderParser, measurement_parser: MeasurementParser):
        self.file_operator = file_operator
        self.header_parser = header_parser
        self.measurement_parser = measurement_parser
        self.header: list[tuple[str, str]] = []
        self.measurements: pd.DataFrame = pd.DataFrame()

    def process(self) -> tuple[list[tuple[str, str]], pd.DataFrame]:
        """Process the file and return the header and measurements.

        Returns:
            A tuple containing the header and measurements.
            - The header is a list of tuples, where each tuple contains two strings representing the column name and data type.
            - The measurements is a pandas DataFrame containing the parsed data.

        """
        lines = self.file_operator.read()
        self.header = self.header_parser.parse(lines)
        self.measurements = self.measurement_parser.parse(lines, self.header_parser.end_line + 1)
        return self.header, self.measurements

    def get_metadata(self) -> list[tuple[str, str]]:
        """Return the metadata of the input file.

        Returns:
            list[tuple[str, str]]: A list of tuples representing the metadata.

        """
        return self.header

    def get_measurements(self) -> pd.DataFrame:
        """Return the measurements stored in the input file.

        Returns:
            pd.DataFrame: The measurements stored in the input file.

        """
        return self.measurements


class FileReader:
    """Class for reading and parsing files.

    This class reads a text file from the specified file path and returns its content as a list of strings.

    Args:
        file_path (Path): The path to the file to be read.

    Methods:
        read() -> list[str]: Reads the file and returns its content as a list of strings.

    Example:
        file_reader = FileReader(Path('file1.txt'))
        loaded_data = file_reader.read()

    """

    user_mesurement_start_number: int | None = None

    def read(self, file_path: Path) -> tuple[list[tuple[str, str]], pd.DataFrame]:
        """Read the file at the given file path and process its contents.

        This method initializes the file reader, metadata parser, measurement parser,
        and data parser. It then processes the file and retrieves the metadata and
        measurements.

        Args:
            file_path (Path): The path to the file to be read.

        Returns:
            tuple: A tuple containing the metadata and measurements extracted from the file.

        """
        self.file_reader = FileOperator(file_path)
        self.metadata_parser = HeaderParser(user_mesurement_start_number=self.user_mesurement_start_number)
        self.measurement_parser = MeasurementParser()
        self.data_parser = DataParser(self.file_reader, self.metadata_parser, self.measurement_parser)
        self.data_parser.process()
        metadata = self.data_parser.get_metadata()
        measurements = self.data_parser.get_measurements()
        return metadata, measurements

    def set_mesurement_start_number(self, input_file_path: Path, invoice_json: Path) -> int | None:
        """Set the measurement start number from the provided JSON file.

        This method reads a JSON file specified by the `invoice_json` path, extracts the
        "measurement_data_start_line_number" from the "custom" section, and sets it to
        `self.user_mesurement_start_number`. If the number is not found, it sets
        `self.user_mesurement_start_number` to None.

        Args:
            input_file_path (Path): The path to the input file.
            invoice_json (Path): The path to the JSON file containing the invoice data.

        Returns:
            int | None: The measurement start number as a string, or None if not found.

        """
        if not input_file_path.exists():
            emsg = f"File not found: {input_file_path}"
            raise FileNotFoundError(emsg)

        contents = read_from_json_file(invoice_json)
        mesurement_start_char = contents.get("custom", {}).get("measurement_data_start_character", None)
        number = self.__find_line_number_with_target_char(str(input_file_path), mesurement_start_char) if mesurement_start_char else None
        self.user_mesurement_start_number = int(number) if number is not None else None
        return self.user_mesurement_start_number

    def __find_line_number_with_target_char(self, path: str, search_char: str) -> int | None:
        """Retrieve the line number of the first occurrence of the specified string in a text file.

        Args:
            path (str): The path to the text file.
            search_char (str): The character to search for.

        Returns:
            int: The line number (1-based) where the search string is first found.
                Returns -1 if the string is not found.

        """
        enc = CharDecEncoding.detect_text_file_encoding(path)
        with open(path, encoding=enc) as f:
            for idx, line in enumerate(f, start=1):
                if search_char in line:
                    return idx
            return None
