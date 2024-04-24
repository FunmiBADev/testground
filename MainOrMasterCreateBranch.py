import gitlab
import getpass

def create_branch(project_ids, branch, token):
    gitlab_url = 'https://gitlab.com'
    gl = gitlab.Gitlab(gitlab_url, private_token=token)

    for project_id in project_ids:
        project = gl.projects.get(project_id)
        existing_branches = project.branches.list()

        if any(existing_branch.name == branch for existing_branch in existing_branches):
            print(f"Branch '{branch}' already exists in project with ID '{project_id}'.")
        else:
            default_branch = project.default_branch

            if default_branch in ['master', 'main']:
                branch_obj = project.branches.create({'branch': branch, 'ref': default_branch})
                print(f"New branch '{branch_obj.name}' created successfully from {default_branch} branch in project with ID '{project_id}'.")
            else:
                print(f"Error: Default branch is neither 'master' nor 'main' in project with ID '{project_id}'. Unable to create branch.")

def main():
    project_ids = [12345678, 87654321]  # Replace with your project IDs
    new_branch = 'test_branch'
    token = getpass.getpass("Enter your GitLab personal access token: ")

    create_branch(project_ids, new_branch, token)

if __name__ == "__main__":
    main()
