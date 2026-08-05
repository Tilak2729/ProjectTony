from .registry import registry


def tool(name: str, description: str):

    def decorator(func):

        registry.register(
            name=name,
            description=description,
            function=func
        )

        return func

    return decorator
    