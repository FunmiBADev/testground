import os
from gitlab import Gitlab

def search_yaml_files_in_projects(group_id, file_paths):
    try:
        token = os.environ.get('GITLAB_PRIVATE_TOKEN')
        if not token:
            print("Error: GitLab private access token not found in environment variables.")
            return

        gl = Gitlab('https://gitlab.com', private_token=token)
        projects = gl.projects.list(group=group_id, all=True)

        for project in projects:
            for file_path in file_paths:
                yaml_files = project.repository_tree(recursive=True, all=True, path=file_path, ref='master', as_list=True)
                for yaml_file in yaml_files:
                    if yaml_file['name'].endswith('.yml'):
                        file_content = project.files.raw(file_path=yaml_file['path'], ref='master')
                        print(f"Project: {project.name}, File Path: {file_path}, File Name: {yaml_file['name']}, File Content: {file_content}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    group_id = input("Enter the Group ID: ")
    file_paths = input("Enter the file paths (comma-separated): ").split(',')
    search_yaml_files_in_projects(group_id, file_paths)


import os
from gitlab import Gitlab

def print_repository_tree_for_projects(group_id):
    try:
        token = os.environ.get('GITLAB_PRIVATE_TOKEN')
        if not token:
            print("Error: GitLab private access token not found in environment variables.")
            return

        gl = Gitlab('https://gitlab.com', private_token=token)
        projects = gl.projects.list(group=group_id, all=True)

        for project in projects:
            print(f"Project: {project.name}")
            tree = project.repository_tree(all=True)
            for item in tree:
                print(f"    {item['path']} - {item['type']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    group_id = input("Enter the Group ID: ")
    print_repository_tree_for_projects(group_id)
