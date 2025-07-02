from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator


class Label(BaseModel):
    ja: str
    en: str


class Schema(BaseModel):
    type: str
    format: str | None = Field(default=None)


class ChildItem(BaseModel):
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    name: Label
    schema_: Schema = Field(alias="schema")
    unit: str | None = Field(default=None)
    description: str | None = Field(default=None)
    uri: str | None = Field(default=None)
    mode: str | None = Field(default=None)
    order: str | int = Field(default=None)
    original_name: str | None = Field(default=None, alias="originalName")


class MetaDataDef(RootModel):
    root: dict[str, ChildItem]


class Basic(BaseModel):
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    date_submitted: str | None = Field(default=None, alias="dateSubmitted")
    data_ownerid: str | None = Field(default=None, alias="dataOwnerId")
    data_name: str | None = Field(default=None, alias="dataName")
    instrument_id: str | None = Field(default=None, alias="instrumentId")
    experiment_id: str | None = Field(default=None, alias="experimentId")
    description: str | None = Field(default=None, alias="description")


class Custom(BaseModel):
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    measurement_data_start_character: str
    x_axis_column_index: int | None = Field(default=1, alias="x-axis_column_index")
    y_axis_column_index: int | None = Field(default=2, alias="y-axis_column_index")
    xaxis_label_name: str | None
    yaxis_label_name: str | None
    key1: str | None
    key2: str | None
    key3: str | None
    key4: str | None
    key5: str | None
    key6: str | None
    key7: str | None
    key8: str | None
    key9: str | None
    key10: str | None

    @field_validator("x_axis_column_index")
    def x_axis_replace_none(cls, v: int | None) -> int:
        """Replace None with 0 if the input is None.

        Args:
            v (int | None): The value to check.

        Returns:
            int: The input value if it is not None, otherwise 0.

        """
        return 1 if v is None else v

    @field_validator("y_axis_column_index")
    def y_axis_replace_none(cls, v: int | None) -> int:
        """Replace None with 0 if the input is None.

        Args:
            v (int | None): The value to check.

        Returns:
            int: The input value if it is not None, otherwise 0.

        """
        return 2 if v is None else v


class Sample(BaseModel):
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    sample_id: str | None = Field(default=None, alias="sampleId")
    names: list[str]
    composition: str | None
    reference_url: str | None = Field(default=None, alias="referenceUrl")
    description: str | None
    owner_id: str | None = Field(default=None, alias="ownerId")


class InvoiceJson(BaseModel):
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    dataset_id: str | None = Field(default=None, alias="datasetId")
    basic: Basic
    custom: Custom
    sample: Sample

    def get_xaxis_label_name(self) -> str | None:
        """Retrieve the label name for the x-axis.

        Returns:
            str | None: The label name for the x-axis if it is set, otherwise None.

        """
        return self.custom.xaxis_label_name

    def get_yaxis_label_name(self) -> str | None:
        """Retrieve the label name for the Y-axis.

        Returns:
            str | None: The label name for the Y-axis if set, otherwise None.

        """
        return self.custom.yaxis_label_name

    def to_json(self, path: Path) -> dict[str, Any]:
        """Convert the InvoiceJson object to a JSON string.

        Returns:
            str: The JSON string representation of the InvoiceJson object.

        """
        with path.open('w', encoding='utf-8') as f:
            json.dump(self.model_dump(by_alias=True), f, ensure_ascii=False, indent=2)

        return self.model_dump(by_alias=True)
