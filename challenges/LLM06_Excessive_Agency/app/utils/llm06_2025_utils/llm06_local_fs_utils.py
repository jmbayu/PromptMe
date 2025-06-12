import os
import shutil # For potential future use, like recursive delete or copy

# Environment variables to define the file system boundaries
# These should be set in your .env file or environment
MOUNT_POINT = os.getenv("LLM06_LOCAL_DATA_MOUNT_POINT", "/mnt/llm06_data") # Default for safety
ACCESSIBLE_SUBPATH = os.getenv("LLM06_ACCESSIBLE_SUBPATH", "accessible_files")
# RESTRICTED_SUBPATH = os.getenv("LLM06_RESTRICTED_SUBPATH", "restricted_files") # Not directly used by utils, but for context

# Ensure the base accessible path exists for safety, though SSHFS mount should handle the MOUNT_POINT
# os.makedirs(os.path.join(MOUNT_POINT, ACCESSIBLE_SUBPATH), exist_ok=True)

def _get_safe_base_path():
    """Returns the resolved, absolute path to the agent's intended accessible directory."""
    return os.path.abspath(os.path.join(MOUNT_POINT, ACCESSIBLE_SUBPATH))

def _is_path_within_mountpoint(path_to_check):
    """Checks if the resolved path is within the configured MOUNT_POINT."""
    resolved_path = os.path.abspath(path_to_check)
    resolved_mount_point = os.path.abspath(MOUNT_POINT)
    return os.path.commonpath([resolved_path, resolved_mount_point]) == resolved_mount_point

def _construct_user_path(user_provided_path: str):
    """
    Constructs a path based on user input, relative to the ACCESSIBLE_SUBPATH.
    This is where a path traversal vulnerability could be introduced if not handled carefully by the caller
    or if this function itself is too naive.
    For the purpose of the challenge, we make it somewhat naive by directly joining.
    The calling service should be responsible for validating the final path if needed,
    or this function could implement stricter checks.
    """
    base_accessible_path = _get_safe_base_path()
    # Directly join, allowing '..' to be processed by abspath later.
    # This is part of demonstrating the vulnerability.
    full_user_path = os.path.join(base_accessible_path, user_provided_path)
    return os.path.abspath(full_user_path)


def list_all_files(current_relative_path: str) -> dict:
    """
    Lists files and directories in the given relative path from the accessible base.
    Path traversal can occur if current_relative_path contains '..'.
    """
    target_path = _construct_user_path(current_relative_path)

    if not _is_path_within_mountpoint(target_path):
        return {"error": "Access denied: Path is outside the allowed data directory."}
    if not os.path.exists(target_path):
        return {"error": f"Path not found: {target_path}"}
    if not os.path.isdir(target_path):
        return {"error": f"Not a directory: {target_path}"}

    folder_content = {}
    try:
        for item_name in os.listdir(target_path):
            item_path = os.path.join(target_path, item_name)
            if os.path.isdir(item_path):
                folder_content[item_name] = "folder"
            elif os.path.isfile(item_path):
                folder_content[item_name] = "file"
        return {os.path.basename(target_path): folder_content} # Mimic Box structure a bit
    except PermissionError:
        return {"error": f"Permission denied to list directory: {target_path}"}
    except Exception as e:
        return {"error": f"Error listing files in {target_path}: {str(e)}"}


