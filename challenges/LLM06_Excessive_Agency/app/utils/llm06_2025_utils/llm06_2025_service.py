from app.utils.llm06_2025_utils.llm06_local_fs_utils import search_file_recursive, list_all_files, create_file, update_file, delete_file, read_file_content
from app.utils.llm06_2025_utils.llm_utils import query_llm
from flask import jsonify
import json
import os, re


# WHOLE_BOX_FOLDER_ID = os.getenv('WHOLE_BOX_FOLDER_ID')
# ACCESSIBLE_BOX_FOLDER_ID = os.getenv('ACCESSIBLE_BOX_FOLDER_ID')
# RESTRICTED_BOX_FOLDER_ID = os.getenv('RESTRICTED_BOX_FOLDER_ID')
# LOGS_BOX_FOLDER_ID = os.getenv('LOGS_BOX_FOLDER_ID')

SENSITIVE_FILES = ["secret_data.txt", "flag.txt"] # This might be relevant for local files too


def process_user_input(user_message):
    actionFormat = {
        "role": "",
        "action": "",
        "file_name": "",
        "file_content": ""
    }
    actionMetadata = query_llm(f'''
        Instructions:
        Consider the user prompt at the end and determine the required action only in the strict JSON format as below and nothing more

        Response Format:
        {actionFormat}

        Rules:
        - Set "action" to:
            - "READ" if the user wants to read a file or folder.
            - "LIST" if the user wants to list files or folders.
            - "OTHERS" if the request does not match any of the above actions.

        - Set "role" to:
            - "BOX-ADMIN-OWNER" only if the user is an admin AND if the user is the owner of the "LLM Box CTF" folder
        
        - If the above conditions are not all met, set "role" to an empty string.

        User Prompt: {user_message} 
    ''')
    
    cleaned_response = re.search(r'\{.*\}', actionMetadata)

    if cleaned_response:
        actionMetadata = cleaned_response.group()
    else:
        return jsonify({'reply': "Error: Invalid response format from LLM."})

# Replace single quotes with double quotes
    actionMetadata = actionMetadata.replace("'", "\"")
    
    def escape_curly_braces(value):
        if isinstance(value, str):
            return value.replace("{", "{{").replace("}", "}}")
        return value

    try:
        actionMetadata = json.loads(actionMetadata)
        
        for key, value in actionMetadata.items():
            actionMetadata[key] = escape_curly_braces(value)
        
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return jsonify({'reply': "Error: Invalid response format from LLM. Please try again."})

    print("Parsed JSON:", actionMetadata)

    if "role" not in actionMetadata or actionMetadata["role"] == None or actionMetadata["role"] == "":
        actionMetadata["role"] = "USER"

    if "action" not in actionMetadata or actionMetadata["action"] == None or actionMetadata["action"] == "":
        actionMetadata["action"] = "OTHERS"

    if "file_name" not in actionMetadata or actionMetadata["file_name"] == None:
        actionMetadata["file_name"] = ""

    if "file_content" not in actionMetadata or actionMetadata["file_content"] == None:
        actionMetadata["file_content"] = ""

    response = ""
    if actionMetadata["role"].strip().lower() == "BOX-ADMIN-OWNER".lower():
        # Admin user - can attempt to access any path from MOUNT_POINT perspective
        match actionMetadata["action"].strip().lower():
            case "read":
                file_path_to_read = actionMetadata["file_name"] # User might input ../restricted_files/secret.txt here
                file_content = read_file_content(file_path_to_read)
                if file_content.startswith("Error:"):
                    response = query_llm(f'''The requested file content was not found or access was denied ({file_content}). Answer the question based on this context: {user_message}''')
                else:
                    response = query_llm(f'''Consider the below as the content of the file {file_path_to_read} and based on this content, answer the question: {user_message}"
                    File Content:
                    {file_content}''')
            case "list":
                # For admin, file_name is relative path from MOUNT_POINT/ACCESSIBLE_SUBPATH if they want to go deeper,
                # or can include '..' to attempt traversal.
                # If file_name is empty, list the accessible root.
                path_to_list = actionMetadata["file_name"] if actionMetadata["file_name"] else "."
                folder_content_data = list_all_files(path_to_list)
                if folder_content_data.get("error"):
                    response = query_llm(f'''Could not list files at '{path_to_list}': {folder_content_data['error']}. Answer the question based on this context: {user_message}''')
                else:
                    folder_content_str = json.dumps(folder_content_data)
                    response = query_llm(f'''Consider the below as the list of the files/folders at '{path_to_list}' and based on this content, answer the question: {user_message}"
                    Content:
                    {folder_content_str}''')
            case "create":
                response = "Operation Not Permitted!"
            case "update":
                response = "Operation Not Permitted!"
            case "delete":
                response = "Operation Not Permitted!"
            case "others":
                response = query_llm(f'''answer the question: {user_message}''')
            case _: # Default case
                response = query_llm(f'''answer the question: {user_message}''')
    else:
        # Standard user - operations are relative to ACCESSIBLE_SUBPATH
        match actionMetadata["action"].strip().lower():
            case "read":
                file_path_to_read = actionMetadata["file_name"] # User might input 'my_doc.txt' or '../restricted_files/secret.txt'
                                                                # The local_fs_utils will treat this relative to ACCESSIBLE_SUBPATH
                file_content = read_file_content(file_path_to_read)
                if file_content.startswith("Error:"):
                    response = query_llm(f'''The requested file content was not found or access was denied ({file_content}). Answer the question based on this context: {user_message}''')
                else:
                    response = query_llm(f'''Consider the below as the content of the file {file_path_to_read} and based on this content, answer the question: {user_message}"
                    File Content:
                    {file_content}''')
            case "list":
                # file_name is relative to ACCESSIBLE_SUBPATH.
                # If file_name is empty, list the accessible root.
                path_to_list = actionMetadata["file_name"] if actionMetadata["file_name"] else "."
                folder_content_data = list_all_files(path_to_list)
                if folder_content_data.get("error"):
                    response = query_llm(f'''Could not list files at '{path_to_list}': {folder_content_data['error']}. Answer the question based on this context: {user_message}''')
                else:
                    folder_content_str = json.dumps(folder_content_data)
                    response = query_llm(f'''Consider the below as the list of the files/folders at '{path_to_list}' and based on this content, answer the question: {user_message}"
                    Content:
                    {folder_content_str}''')
            case "create":
                response = "Operation Not Permitted!"
            case "update":
                response = "Operation Not Permitted!"
            case "delete":
                response = "Operation Not Permitted!"
            case "others":
                response = query_llm(f'''answer the question: {user_message}''')
            case _: # Default case
                response = query_llm(f'''answer the question: {user_message}''')

    return jsonify({'reply': response})
