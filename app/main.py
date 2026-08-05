from registry.registry import registry

# Import tools so they register themselves
import tools.apps


def main():

    print()

    print("Available Functions")

    print("--------------------")

    for tool in registry.list_tools():

        print(tool["name"])
        print(tool["description"])
        print()


if __name__ == "__main__":
    main()