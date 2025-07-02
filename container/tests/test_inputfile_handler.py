import os
from pathlib import Path
from unittest.mock import patch
import pandas as pd
import pytest

from rdetoolkit.exceptions import StructuredError

from modules.inputfile_handler import HeaderParser, MeasurementParser, FileOperator, DataParser, FileReader, detect_separator


@pytest.fixture
def test_inputfile():
    test_file = Path("testinput1.txt")
    test_content = [
        "Hello World\n",
        "This is a test file.\n",
        "Python is awesome.\n",
        "Goodbye!\n",
        "[Data]",
        "1000 0.01",
        "2000 0.02",
    ]
    with open(str(test_file), "w") as f:
        f.writelines(test_content)
    yield test_file

    if test_file.exists():
        test_file.unlink()


@pytest.mark.parametrize(
    "line, expected",
    [
        ("", True),
        ("#", True),
        ("!", True),
        (";", True),
        ("    ", True),
        ("# comment", True),
        ("! comment", True),
        ("; comment", True),
        ("    comment", False),
        ("not comment", False),
        ("# comment\n", True),
        ("! comment\n", True),
        ("; comment\n", True),
        ("    comment\n", False),
        ("not comment\n", False),
    ],
)
def test_headerparse_is_comment_or_empty(line, expected):
    header_parser = HeaderParser()
    assert header_parser._HeaderParser__is_comment_or_empty(line) == expected


@pytest.mark.parametrize(
    "line, split_char, expected",
    [
        ("[Data]", ",", True),
        ("{DATA}", ",", True),
        ("(data)", ",", True),
        ("data", ",", False),
        ("[Measurement]", ",", True),
        ("{measurement}", ",", True),
        ("(measurement)", ",", True),
        ("mesure", ",", False),
        ("[計測]", ",", False),
        ("{データセクション}", ",", False),
        ("(データセクション)", ",", False),
        ("dataset", ",", False),
        ("***DATA***", ",", False),
        ("---data---", ",", False),
        ("~~~Data~~~", ",", False),
        ("[]", ",", False),
        ("{}", ",", False),
        ("()", ",", False),
        ("Sample", ",", False),
        ("Frame", ",", False),
        (";", ",", False),
        # ("time;data", True),
        # ("Volume, Sample", True),
        ("1000 0.01", ",", True),
    ],
)
def test_headerparse_is_mesurement_start(line, split_char, expected):
    header_parser = HeaderParser()
    header_parser.sep = split_char
    assert header_parser.is_mesurement_start(line) == expected


@pytest.mark.parametrize("lines, separators, expected", [
    ([
        "name,age,city",
        "Alice,30,New York",
        "Bob,25,Los Angeles"
    ], [",", ";", "\t"], ","),

    ([
        "name\tage\tcity",
        "Alice\t30\tNew York",
        "Bob\t25\tLos Angeles"
    ], [",", ";", "\t"], "\t"),

    ([
        "name;age;city",
        "Alice;30;New York",
        "Bob;25;Los Angeles"
    ], [",", ";", "\t"], ";"),

    ([
        "name age city",
        "Alice 30 New York",
        "Bob 25 Los Angeles"
    ], [",", ";", "\t"], None),

    ([
        "",
        "   ",
        "\t\t\t"
    ], [",", ";", "\t"], None),

    ([
        "name,age;city",
        "Alice,30;New York",
        "Bob,25;Los Angeles"
    ], [",", ";", "\t"], ","),

    (["name,age,city"] * 1001, [",", ";", "\t"], ",")
])
def test_detect_separator(lines, separators, expected):
    assert detect_separator(lines, separators) == expected


@pytest.mark.parametrize(
    "line, expected, separator",
    [
        ("date: 2021-01-01", ("date", "2021-01-01"), ":"),
        ("model: 1234", ("model", "1234"), ":"),
        ("media : jpeg,png,bmp", ("media", "jpeg,png,bmp"), ":"),
        ("file|/path/to/file", ("file", "/path/to/file"), "|"),
        ("version | 10.branch.1", ("version", "10.branch.1"), "|"),
        ("cycle\t100", ("cycle", "100"), "\t"),
        ("voltage \t 100 200 300 400", ("voltage", "100 200 300 400"), "\t"),
        ("location;Tokyo", ("location", "Tokyo"), ";"),
        ("location; Tokyo, Kyoto", ("location", "Tokyo, Kyoto"), ";"),
        ("location ; Tokyo, Kyoto", ("location", "Tokyo, Kyoto"), ";"),
        ("location ;Tokyo, Kyoto, Osaka", ("location", "Tokyo, Kyoto, Osaka"), ";"),
        ("name ;Hans, Anna, Marco, Alexei, Ivan", ("name", "Hans, Anna, Marco, Alexei, Ivan"), ";"),
    ],
)
def test_header_parser_split_key_value(line, expected, separator):
    header_parser = HeaderParser()
    # Mock: header_parser.sep
    with patch.object(header_parser, "sep", separator):
        key, value = header_parser.split_key_value(line)
        assert (key, value) == expected


