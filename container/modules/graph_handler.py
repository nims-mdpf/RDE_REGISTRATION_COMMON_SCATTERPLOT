from __future__ import annotations

from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
from pydantic import BaseModel, Field, field_validator

from modules.models import InvoiceJson

plt.rcParams["font.family"] = "Hiragino Sans"


class GraphOptions(BaseModel):
    xlabel: str | None = Field(default=None)
    ylabel: str | None = Field(default=None)
    x_col_num: int = Field(default=0)
    y_col_num: int = Field(default=1)
    title_fontsize: int | float = Field(default=16)
    label_fontsize: int | float = Field(default=12)
    scale_fontsize: int | float = Field(default=10)
    title: str | None = Field(default=None)

    @field_validator("x_col_num", "y_col_num")
    def adjust_column_number(cls, v: int) -> int:
        """Adjust the given column number by decrementing it if it is greater than zero.

        Args:
            v (int): The column number to adjust.

        Returns:
            int: The adjusted column number. If the input is greater than zero,
                the result is the input minus one. Otherwise, the input is
                returned unchanged.

        """
        if v > 0:
            return v - 1
        return v


class GraphPlotter:
    """Plot a scatterplot of the given data and save it to the specified path.

    Args:
        data (pd.DataFrame): The data to be plotted.
        save_path (Path): The path to save the plot.
        title (str | None, optional): The title of the plot. Defaults to None.
        xlabel (str | None, optional): The label for the x-axis. Defaults to None.
        ylabel (str | None, optional): The label for the y-axis. Defaults to None.

    """

    def plot(self, data: pd.DataFrame, save_path: Path, option: GraphOptions) -> None:
        """Plot the data and save the plot to the specified path.

        Args:
            data (pd.DataFrame): The data to be plotted. The first column is used for the x-axis and the second column for the y-axis.
            save_path (Path): The path where the plot image will be saved.
            title (str | None, optional): The title of the plot  . Defaults to None.
            xlabel (str | None, optional): The label for the x-axis. Defaults to None.
            ylabel (str | None, optional): The label for the y-axis. Defaults to None.
            option (GraphOptions): The options for configuring the graph such as labels, column numbers, and font size.

        """
        _select_x_col_num = option.x_col_num if option.x_col_num else 0
        _select_y_col_num = option.y_col_num if option.y_col_num else 1
        new_df = data if _select_x_col_num == 0 and _select_y_col_num == 1 else data.iloc[:, [_select_x_col_num, _select_y_col_num]]
        fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=100)
        ax.scatter(new_df.iloc[:, 0], new_df.iloc[:, 1])

        if option.title:
            ax.set_title(option.title, fontsize=option.title_fontsize)
        if option.xlabel:
            ax.set_xlabel(option.xlabel, fontsize=option.label_fontsize)
        if option.ylabel:
            ax.set_ylabel(option.ylabel, fontsize=option.label_fontsize)

        # Set the number of ticks (aiming for 4-6 ticks)
        ax.xaxis.set_major_locator(MaxNLocator(6, integer=False))
        ax.yaxis.set_major_locator(MaxNLocator(6, integer=False))

        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.1f}' if x % 1 != 0 else f'{int(x)}'))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.1f}' if y % 1 != 0 else f'{int(y)}'))

        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')

        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        ax.tick_params(axis='both', which='major', labelsize=option.scale_fontsize)
        plt.subplots_adjust(left=0.2, bottom=0.15)

        plt.savefig(save_path)
        plt.close()
        plt.cla()

    def create_options(self, invoice_obj: InvoiceJson) -> GraphOptions:
        """Create and return a GraphOptions object based on the provided invoice JSON file.

        Args:
            invoice_obj (InvoiceJson): The invoice object containing the data for creating graph options.

        Returns:
            GraphOptions: An object containing graph configuration options such as x-axis label, y-axis label, x-axis column index, and y-axis column index.

        Notes:
            - Exception handling is not required because the x-axis and y-axis label names are mandatory in the JSON file.
            - If the x-axis or y-axis column index is not specified in the JSON file, default values of 0 and 1 are used respectively.

        """
        # x_col_num = invoice_obj.custom.x_axis_column_index if invoice_obj.custom.x_axis_column_index else 0
        # y_col_num = invoice_obj.custom.y_axis_column_index if invoice_obj.custom.y_axis_column_index else 1

        return GraphOptions(
            xlabel=invoice_obj.get_xaxis_label_name(),
            ylabel=invoice_obj.get_yaxis_label_name(),
            x_col_num=invoice_obj.custom.x_axis_column_index if invoice_obj.custom.x_axis_column_index else 0,
            y_col_num=invoice_obj.custom.y_axis_column_index if invoice_obj.custom.y_axis_column_index else 1,
            label_fontsize=18,
            scale_fontsize=12,
        )
