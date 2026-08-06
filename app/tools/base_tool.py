from abc import ABC, abstractmethod
from .tool_result import ToolResult


class BaseTool(ABC):
    """
    Every tony tool must inherit from this class.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique tool name.
        Example: browser, volume, files
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Description sent to the LLM.
        """
        pass

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """
        Executes the tool.
        """
        pass