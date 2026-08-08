class ToolExecutor:

    def __init__(self, registry):
        self.registry = registry

    def execute(self, tool_name, arguments):

        tool = self.registry.get(tool_name)

        if tool is None:

            return {
                "success": False,
                "message": f"Tool '{tool_name}' is not available."
            }

        if not isinstance(arguments, dict):

            return {
                "success": False,
                "message": "Invalid tool arguments."
            }

        try:

            result = tool["function"](**arguments)

            return {
                "success": result.success,
                "message": result.message
            }

        except TypeError as e:

            print(f"\n❌ Invalid tool arguments: {e}")

            return {
                "success": False,
                "message": "The requested action contained invalid arguments."
            }

        except Exception as e:

            print(f"\n❌ Tool error: {e}")

            return {
                "success": False,
                "message": "The tool could not complete the requested action."
            }