from typing import Annotated
from dataclasses import dataclass
from mininterface.validators import not_empty
from mininterface import run, Tag, Validation


@dataclass
class NestedEnv:
    another_number: int = 7
    """ This field is nested """


@dataclass
class Env:
    nested_config: NestedEnv

    mandatory_str: str
    """ As there is no default value, you will be prompted automatically to fill up the field """

    my_number: int | None = None
    """ This is not just a dummy number, if left empty, it is None. """

    my_string: str = "Hello"
    """ A dummy string """

    my_flag: bool = False
    """ Checkbox test """

    my_validated: Annotated[str, Validation(not_empty)] = "hello"
    """ A validated field """


def hello() -> str:
    return "Hello from aidata hello()!"


def main() -> None:
    # print("Hello from aidata main()!")
    m = run(Env, title="My program")
    # See some values
    print(m.env.nested_config.another_number)  # 7
    print(m.env)
    # Env(nested_config=NestedEnv(another_number=7), my_number=5, my_string='Hello', my_flag=False, my_validated='hello')

    # Edit values in a dialog
    m.form()
