import os


# The path you want to explore
search_path = "C:/Users/AES/Desktop/EDUCONNECT-MAIN/"

# A list of files/folders to exclude (you can add more like .git, .venv, __pycache__)
excluded = ["flask",
            ".git",
            ".venv",
            "__pycache__",
            "recursive_directory_printer.py",
            "test_apis_with_python",
            ]  # Example with common exclusions



def print_directory_tree(startpath, excluded_items=None, prefix=""):
    """
    Prints the directory structure recursively in a tree format.

    Args:
        startpath (str): The path to the directory to start the search from.
        excluded_items (list, optional): A list of file or folder names to exclude.
                                        Default is None (no exclusion).
        prefix (str, optional): The prefix used for indentation and tree lines.
                                This is used internally for recursion.
    """
    if excluded_items is None:
        excluded_items = []

    # Get the list of contents inside the current directory
    try:
        # Use abspath to ensure the path works correctly even if it's relative
        real_startpath = os.path.abspath(startpath)
        entries = os.listdir(real_startpath)
        # Exclude the specified items
        filtered_entries = [e for e in entries if e not in excluded_items]
        # Separate directories and files, and sort each list alphabetically
        dirs = sorted([d for d in filtered_entries if os.path.isdir(os.path.join(real_startpath, d))])
        files = sorted([f for f in filtered_entries if os.path.isfile(os.path.join(real_startpath, f))])
        # Merge the two lists (directories first, then files)
        all_entries = dirs + files
    except FileNotFoundError:
        print(f"{prefix}└── [Error: Directory not found]")
        return
    except PermissionError:
        print(f"{prefix}└── [Error: Permission denied]")
        return
    except OSError as e:
        print(f"{prefix}└── [Error accessing directory: {e.strerror}]")
        return

    # Define tree markers (├── for non-last items, └── for the last item)
    pointers = ['├── '] * (len(all_entries) - 1) + ['└── ']

    for pointer, entry in zip(pointers, all_entries):
        entry_path = os.path.join(real_startpath, entry)
        is_dir = os.path.isdir(entry_path)

        # Print the current entry (add / for directories)
        print(f"{prefix}{pointer}{entry}{'/' if is_dir else ''}")

        if is_dir:
            # Calculate the new prefix for the next level
            # If the current pointer is ├──, continue with the vertical line │
            # If the current pointer is └──, use spaces
            extension = "│   " if pointer == '├── ' else "    "
            # Recursively call the function for the subdirectory
            print_directory_tree(entry_path, excluded_items, prefix + extension)


# --- Usage ---

print(f"{search_path}")  # Print the root directory path first

# Check if the path exists and is a directory before starting
if os.path.isdir(search_path):
    # Start the recursive printing of the root directory contents
    print_directory_tree(search_path, excluded_items=excluded, prefix="")  # No prefix at the first level
else:
    print(f"Error: Path '{search_path}' is not a valid directory or does not exist.")
