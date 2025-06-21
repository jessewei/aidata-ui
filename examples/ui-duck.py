from dataclasses import dataclass
from mininterface import run


@dataclass
class UserConfig:
    """
    This dataclass defines the configuration for our simple application.
    mininterface will automatically generate UI elements for these fields.
    """

    name: str = "Guest"  # [3, 4]
    age: int = 30  # [3, 4]
    is_active: bool = True  # [3, 4]


def main():
    # mininterface.run() adapts based on the environment (GUI, TUI, CLI, Web).
    # It 'ducks' into the appropriate UI backend.
    with run(UserConfig, title="My Adaptive App") as m:  # [3, 4]
        print(f"Initial Name: {m.env.name}, Age: {m.env.age}, Active: {m.env.is_active}")

        # The 'form' method will appear as a graphical window,
        # a text-based form, or CLI prompts depending on the environment.
        # mininterface doesn't care about the *type* of UI, just its *behavior*.
        updated_values = m.form(
            {"name": m.env.name, "age": m.env.age, "is_active": m.env.is_active}  # [3, 4]
        )

        m.env.name = str(updated_values["name"])
        m.env.age = int(updated_values["age"])  # type: ignore
        m.env.is_active = bool(updated_values["is_active"])

        if m.confirm(
            f"Confirm changes? Name: {m.env.name}, Age: {m.env.age}, Active: {m.env.is_active}"
        ):  # [3, 4]
            print("Changes confirmed!")
        else:
            print("Changes discarded.")


if __name__ == "__main__":
    main()
