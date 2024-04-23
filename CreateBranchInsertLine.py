import gitlab

# GitLab API access token
access_token = "Add Access Token"


# GitLab API endpoint and personal access token
GITLAB_URL = 'https://gitlab.com/'
PRIVATE_TOKEN = access_token

# GitLab project name
PROJECT_NAME = 'FunmiBADev/DevOps-Course-Workshop-Module-07-Learners'

# Create GitLab connection
gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)

# Find the project by name
project = gl.projects.get(PROJECT_NAME)

# Create a new branch
branch_name = 'test_create_branch15'
project.branches.create({'branch': branch_name, 'ref': 'main'})


# Edit gitlab-ci.yml file and insert a new line
# Edit gitlab-ci.yml file and insert a new line
file_path = '.gitlab-ci.yml'
file_content = project.files.get(file_path, ref='main').decode()
new_line = '- new/templata/scan_build_always\n'
# Corrected code snippet
new_content = file_content.decode() + '\n' + new_line

# Update the existing file instead of creating a new one
# Corrected code snippet with file_path as a string
project.files.update(file_path, {'content': new_content, 'branch': branch_name, 'commit_message': 'Add new line to gitlab-ci.yml'})

# Commit and push changes
project.commits.create({'branch': branch_name, 'commit_message': 'scan changes'})

print("Script executed successfully.")


### With getpass

import gitlab
from getpass import getpass

# GitLab API endpoint
GITLAB_URL = 'https://gitlab.com/'

# Prompt for GitLab private token
PRIVATE_TOKEN = getpass("Enter your GitLab private token: ")

# GitLab project name
PROJECT_NAME = 'FunmiBADev/DevOps-Course-Workshop-Module-07-Learners'

# Create GitLab connection
gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)

# Find the project by name
project = gl.projects.get(PROJECT_NAME)

# Create a new branch
branch_name = 'test_create_branch15'
project.branches.create({'branch': branch_name, 'ref': 'main'})

# Edit gitlab-ci.yml file and insert a new line
file_path = '.gitlab-ci.yml'
file_content = project.files.get(file_path, ref='main').decode()
new_line = '- new/templata/scan_build_always\n'
new_content = file_content.decode() + '\n' + new_line

# Update the existing file instead of creating a new one
project.files.update(file_path, {'content': new_content, 'branch': branch_name, 'commit_message': 'Add new line to gitlab-ci.yml'})

# Commit and push changes
project.commits.create({'branch': branch_name, 'commit_message': 'scan changes'})

print("Script executed successfully.")
