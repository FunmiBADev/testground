import gitlab
import getpass

# GitLab API access token
access_token = "Update"

def create_branch(project_name, branch, token):
    # GitLab instance URL
    gitlab_url = 'https://gitlab.com'
    # Create GitLab instance
    gl = gitlab.Gitlab(gitlab_url, private_token=token)

    # Find project by name
    project = gl.projects.get(project_name)


    # Create new branch from 'main' branch
    branch = project.branches.create({'branch': branch, 'ref': 'main'})

    print(f"New branch '{branch}' created successfully from main branch.")

def main():
    project_name = 'FunmiBADev/DevOps-Course-Workshop-Module-07-Learners'
    new_branch = 'test_branch'

    # Get personal access token securely
    token = getpass.getpass("Enter your GitLab personal access token: ")

    create_branch(project_name, new_branch, token)

if __name__ == "__main__":
    main()

def edit_and_commit(project_name, branch_name, token):
  # GitLab instance URL
  gitlab_url = 'https://gitlab.com'
  # Create GitLab instance
  gl = gitlab.Gitlab(gitlab_url, private_token=token)

  # Find project by name
  project = gl.projects.get(project_name)

  file_path = '.gitlab-ci.yml'
  file_content = project.files.get(file_path, ref='main').decode()
  new_line = '- new/templata/scan_build_always\n'
  new_content = file_content.decode() + new_line

  # Update the existing file instead of creating a new one
  project.files.update(file_path, {'content': new_content, 'branch': branch_name, 'commit_message': 'Add new line to gitlab-ci.yml'})

  # Commit and push changes
  project.commits.create({'branch': branch_name, 'commit_message': 'scan changes'})

  print("Changes committed and pushed successfully.")

def main():
  project_name = 'FunmiBADev/DevOps-Course-Workshop-Module-07-Learners'
  branch_name = 'test_branch'  # Set branch name as a variable

  # Get personal access token securely
  token = getpass.getpass("Enter your GitLab personal access token: ")

  edit_and_commit(project_name, branch_name, token)

if __name__ == "__main__":
  main()




