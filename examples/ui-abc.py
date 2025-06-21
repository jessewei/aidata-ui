from abc import ABC, abstractmethod  # [3, 5, 6]
from dataclasses import dataclass
from mininterface import run


# Define an Abstract Base Class for a data processor
class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: float) -> float:
        """
        Abstract method: All concrete processors must implement this.
        """
        pass  # [3, 5, 6]


class SimpleProcessor(DataProcessor):
    """A concrete processor that doubles the input."""

    def process(self, data: float) -> float:
        return data * 2


class ComplexProcessor(DataProcessor):
    """A concrete processor that applies a more complex transformation."""

    def process(self, data: float) -> float:
        return (data**2) + 5


@dataclass
class AppConfig:
    """
    Configuration for our application, including which processor to use.
    """

    initial_value: float = 10.0
    processor_type: str = "simple"  # User selects 'simple' or 'complex'


def main():
    with run(AppConfig, title="Processor App") as m:
        # Use mininterface to get the initial value and processor type from the user
        m.form({"initial_value": m.env.initial_value, "processor_type": m.env.processor_type})

        processor: DataProcessor  # Type hint for clarity

        if m.env.processor_type == "simple":
            processor = SimpleProcessor()
        elif m.env.processor_type == "complex":
            processor = ComplexProcessor()
        else:
            print("Invalid processor type selected. Using SimpleProcessor.")
            processor = SimpleProcessor()

        # The application interacts with the processor via its abstract interface
        # ensuring that the 'process' method is always available.
        result = processor.process(m.env.initial_value)
        m.confirm(f"Processed value: {result}")


if __name__ == "__main__":
    main()
