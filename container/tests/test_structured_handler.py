import os
import pathlib

import pandas as pd

from modules.structured_handler import StructuredDataProcessor


def test_to_csv():
    handler = StructuredDataProcessor()
    data = [[1, 2], [3, 4], [5, 6]]
    df = pd.DataFrame(data)
    handler.to_csv(df, pathlib.Path("data.csv"))

    assert os.path.exists("data.csv")

    with open("data.csv", mode="r", encoding="utf-8") as f:
        contents = f.read()

    print(df)

    assert contents == "0,1\n1,2\n3,4\n5,6\n"

    if os.path.exists("data.csv"):
        os.remove("data.csv")


def test_to_text():
    handler = StructuredDataProcessor()
    metadata = [("key1", "value1"), ("key2", "value2"), ("key3", "value3")]
    handler.to_text(metadata, pathlib.Path("metadata.txt"))

    assert os.path.exists("metadata.txt")

    with open("metadata.txt", mode="r", encoding="utf-8") as f:
        contents = f.read()

    assert contents == "key1,value1\nkey2,value2\nkey3,value3\n"

    if os.path.exists("metadata.txt"):
        os.remove("metadata.txt")
