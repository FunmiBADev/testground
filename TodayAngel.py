import os
from gitlab import Gitlab

def search_yaml_files_for_keyword(project, keyword):
    try:
        yaml_files = project.repository_tree(recursive=True, all=True, path='/', ref='master', as_list=True)

        for yaml_file in yaml_files:
            if yaml_file['name'].endswith('.yml'):
                file_content = project.files.raw(file_path=yaml_file['path'], ref='master')
                if 'includes' in file_content and keyword in file_content['includes']:
                    print(f"Project: {project.name}, YAML file: {yaml_file['name']}")
    except Exception as e:
        print(f"Failed to search YAML files for project {project.name}. Error: {e}")

def search_projects_for_keyword(projects, keyword):
    for project in projects:
        search_yaml_files_for_keyword(project, keyword)

if __name__ == "__main__":
    token = os.environ.get('GITLAB_PRIVATE_TOKEN')
    if not token:
        print("Error: GitLab private access token not found in environment variables.")
    else:
        gl = Gitlab('https://gitlab.com', private_token=token)
        projects = gl.projects.list(all=True)
        
        keyword = "angel"

        search_projects_for_keyword(projects, keyword)