@patch('modules.inputfile_handler.detect_separator', return_value=':')
def test_header_parser_parse(mock_detect_separator):
    header_parser = HeaderParser()
    data = [
        "# comment",
        "date: 2021-01-01",
        "model: 1234",
        "media : jpeg,png,bmp",
        "file|1 : /path/to/file",
        "version|2: 10.branch.1",
        "cycle\tvalue : 100",
        "voltage\tvalue: 100 200 300 400",
        "location:Tokyo",
        "location: Tokyo, Kyoto",
        "location : Tokyo, Kyoto",
        "location :Tokyo, Kyoto, Osaka",
        "name :Hans, Anna, Marco, Alexei, Ivan",
        "[data]",
        "1000 0.01",

    ]
    header = header_parser.parse(data)
    assert header == [
        ("date", "2021-01-01"),
        ("model", "1234"),
        ("media", "jpeg,png,bmp"),
        ("file|1", "/path/to/file"),
        ("version|2", "10.branch.1"),
        ("cycle\tvalue", "100"),
        ("voltage\tvalue", "100 200 300 400"),
        ("location", "Tokyo"),
        ("location", "Tokyo, Kyoto"),
        ("location", "Tokyo, Kyoto"),
        ("location", "Tokyo, Kyoto, Osaka"),
        ("name", "Hans, Anna, Marco, Alexei, Ivan"),
    ]
    assert header_parser.end_line == 13
    assert header_parser.sep == ":"


def test_mesurements_parser_parse():
    mesurement_parser = MeasurementParser()
    data = [
        "# comment",
        "date: 2021-01-01",
        "model: 1234",
        "media : jpeg,png,bmp",
        "file|1 : /path/to/file",
        "version|2: 10.branch.1",
        "cycle\tvalue : 100",
        "voltage\tvalue: 100 200 300 400",
        "location:Tokyo",
        "location: Tokyo, Kyoto",
        "location : Tokyo, Kyoto",
        "location :Tokyo, Kyoto, Osaka",
        "name :Hans, Anna, Marco, Alexei, Ivan",
        "data",
        "1000 0.01",
        "2000 0.02",
        "3000 0.03",
        "4000 0.04",
        "5000 0.05",
    ]
    df = mesurement_parser.parse(data, 14)
    print(df.shape)
    assert df.shape == (5, 2)
    assert df.loc[0].to_list() == [1000, 0.01]
    assert df.loc[1].to_list() == [2000, 0.02]
    assert df.loc[2].to_list() == [3000, 0.03]
    assert df.loc[3].to_list() == [4000, 0.04]
    assert df.loc[4].to_list() == [5000, 0.05]


# @pytest.mark.parametrize(
#     "line, expected",
#     [
#         ("1000 0.01", " "),
#         ("1000:0.01", ":"),
#         ("1000\t0.01", "\t"),
#         ("1000|0.01", "|"),
#         ("1000;0.01", ";"),
#         ("1000,0.01", ","),
#         ("1000  0.01", " "),
#         ("1000 :0.01", ":"),
#         ("1000 \t0.01", "\t"),
#         ("1000| 0.01", "|"),
#         ("1000; 0.01", ";"),
#         ("1000 ,0.01", ","),
#     ],
# )
# def test_mesurement_parser_detect_separator(line, expected):
#     mesurement_parser = MeasurementParser()
#     sep = mesurement_parser.detect_separator_with_single_line(line)
#     assert sep == expected


@pytest.mark.parametrize(
    "line, sep, expected",
    [
        ("1000 0.01", " ", [1000, 0.01]),
        ("1000 :0.01", ":", [1000, 0.01]),
        ("1000|0.01", "|", [1000, 0.01]),
        ("1000,0.01", ",", [1000, 0.01]),
        ("1000;0.01", ";", [1000, 0.01]),
        ("1000:0.01", ":", [1000, 0.01]),
    ],
)
def test_mesurement_parser_split_data_line(line, sep, expected):
    mesurement_parser = MeasurementParser()
    mesurement_parser.sep = sep
    parts = mesurement_parser.split_data_line(line)
    assert parts == expected


@pytest.mark.parametrize(
    "line, sep",
    [
        ("", " "),
    ],
)
def test_invalid_format_mesurement_parser_split_data_line(line, sep):
    parser = MeasurementParser()
    parser.sep = sep

    with pytest.raises(StructuredError) as excinfo:
        parser.split_data_line(line)

    assert excinfo.value.emsg == "Invalid data line format. Please check the format of the measurement data."
    assert excinfo.value.ecode == 1


