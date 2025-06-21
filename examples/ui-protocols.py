from dataclasses import dataclass
from typing import Protocol, runtime_checkable  # [8]
from mininterface import run


# Define a Protocol for any object that should have 'name' and 'version' attributes
@runtime_checkable  # Allows isinstance() checks at runtime [8]
class Configurable(Protocol):
    name: str
    version: str


# Our mininterface Env dataclass implicitly conforms to the Configurable protocol
# because it has 'name' and 'version' attributes. No explicit inheritance needed.
@dataclass
class MyApplicationEnv:
    """
    Environment configuration for our application.
    """

    name: str = "My Awesome App"
    version: str = "1.0.0"
    author: str = "AI Writer"


def display_app_info(app_config: Configurable):
    """
    This function accepts any object that conforms to the Configurable protocol.
    Static type checkers will verify this.
    """
    print(f"Application Name: {app_config.name}")
    print(f"Application Version: {app_config.version}")


def main():
    with run(MyApplicationEnv, title="Protocol Demo") as m:
        # mininterface automatically handles prompting for missing parameters
        # based on the MyApplicationEnv dataclass.
        m.form({"name": m.env.name, "version": m.env.version, "author": m.env.author})

        # Our MyApplicationEnv instance can be passed to display_app_info
        # because it structurally matches the Configurable protocol.
        display_app_info(m.env)

        # You can also use runtime_checkable for runtime checks (less common for protocols)
        if isinstance(m.env, Configurable):  # [8]
            print("\nRuntime check: MyApplicationEnv instance conforms to Configurable protocol.")
        else:
            print(
                "\nRuntime check: MyApplicationEnv instance DOES NOT conform to Configurable protocol."
            )


if __name__ == "__main__":
    main()
