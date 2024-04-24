import gitlab
import getpass

def create_branch(group_id, project_names, branch, token):
    # GitLab instance URL
    gitlab_url = 'https://gitlab.com'
    # Create GitLab instance
    gl = gitlab.Gitlab(gitlab_url, private_token=token)

    # Find group by ID
    group = gl.groups.get(group_id)

    for project_name in project_names:
        try:
            # Find project within group by name
            project = group.projects.get(project_name)
            # Create new branch from 'main' branch
            new_branch = project.branches.create({'branch': branch, 'ref': 'main'})
            print(f"New branch '{branch}' created successfully for project '{project_name}'.")
        except gitlab.exceptions.GitlabGetError as e:
            print(f"Error: Project '{project_name}' not found in group.")

def main():
    group_id = 'your_group_id'  # Update with your group ID
    project_names = ['project1', 'project2', 'project3']  # Update with your project names
    new_branch = 'test_branch'

    # Get personal access token securely
    token = getpass.getpass("Enter your GitLab personal access token: ")

    create_branch(group_id, project_names, new_branch, token)

if __name__ == "__main__":
    main()
