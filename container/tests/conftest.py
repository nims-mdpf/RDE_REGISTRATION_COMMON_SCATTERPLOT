import json
import os
import shutil
from subprocess import PIPE, run

import pytest

pytest_plugins = ("tests.fixtures.template_files",)


@pytest.fixture
def data_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


@pytest.fixture(scope="class")
def setup_main():
    """main.pyを実行するフィクスチャ
    Note:
        scope='module': テストクラスごとに１度だけ実行される
    """
    # setup: テスト準備処理
    basepath_main_script = os.path.dirname(os.path.dirname(__file__))
    if os.name == "nt":
        # windows command
        cmd = ["python", os.path.join(basepath_main_script, "main.py")]
    else:
        # mac / unix command
        pyenv_version = os.getenv("PYENV_VERSION")
        if pyenv_version is not None:
            cmd = ["python", os.path.join(basepath_main_script, "main.py")]
        else:
            cmd = ["python3", os.path.join(basepath_main_script, "main.py")]
    rtn = run(cmd, encoding="utf-8", stdout=PIPE)
    print(rtn)

    yield

    # teardown:終了処理
    if os.path.exists(os.path.join(basepath_main_script, "data")):
        shutil.rmtree(os.path.join(basepath_main_script, "data"))


@pytest.fixture
def setup_metadatadef_json():
    metadata_filename = "metadata-def.json"

    test_specification_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates", "template", metadata_filename)

    with open(test_specification_path, mode="r", encoding="utf-8") as f:
        contents = json.load(f)
        print(contents)

    yield contents


@pytest.fixture
def setup_invoice_schema_json():
    metadata_filename = "invoice.schema.json"

    test_specification_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates", "template", metadata_filename)

    with open(test_specification_path, mode="r", encoding="utf-8") as f:
        contents = json.load(f)
        print(contents)

    yield contents


@pytest.fixture
def input_data_pattern1():
    data = """[Header]
ExperimentName,Example Experiment
Date,2024-08-07
Operator,John Doe
Temperature,25.0,25.5,26.0
Pressure,1.0,1.1,1.2
Comment,This is a test experiment

[Data]
Time,Value
0,0.1
1,0.15
2,0.2
3,0.25
"""
    yield data


@pytest.fixture
def input_data_pattern2():
    data = """-ExperimentName	Example Experiment
-Date	2024-08-07
-Operator	John Doe
-Temperature	25.0	25.5	26.0
-Pressure	1.0	1.1	1.2
-Comment	This is a test experiment

0	0.1
1	0.15
2	0.2
3	0.25
"""
    yield data


@pytest.fixture
def input_data_pattern3():
    data = """header
; header comments
ExperimentName:Example Experiment
Date:2024-08-07
Operator:John Doe
Temperature:25.0:25.5:26.0
Pressure:1.0:1.1:1.2
Comment:This is a test experiment

data
; header comments
0,0.1
1,0.15
"""
    yield data