@pytest.fixture
def inputdata_file():
    data = [
        "# comment",
        "date: 2021-01-01",
        "model: 1234",
        "media : jpeg,png,bmp",
        "file|1 : /path/to/file",
        "version|2: 10.branch.1",
        "cycle\tvalue : 100",
        "voltage\tvalue: 100 200 300 400",
        "location:Tokyo",
        "location: Tokyo, Kyoto",
        "location : Tokyo, Kyoto",
        "location :Tokyo, Kyoto, Osaka",
        "name :Hans, Anna, Marco, Alexei, Ivan",
        "[data]",
        "1000 0.01",
        "2000 0.02",
        "3000 0.03",
        "4000 0.04",
        "5000 0.05",
    ]

    file_path = "tests/test_inputdata.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(data))

    yield file_path

    if os.path.exists(file_path):
        os.remove(file_path)


def test_file_operator(inputdata_file):
    expected = [
        "# comment",
        "date: 2021-01-01",
        "model: 1234",
        "media : jpeg,png,bmp",
        "file|1 : /path/to/file",
        "version|2: 10.branch.1",
        "cycle\tvalue : 100",
        "voltage\tvalue: 100 200 300 400",
        "location:Tokyo",
        "location: Tokyo, Kyoto",
        "location : Tokyo, Kyoto",
        "location :Tokyo, Kyoto, Osaka",
        "name :Hans, Anna, Marco, Alexei, Ivan",
        "[data]",
        "1000 0.01",
        "2000 0.02",
        "3000 0.03",
        "4000 0.04",
        "5000 0.05",
    ]
    operator = FileOperator(inputdata_file)

    assert operator.read() == expected


def test_data_parser(inputdata_file):
    operator = FileOperator(inputdata_file)
    header_parser = HeaderParser()
    measurement_parser = MeasurementParser()
    parser = DataParser(operator, header_parser, measurement_parser)
    parser.process()

    metadata = parser.get_metadata()
    mesurements = parser.get_measurements()

    assert isinstance(metadata, list)
    assert isinstance(mesurements, pd.DataFrame)

    assert metadata == [
        ("date", "2021-01-01"),
        ("model", "1234"),
        ("media", "jpeg,png,bmp"),
        ("file|1", "/path/to/file"),
        ("version|2", "10.branch.1"),
        ("cycle\tvalue", "100"),
        ("voltage\tvalue", "100 200 300 400"),
        ("location", "Tokyo"),
        ("location", "Tokyo, Kyoto"),
        ("location", "Tokyo, Kyoto"),
        ("location", "Tokyo, Kyoto, Osaka"),
        ("name", "Hans, Anna, Marco, Alexei, Ivan"),
    ]

    expected_df = pd.DataFrame(
        [
            [1000, 0.01],
            [2000, 0.02],
            [3000, 0.03],
            [4000, 0.04],
            [5000, 0.05],
        ]
    )

    assert mesurements.equals(expected_df)


def test_file_reader(inputdata_file):
    expected_metadata = [
        ("date", "2021-01-01"),
        ("model", "1234"),
        ("media", "jpeg,png,bmp"),
        ("file|1", "/path/to/file"),
        ("version|2", "10.branch.1"),
        ("cycle\tvalue", "100"),
        ("voltage\tvalue", "100 200 300 400"),
        ("location", "Tokyo"),
        ("location", "Tokyo, Kyoto"),
        ("location", "Tokyo, Kyoto"),
        ("location", "Tokyo, Kyoto, Osaka"),
        ("name", "Hans, Anna, Marco, Alexei, Ivan"),
    ]

    expected_df = pd.DataFrame(
        [
            [1000, 0.01],
            [2000, 0.02],
            [3000, 0.03],
            [4000, 0.04],
            [5000, 0.05],
        ]
    )
    file_reader = FileReader()
    metadata, mesurements = file_reader.read(inputdata_file)

    assert expected_df.equals(mesurements)
    assert expected_metadata == metadata


def test_set_mesurement_start_number(test_inputfile, ivnoice_json_with_sample_info):
    file_reader = FileReader()
    file_reader.set_mesurement_start_number(test_inputfile, ivnoice_json_with_sample_info)
    assert file_reader.user_mesurement_start_number == 5


def test_raise_filenotfound_error_set_mesurement_start_number(test_inputfile, ivnoice_json_with_sample_info):
    file_reader = FileReader()
    with pytest.raises(FileNotFoundError) as e:
        file_reader.set_mesurement_start_number(Path("notfound.txt"), ivnoice_json_with_sample_info)
    assert file_reader.user_mesurement_start_number is None
    assert str(e.value) == "File not found: notfound.txt"