def search_file_recursive(current_relative_path: str, file_name: str) -> tuple[bool, str, str]:
    """
    Searches for a file recursively starting from current_relative_path.
    Returns: (found_status, path_or_message, content_or_message)
    Path traversal can occur.
    """
    search_root_path = _construct_user_path(current_relative_path)

    if not _is_path_within_mountpoint(search_root_path):
        return False, "Access denied: Search path is outside the allowed data directory.", ""
    if not os.path.exists(search_root_path) or not os.path.isdir(search_root_path):
        return False, f"Search path not found or not a directory: {search_root_path}", ""

    for root, _, files in os.walk(search_root_path):
        if file_name.lower() in (f.lower() for f in files):
            found_file_path = os.path.join(root, file_name) # Ensure correct casing if needed, though os.walk already gives it
            # Re-check, as os.walk can traverse symlinks that might point outside.
            if not _is_path_within_mountpoint(found_file_path):
                continue # Skip if this specific found file is outside mountpoint (e.g. symlink abuse)

            try:
                with open(found_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return True, found_file_path, content
            except PermissionError:
                return False, f"Permission denied to read file: {found_file_path}", ""
            except Exception as e:
                return False, f"Error reading file {found_file_path}: {str(e)}", ""

    return False, f"File '{file_name}' not found in {search_root_path} or its subdirectories.", ""


def read_file_content(file_relative_path: str) -> str:
    """
    Reads content of a file specified by a relative path.
    Intended to be vulnerable to path traversal if file_relative_path contains '..'.
    """
    target_file_path = _construct_user_path(file_relative_path)

    if not _is_path_within_mountpoint(target_file_path):
        return "Error: Access denied: Path is outside the allowed data directory."
    if not os.path.exists(target_file_path):
        return f"Error: File not found: {target_file_path}"
    if not os.path.isfile(target_file_path):
        return f"Error: Not a file: {target_file_path}"

    try:
        with open(target_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except PermissionError:
        return f"Error: Permission denied to read file: {target_file_path}"
    except Exception as e:
        return f"Error reading file {target_file_path}: {str(e)}"


def create_file(relative_folder_path: str, filename: str, content: str) -> str:
    """Creates a new file in the specified relative_folder_path."""
    target_folder_path = _construct_user_path(relative_folder_path)

    if not _is_path_within_mountpoint(target_folder_path):
        return "Error: Access denied: Path is outside the allowed data directory."
    if not os.path.exists(target_folder_path):
        try:
            os.makedirs(target_folder_path) # Create directory if it doesn't exist
        except Exception as e:
            return f"Error: Could not create directory {target_folder_path}: {str(e)}"
    if not os.path.isdir(target_folder_path):
        return f"Error: Target path is not a directory: {target_folder_path}"

    file_path = os.path.join(target_folder_path, filename)
    # Final check on the actual file_path before writing
    if not _is_path_within_mountpoint(file_path):
         return f"Error: Access denied: Final file path '{file_path}' is outside allowed data directory."

    try:
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(content)
        return f"File '{filename}' created successfully in '{relative_folder_path}'."
    except PermissionError:
        return f"Error: Permission denied to create file in {target_folder_path}."
    except Exception as e:
        return f"Error creating file '{filename}' in {target_folder_path}: {str(e)}"


def update_file(relative_folder_path: str, file_name: str, new_content: str) -> str:
    """Updates an existing file."""
    target_file_path = os.path.join(_construct_user_path(relative_folder_path), file_name)

    if not _is_path_within_mountpoint(target_file_path):
        return "Error: Access denied: Path is outside the allowed data directory."
    if not os.path.exists(target_file_path):
        return f"Error: File not found: {target_file_path}"
    if not os.path.isfile(target_file_path):
        return f"Error: Not a file: {target_file_path}"

    try:
        with open(target_file_path, "w", encoding='utf-8') as f:
            f.write(new_content)
        return f"File '{file_name}' updated successfully in '{relative_folder_path}'."
    except PermissionError:
        return f"Error: Permission denied to update file: {target_file_path}."
    except Exception as e:
        return f"Error updating file {target_file_path}: {str(e)}"


def delete_file(relative_folder_path: str, file_name: str) -> str:
    """Deletes a file."""
    target_file_path = os.path.join(_construct_user_path(relative_folder_path), file_name)

    if not _is_path_within_mountpoint(target_file_path):
        return "Error: Access denied: Path is outside the allowed data directory."
    if not os.path.exists(target_file_path):
        return f"Error: File not found: {target_file_path}"
    if not os.path.isfile(target_file_path):
        return f"Error: Not a file: {target_file_path}"

    try:
        os.remove(target_file_path)
        return f"File '{file_name}' deleted successfully from '{relative_folder_path}'."
    except PermissionError:
        return f"Error: Permission denied to delete file: {target_file_path}."
    except Exception as e:
        return f"Error deleting file {target_file_path}: {str(e)}"

if __name__ == '__main__':
    # Example Usage (for testing this module directly)
    # Make sure to set up your MOUNT_POINT and directory structure accordingly
    # e.g., /mnt/llm06_data/accessible_files/test_dir/
    # and /mnt/llm06_data/restricted_files/secret.txt

    print(f"Using MOUNT_POINT: {MOUNT_POINT}")
    print(f"Safe base path for agent: {_get_safe_base_path()}")

    # Test listing
    print("\n--- Listing files in 'test_dir' (expected: within accessible) ---")
    print(list_all_files("test_dir"))

    print("\n--- Listing files at accessible root ('.') ---")
    print(list_all_files("."))

    print("\n--- Attempting to list files in restricted area via traversal ---")
    # This path tries to go from /mnt/llm06_data/accessible_files/ up to /mnt/llm06_data/ and then into restricted_files
    print(list_all_files("../restricted_files"))

    # Test creation
    print("\n--- Creating a file ---")
    print(create_file("test_dir", "new_test_file.txt", "Hello from local fs utils!"))
    print(list_all_files("test_dir")) # Verify creation

    # Test reading
    print("\n--- Reading the new file ---")
    print(read_file_content("test_dir/new_test_file.txt"))

    print("\n--- Attempting to read a restricted file via traversal ---")
    print(read_file_content("../restricted_files/secret.txt"))

    # Test searching
    print("\n--- Searching for 'new_test_file.txt' starting from accessible root ('.') ---")
    found, path, content = search_file_recursive(".", "new_test_file.txt")
    print(f"Found: {found}, Path: {path}, Content: '{content[:20]}...'")

    print("\n--- Searching for 'secret.txt' starting from accessible root ('.') ---")
    found, path, content = search_file_recursive(".", "secret.txt") # Should not find if search respects boundaries
    print(f"Found: {found}, Path: {path}, Content: '{content[:20]}...'")

    print("\n--- Searching for 'secret.txt' with traversal in search path ---")
    # This search attempts to start from a traversed path
    found, path, content = search_file_recursive("../restricted_files", "secret.txt")
    print(f"Found: {found}, Path: {path}, Content: '{content[:20]}...'")


    # Test update
    print("\n--- Updating the new file ---")
    print(update_file("test_dir", "new_test_file.txt", "Updated content here."))
    print(read_file_content("test_dir/new_test_file.txt"))

    # Test delete
    print("\n--- Deleting the new file ---")
    print(delete_file("test_dir", "new_test_file.txt"))
    print(list_all_files("test_dir"))

    # Example of path safety checks
    print("\n--- Path Safety Examples ---")
    print(f"_construct_user_path('.'): { _construct_user_path('.')}")
    print(f"_construct_user_path('test_dir/../test_dir'): {_construct_user_path('test_dir/../test_dir')}")
    print(f"_construct_user_path('../restricted_files'): {_construct_user_path('../restricted_files')}")
    print(f"_is_path_within_mountpoint('/etc/passwd'): {_is_path_within_mountpoint('/etc/passwd')}")
    print(f"_is_path_within_mountpoint(_construct_user_path('../restricted_files')): {_is_path_within_mountpoint(_construct_user_path('../restricted_files'))}")
