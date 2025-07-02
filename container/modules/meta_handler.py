from __future__ import annotations

from pathlib import Path
from typing import cast

from rdetoolkit import rde2util
from rdetoolkit.models.rde2types import MetaType, RepeatedMetaType

from modules.models import InvoiceJson, MetaDataDef


class MetaParser:
    """Class for parsing and saving metadata.

    This class is for parsing pre-acquired metadata and saving it to a file.
    It only handles constant metadata and does not support repeated metadata.

    Args:
        data (dict): The metadata to be parsed.

    Returns:
        tuple[MetaType, RepeatedMetaType | None]: A tuple containing the parsed constant and repeated metadata.

    """

    def parse(self, data: list[tuple[str, str]], metadata_def_path: Path) -> tuple[MetaType, RepeatedMetaType | None]:
        """Parse the given data dictionary and return a tuple containing the constant meta information and the optional repeated meta information.

        Args:
            data (list[tuple[str, str]]): The list of tuples containing metadata key-value pairs to be parsed.
            Each tuple consists of a metadata key and its corresponding value.
            metadata_def_path (Path): The path to the metadata-def.json file.
            This file contains the metadata definitions used for parsing.

        Returns:
            tuple[MetaType, RepeatedMetaType | None]: A tuple containing the constant meta information and the optional repeated meta information.

        """
        _meta: dict = {}
        _data = {item[0]: item[1] for item in data}
        metadef_contents = rde2util.read_from_json_file(metadata_def_path)
        bind_object = MetaDataDef.model_validate(metadef_contents)
        for key, value in bind_object.root.items():
            if value.original_name in _data:
                _meta[key] = _data[value.original_name]

        self.const_meta_info: MetaType = _meta
        self.repeated_meta_info: RepeatedMetaType | None = None

        return self.const_meta_info, self.repeated_meta_info

    def save_meta(
        self,
        save_path: Path,
        metaobj: rde2util.Meta,
        *,
        const_meta_info: MetaType | None = None,
        repeated_meta_info: RepeatedMetaType | None = None,
    ) -> rde2util.Meta:
        """Save the meta information to a file.

        Args:
            save_path (Path): The path where the meta information will be saved.
            metaobj (rde2util.Meta): The meta object containing the information to be saved.
            const_meta_info (Optional[MetaType], optional): The constant meta information to be used. Defaults to None.
            repeated_meta_info (RepeatedMetaType | None, optional): The repeated meta information. Defaults to None.

        Returns:
            assign_meta_info: The assigned meta information.

        """
        _const_meta_info = self.const_meta_info if const_meta_info is None else const_meta_info
        if repeated_meta_info is not None:
            error_message = "Repeated meta info is not supported in this template"
            raise NotImplementedError(error_message)

        metaobj.assign_vals(_const_meta_info)

        return cast(rde2util.Meta, metaobj.writefile(save_path))


def get_invoice_obj(path: str | Path) -> InvoiceJson:
    """Read a JSON file from the given path and return an InvoiceJson object.

    Args:
        path (str | Path): The path to the JSON file.

    Returns:
        InvoiceJson: An object created from the JSON contents.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON.

    """
    json_contents = rde2util.read_from_json_file(path)
    return InvoiceJson(**json_contents)
