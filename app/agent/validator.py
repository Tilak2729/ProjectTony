class ResponseValidator:

    @staticmethod
    def validate(response):

        if not isinstance(response, dict):
            return False

        if "type" not in response:
            return False

        if response["type"] == "conversation":

            return "response" in response

        if response["type"] == "tool_call":

            required = [
                "tool",
                "arguments"
            ]

            return all(
                key in response
                for key in required
            )

        return False