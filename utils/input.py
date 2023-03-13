import os
import tempfile
from dataclasses import dataclass
from enum import Enum
from subprocess import call
from typing import Iterator


EDITOR = os.environ.get("EDITOR", "vim")


class INPUT_FIELD_TYPES(Enum):
    DEFAULT = 0
    EDITOR = 1


def receive_item_input(
    item: dataclass, input_fields: dict[str, INPUT_FIELD_TYPES]
) -> None:
    for key, field_type in input_fields.items():
        text = f"{key}: "
        curr = item.get(key, "")
        text += f"- [{curr}]: " if curr else ""

        if field_type == INPUT_FIELD_TYPES.EDITOR:
            choice = input(
                f"For {key} enter e to open editor or any other to inline edit:"
            )
            item.set(key, text_editor_input(curr)) if choice == "e" else durable_input(
                item, key, text, input
            )
        else:
            durable_input(item, key, text, input)


def durable_input(item: dataclass, key: str, text: str, call_back) -> str:
    try:
        attempt_value = call_back(text)
        if item.get(key) and attempt_value == "":
            return
        item.set(key, attempt_value)
        return
    except Exception as e:
        print(e)
        durable_input(item, key, text, call_back)


def recieve_input(
    input_fields: dict[str, INPUT_FIELD_TYPES], row: dict[str, str] | None = None
) -> dict:
    retval = {}
    is_edit = bool(row)

    input_text = "{key} - [{curr}]: " if is_edit else "{key}: "

    for key in input_fields.keys():
        format_args = {"key": key}
        note = ""
        if row:
            format_args["curr"] = row.get(key)
        if input_fields[key] == INPUT_FIELD_TYPES.EDITOR:
            if row:
                note = row.get(key)
            choice = input(
                f"For {key} enter e to open editor or any other to inline edit:"
            )
            if choice == "e":
                retval[key] = text_editor_input()
            else:
                retval[key] = input(input_text.format(**format_args))
        else:
            retval[key] = input(input_text.format(**format_args))
    return IgnoreEmptyString(retval)


def IgnoreEmptyString(data: dict) -> dict:
    return {k: v for k, v in data.items() if v}


def text_editor_input(org_message: str | None = None) -> str:
    # Open a temporary file to communicate through (´tempfile` should avoid any filename conflicts)
    # NOTE: Don't autodelete the file on close!, We want to reopen the file incase the
    # editor uses a swap-file
    msg = "" if not org_message else org_message
    msg = str.encode(msg)
    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as tf:

        tf.write(msg)

        # Flush the I/O buffer to make sure the data is written to the file
        tf.flush()

        # Open the file with the text editor
        call([EDITOR, tf.name])

    # Reopen the file to read the edited data
    with open(tf.name, "r") as tfs:
        # Read the file data into a variable
        msg = tfs.read()
        tfs.close()
    tf.close()
    os.unlink(tf.name)
    return msg
