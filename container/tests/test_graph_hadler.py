import os
from pathlib import Path

from matplotlib import pyplot as plt
from unittest.mock import patch
import tempfile
import pandas as pd
import pytest

from modules.graph_handler import GraphPlotter, GraphOptions

plt.rcParams["font.family"] = "Noto Sans CJK JP"


@pytest.fixture
def sample_data():
    """サンプルのデータフレームを返すフィクスチャ"""
    data = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 3, 4, 5, 6]})
    return data


@pytest.fixture
def save_path():
    """一時的な保存パスを返すフィクスチャ"""
    yield Path("tests", "test_plot.png")

    if Path("tests", "test_plot.png").exists():
        os.remove(Path("tests", "test_plot.png"))


@pytest.fixture
def expected_path():
    """期待されるプロットの保存パスを返すフィクスチャ"""
    yield Path("tests", "expected_plot.png")

    if Path("tests", "expected_plot.png").exists():
        os.remove(Path("tests", "expected_plot.png"))


@pytest.fixture
def graph_options():
    # テスト用のGraphOptionsを準備
    yield GraphOptions(x_col_num=0, y_col_num=1, title="Sample Title", xlabel="X-axis", ylabel="Y-axis", title_fontsize=14)


def test_plot(sample_data, graph_options):
    # 一時ディレクトリにファイルを保存
    with tempfile.TemporaryDirectory() as tempdir:
        save_path = Path(tempdir) / "test_plot.png"

        plotter = GraphPlotter()
        plotter.plot(sample_data, save_path, graph_options)
        assert save_path.exists(), "The plot was not saved correctly."


def test_plot_with_mock(sample_data, graph_options):
    # matplotlibのsavefigメソッドをモック化して、正しく呼ばれるか確認
    plotter = GraphPlotter()

    with patch.object(plt, 'savefig') as mock_savefig:
        with tempfile.TemporaryDirectory() as tempdir:
            save_path = Path(tempdir) / "mock_plot.png"
            plotter.plot(sample_data, save_path, graph_options)
            mock_savefig.assert_called_once_with(save_path)
