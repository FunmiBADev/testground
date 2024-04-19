import os
from gitlab import Gitlab
from gitlab.exceptions import GitlabGetError

def search_yaml_files_for_keyword(project, keyword):
    try:
        yaml_files = project.repository_tree(recursive=True, all=True, path='/', ref='master', as_list=True)

        for yaml_file in yaml_files:
            try:
                if yaml_file['type'] == 'tree':
                    # If it's a directory, recursively search inside it
                    subdir_files = project.repository_tree(recursive=True, all=True, path=yaml_file['path'], ref='master', as_list=True)
                    for subdir_file in subdir_files:
                        if subdir_file['name'].endswith('.yml'):
                            file_content = project.files.raw(file_path=subdir_file['path'], ref='master')
                            if 'includes' in file_content and keyword in file_content['includes']:
                                print(f"Project: {project.name}, YAML file: {subdir_file['path']}")
                elif yaml_file['name'].endswith('.yml'):
                    # If it's a YAML file directly in the root directory
                    file_content = project.files.raw(file_path=yaml_file['path'], ref='master')
                    if 'includes' in file_content and keyword in file_content['includes']:
                        print(f"Project: {project.name}, YAML file: {yaml_file['path']}")
            except GitlabGetError as e:
                if e.response_code == 404:
                    print(f"File not found: {yaml_file['path']}")

    except GitlabGetError as e:
        if e.response_code == 404:
            print(f"Path not found in repository: {e.response_url}")

def search_projects_for_keyword(projects, keyword):
    for project in projects:
        search_yaml_files_for_keyword(project, keyword)

if __name__ == "__main__":
    token = os.environ.get('GITLAB_PRIVATE_TOKEN')
    if not token:
        print("Error: GitLab private access token not found in environment variables.")
    else:
        gl = Gitlab('https://gitlab.com', private_token=token)
        group_id = input("Enter the group ID: ")
        
        # Fetch projects within the specified group only
        group = gl.groups.get(group_id)
        projects = group.projects.list(all=True)

        keyword = input("Enter the keyword to search for in 'includes' section: ")

        search_projects_for_keyword(projects, keyword)
