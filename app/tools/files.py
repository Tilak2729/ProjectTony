from pathlib import Path
import shutil
import subprocess
import os

from registry.decorators import tool
from tools.tool_result import ToolResult


HOME = Path.home()

ONEDRIVE = Path(
    os.environ.get(
        "OneDrive",
        HOME / "OneDrive"
    )
)

KNOWN_FOLDERS = {
    "desktop": (
        ONEDRIVE / "Desktop"
        if (ONEDRIVE / "Desktop").exists()
        else HOME / "Desktop"
    ),

    "downloads": (
        ONEDRIVE / "Downloads"
        if (ONEDRIVE / "Downloads").exists()
        else HOME / "Downloads"
    ),

    "documents": (
        ONEDRIVE / "Documents"
        if (ONEDRIVE / "Documents").exists()
        else HOME / "Documents"
    ),
}


def resolve_path(path: str) -> Path:

    path = path.strip()

    # Known special folders
    if path.lower() in KNOWN_FOLDERS:

        return KNOWN_FOLDERS[path.lower()]

    requested = Path(path).expanduser()

    # Exact path already exists
    if requested.exists():

        return requested

    # Try resolving the path relative to the current directory
    current_path = Path.cwd() / requested

    if current_path.exists():

        return current_path

    # Normalize the spoken name:
    # "Tony Test" -> "tonytest"
    target_name = (
        requested.name
        .replace(" ", "")
        .lower()
    )

    # Search common user folders
    for base_folder in KNOWN_FOLDERS.values():

        if not base_folder.exists():

            continue

        # First check direct children
        for item in base_folder.iterdir():

            actual_name = (
                item.name
                .replace(" ", "")
                .lower()
            )

            if actual_name == target_name:

                return item

        # Then search one level deeper
        try:

            for item in base_folder.rglob("*"):

                actual_name = (
                    item.name
                    .replace(" ", "")
                    .lower()
                )

                if actual_name == target_name:

                    return item

        except Exception:

            continue

    # Return original path if nothing matched
    return requested


@tool(
    name="file_manager",
    description="""
Manage files and folders on the computer.

Actions:
- list: List files and folders inside a directory.
- create_folder: Create a new folder.
- open_folder: Open a folder in Windows File Explorer.
- find: Find files by name inside a directory.
- copy: Copy a file.
- move: Move a file.
- rename: Rename a file or folder.
- delete: Delete a file or folder.

Parameters:
action (string)
path (string, optional)
name (string, optional)
destination (string, optional)
"""
)
def file_manager(
    action: str,
    path: str = None,
    name: str = None,
    destination: str = None,
    confirmed: bool = False
) -> ToolResult:

    try:

        if action == "list":

            if not path:

                return ToolResult(
                    False,
                    "Please specify a folder."
                )

            folder = resolve_path(path)

            if not folder.exists():

                return ToolResult(
                    False,
                    f"The folder {folder} does not exist."
                )

            if not folder.is_dir():

                return ToolResult(
                    False,
                    f"{folder} is not a folder."
                )

            items = list(folder.iterdir())

            if not items:

                return ToolResult(
                    True,
                    "The folder is empty."
                )

            result = []

            for item in items:

                item_type = (
                    "Folder"
                    if item.is_dir()
                    else "File"
                )

                result.append(
                    f"{item_type}: {item.name}"
                )

            return ToolResult(
                True,
                "\n".join(result[:100])
            )

        if action == "create_folder":

            if not path:

                return ToolResult(
                    False,
                    "Please specify where to create the folder."
                )

            if not name:

                return ToolResult(
                    False,
                    "Please specify the folder name."
                )

            parent = resolve_path(path)

            if not parent.exists():

                return ToolResult(
                    False,
                    f"The folder {parent} does not exist."
                )

            new_folder = parent / name

            if new_folder.exists():

                return ToolResult(
                    False,
                    f"{new_folder.name} already exists."
                )

            new_folder.mkdir()

            return ToolResult(
                True,
                f"Created folder {new_folder.name}."
            )

        if action == "open_folder":

            if not path:

                return ToolResult(
                    False,
                    "Please specify a folder."
                )

            folder = resolve_path(path)

            if not folder.exists():

                return ToolResult(
                    False,
                    f"The folder {folder} does not exist."
                )

            if not folder.is_dir():

                return ToolResult(
                    False,
                    f"{folder} is not a folder."
                )

            subprocess.Popen(
                ["explorer", str(folder)]
            )

            return ToolResult(
                True,
                f"Opened folder {folder.name}."
            )

        if action == "find":

            if not path:

                return ToolResult(
                    False,
                    "Please specify where to search."
                )

            if not name:

                return ToolResult(
                    False,
                    "Please specify the file name."
                )

            folder = resolve_path(path)

            if not folder.exists():

                return ToolResult(
                    False,
                    f"The folder {folder} does not exist."
                )

            matches = []

            search_term = name.lower()

            for item in folder.rglob("*"):

                if search_term in item.name.lower():

                    matches.append(
                        str(item)
                    )

                if len(matches) >= 50:

                    break

            if not matches:

                return ToolResult(
                    True,
                    f"No files matching '{name}' were found."
                )

            return ToolResult(
                True,
                "\n".join(matches)
            )

        if action == "copy":

            if not path or not destination:

                return ToolResult(
                    False,
                    "Both source and destination are required."
                )

            source = resolve_path(path)
            target = resolve_path(destination)

            if not source.exists():

                return ToolResult(
                    False,
                    f"{source} does not exist."
                )

            if source.is_dir():

                return ToolResult(
                    False,
                    "Copying folders is not supported yet."
                )

            if target.is_dir():

                target = target / source.name

            shutil.copy2(
                source,
                target
            )

            return ToolResult(
                True,
                f"Copied {source.name} successfully."
            )

        if action == "move":

            if not path or not destination:

                return ToolResult(
                    False,
                    "Both source and destination are required."
                )

            source = resolve_path(path)
            target = resolve_path(destination)

            if not source.exists():

                return ToolResult(
                    False,
                    f"{source} does not exist."
                )

            if target.is_dir():

                target = target / source.name

            shutil.move(
                str(source),
                str(target)
            )

            return ToolResult(
                True,
                f"Moved {source.name} successfully."
            )

        if action == "rename":

            if not path:

                return ToolResult(
                    False,
                    "Please specify the file or folder to rename."
                )

            if not name:

                return ToolResult(
                    False,
                    "Please specify the new name."
                )

            source = resolve_path(path)

            if not source.exists():

                return ToolResult(
                    False,
                    f"{source} does not exist."
                )

            target = source.parent / name

            if target.exists():

                return ToolResult(
                    False,
                    f"{target.name} already exists."
                )

            source.rename(target)

            return ToolResult(
                True,
                f"Renamed to {target.name}."
            )

        if action == "delete":

            if not path:

                return ToolResult(
                    False,
                    "Please specify what should be deleted."
                )

            target = resolve_path(path)

            if not target.exists():

                return ToolResult(
                    False,
                    f"{target} does not exist."
                )

            if not confirmed:

                return ToolResult(
                    False,
                    "Delete requires confirmation before execution."
                )

            if target.is_dir():

                shutil.rmtree(target)

            else:

                target.unlink()

            return ToolResult(
                True,
                f"{target.name} deleted successfully."
            )

        return ToolResult(
            False,
            "Unsupported file manager action."
        )

    except Exception as e:

        print(f"File manager error: {e}")

        return ToolResult(
            False,
            "I could not complete the file operation."
        )