import os
from gitlab import Gitlab

def get_project_path(group_id, project_name):
    try:
        # Initialize Gitlab instance
        gl = Gitlab('https://gitlab.com', private_token=os.environ.get('GITLAB_PRIVATE_TOKEN'))

        # Get the group
        group = gl.groups.get(group_id)

        # Search for the project within the group
        projects = group.projects.list(search=project_name)

        # Check if the project exists in the group
        if projects:
            # Assuming there is only one project with the given name in the group
            project = projects[0]
            return project.path_with_namespace
        else:
            print(f"Project '{project_name}' not found in group '{group_id}'.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    group_id = input("Enter the group ID: ")
    project_name = input("Enter the project name: ")

    project_path = get_project_path(group_id, project_name)
    if project_path:
        print(f"Project path: {project_path}")

