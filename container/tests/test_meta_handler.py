import json
import os
import pathlib

import pytest

from modules.meta_handler import MetaParser
from rdetoolkit.rde2util import Meta


@pytest.fixture
def sample_data():
    """サンプルの入力データを提供。"""
    return [
        ("name", "Test Name"),
        ("version", "1.0"),
        ("description", "A sample metadata parser.")
    ]


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


@pytest.fixture
def sample_metadata_def(tmp_path):
    """サンプルの metadata-def.json の内容を提供し、一時ファイルに保存。"""
    metadata_def = {
        "name_key": {
            "name": {
                "ja": "",
                "en": "Comments"
            },
            "originalName": "name",
            "schema": {"type": "string"}
        },
        "version_key": {
            "name": {
                "ja": "",
                "en": "Comments"
            },
            "originalName": "version",
            "schema": {"type": "string"}
        },
        "description_key": {
            "name": {
                "ja": "",
                "en": "Comments"
            },
            "originalName": "description",
            "schema": {"type": "string"}
        }
    }
    metadata_def_path = tmp_path / "metadata-def.json"
    with open(metadata_def_path, mode="w", encoding="utf-8") as f:
        json.dump(metadata_def, f)
    return metadata_def_path


@pytest.fixture
def sample_meta(sample_metadata_def):
    return Meta(sample_metadata_def)


def test_parse_with_valid_data(sample_data, sample_metadata_def):
    handler = MetaParser()
    const_meta_info, repeated_meta_info = handler.parse(sample_data, sample_metadata_def)

    assert const_meta_info == {
        "name_key": "Test Name",
        "version_key": "1.0",
        "description_key": "A sample metadata parser."
    }
    assert repeated_meta_info is None


def test_parse_with_invalid_data(sample_metadata_def):
    handler = MetaParser()
    invalid_data = [("invalid_key", "value")]
    const_meta_info, repeated_meta_info = handler.parse(invalid_data, sample_metadata_def)

    assert const_meta_info == {}
    assert repeated_meta_info is None


def test_save_meta_success(temp_dir, sample_meta):
    handler = MetaParser()
    save_path = temp_dir / "metadata.json"
    const_meta_info = {"name_key": "Test Name", "version_key": "1.0", "description_key": "A sample metadata parser."}

    _ = handler.save_meta(save_path, sample_meta, const_meta_info=const_meta_info)

    assert os.path.exists(save_path)
    with open(save_path, "r", encoding="utf-8") as f:
        contents = json.load(f)
    assert contents == {"constant": {'name_key': {'value': 'Test Name'}, 'version_key': {'value': '1.0'}, 'description_key': {'value': 'A sample metadata parser.'}}, "variable": []}


def test_save_meta_with_repeated_meta_info(temp_dir, sample_meta):
    handler = MetaParser()
    save_path = temp_dir / "metadata.json"
    const_meta_info = {"name_key": "Test Name", "version_key": "1.0", "description_key": "A sample metadata parser."}
    repeated_meta_info = {"some_key": "some_value"}

    with pytest.raises(NotImplementedError, match="Repeated meta info is not supported in this template"):
        handler.save_meta(save_path, sample_meta, const_meta_info=const_meta_info, repeated_meta_info=repeated_meta_info)
