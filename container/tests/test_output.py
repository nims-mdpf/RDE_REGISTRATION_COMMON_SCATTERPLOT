import os
import shutil
from typing import Union

import pytest


def setup_inputdata_folder(inputdata_name: Union[str, list[str]]):
    """テスト用でdataフォルダ群の作成とrawファイルの準備

    Args:
        inputdata_name (Union[str, list[str]]): rawファイル名
    """
    destination_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(destination_path, exist_ok=True)
    os.makedirs(os.path.join(destination_path, "inputdata"), exist_ok=True)
    os.makedirs(os.path.join(destination_path, "invoice"), exist_ok=True)
    inputdata_original_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputdata")

    tasksupport_original_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "templates",
        "template",
        "tasksupport",
    )

    if isinstance(inputdata_name, list):
        for item in inputdata_name:
            shutil.copy(
                os.path.join(inputdata_original_path, item),
                os.path.join(destination_path, "inputdata"),
            )
    else:
        shutil.copy(
            os.path.join(inputdata_original_path, inputdata_name),
            os.path.join(destination_path, "inputdata"),
        )
    if not os.path.exists(os.path.join(destination_path, "tasksupport")):
        shutil.copytree(tasksupport_original_path, os.path.join(destination_path, "tasksupport"))


def setup_invoice_file(path: str):
    """テスト用でinvoiceファイルの準備

    Args:
        path (Union[str, list[str]]): rawファイル名
    """
    destination_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(destination_path, exist_ok=True)
    os.makedirs(os.path.join(destination_path, "invoice"), exist_ok=True)
    inputdata_original_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputdata")

    shutil.copy(
        os.path.join(inputdata_original_path, path),
        os.path.join(destination_path, "invoice"),
    )


def setup_file(dirname: str, path: str):
    """テスト用でinvoiceファイルの準備

    Args:
        path (Union[str, list[str]]): rawファイル名
    """
    destination_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(destination_path, exist_ok=True)
    os.makedirs(os.path.join(destination_path, dirname), exist_ok=True)
    inputdata_original_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputdata")

    shutil.copy(
        os.path.join(inputdata_original_path, path),
        os.path.join(destination_path, dirname),
    )


class TestOutputCase1:
    """case1
    pattern1の入出力テスト
    入力ファイル: pattern1/inputdata/sample-data.txtを参照
    """

    inputdata: Union[str, list[str]] = "pattern1/inputdata/sample-data.txt"
    invoice: str = "pattern1/invoice/invoice.json"

    def test_setup(self):
        setup_inputdata_folder(self.inputdata)
        setup_invoice_file(self.invoice)

    @pytest.mark.parametrize("raw_data", ["sample-data.txt"])
    def test_raw_data(self, setup_main, data_path, raw_data):
        assert os.path.exists(os.path.join(data_path, "raw", raw_data))

    @pytest.mark.parametrize("img_name", ["sample-data.png"])
    def test_main_image(self, data_path, img_name):
        assert os.path.exists(os.path.join(data_path, "main_image", img_name))

    @pytest.mark.parametrize("csv_name", ["data.csv", "header.csv"])
    def test_structured(self, data_path, csv_name):
        assert os.path.exists(os.path.join(data_path, "structured", csv_name))

    def test_thumbnail(self, data_path):
        assert os.path.exists(os.path.join(data_path, "thumbnail", "sample-data.png"))

    def test_metadata(self, data_path):
        assert os.path.exists(os.path.join(data_path, "meta", "metadata.json"))


class TestOutputCase3:
    """case3
    pattern3の入出力テスト
    入力ファイル: pattern3/inputdata/sample-data.txtを参照
    """

    inputdata: Union[str, list[str]] = "pattern3/inputdata/sample-data.txt"
    invoice: str = "pattern3/invoice/invoice.json"

    def test_setup(self):
        setup_inputdata_folder(self.inputdata)
        setup_invoice_file(self.invoice)

    @pytest.mark.parametrize("raw_data", ["sample-data.txt"])
    def test_raw_data(self, setup_main, data_path, raw_data):
        assert os.path.exists(os.path.join(data_path, "raw", raw_data))

    @pytest.mark.parametrize("img_name", ["sample-data.png"])
    def test_main_image(self, data_path, img_name):
        assert os.path.exists(os.path.join(data_path, "main_image", img_name))

    @pytest.mark.parametrize("csv_name", ["data.csv", "header.csv"])
    def test_structured(self, data_path, csv_name):
        assert os.path.exists(os.path.join(data_path, "structured", csv_name))

    def test_thumbnail(self, data_path):
        assert os.path.exists(os.path.join(data_path, "thumbnail", "sample-data.png"))

    def test_metadata(self, data_path):
        assert os.path.exists(os.path.join(data_path, "meta", "metadata.json"))


class TestOutputCase4:
    """case4
    pattern4の入出力テスト
    入力ファイル: pattern4/inputdata/sample-data.txtを参照
    """

    inputdata: Union[str, list[str]] = "pattern4/inputdata/sample-data.txt"
    invoice: str = "pattern4/invoice/invoice.json"

    def test_setup(self):
        setup_inputdata_folder(self.inputdata)
        setup_invoice_file(self.invoice)

    @pytest.mark.parametrize("raw_data", ["sample-data.txt"])
    def test_raw_data(self, setup_main, data_path, raw_data):
        assert os.path.exists(os.path.join(data_path, "raw", raw_data))

    @pytest.mark.parametrize("img_name", ["sample-data.png"])
    def test_main_image(self, data_path, img_name):
        assert os.path.exists(os.path.join(data_path, "main_image", img_name))

    @pytest.mark.parametrize("csv_name", ["data.csv", "header.csv"])
    def test_structured(self, data_path, csv_name):
        assert os.path.exists(os.path.join(data_path, "structured", csv_name))

    def test_thumbnail(self, data_path):
        assert os.path.exists(os.path.join(data_path, "thumbnail", "sample-data.png"))

    def test_metadata(self, data_path):
        assert os.path.exists(os.path.join(data_path, "meta", "metadata.json"))


class TestOutputCase5:
    """case5
    pattern5の入出力テスト
    入力ファイル: pattern5/inputdata/sample-data.txtを参照
    """

    inputdata: Union[str, list[str]] = "pattern5/inputdata/sample-data.txt"
    invoice: str = "pattern5/invoice/invoice.json"

    def test_setup(self):
        setup_inputdata_folder(self.inputdata)
        setup_invoice_file(self.invoice)

    @pytest.mark.parametrize("raw_data", ["sample-data.txt"])
    def test_raw_data(self, setup_main, data_path, raw_data):
        assert os.path.exists(os.path.join(data_path, "raw", raw_data))

    @pytest.mark.parametrize("img_name", ["sample-data.png"])
    def test_main_image(self, data_path, img_name):
        assert os.path.exists(os.path.join(data_path, "main_image", img_name))

    @pytest.mark.parametrize("csv_name", ["data.csv", "header.csv"])
    def test_structured(self, data_path, csv_name):
        assert os.path.exists(os.path.join(data_path, "structured", csv_name))

    def test_thumbnail(self, data_path):
        assert os.path.exists(os.path.join(data_path, "thumbnail", "sample-data.png"))

    def test_metadata(self, data_path):
        assert os.path.exists(os.path.join(data_path, "meta", "metadata.json"))
