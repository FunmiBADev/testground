import gitlab
import gitlab.exceptions

# GitLab credentials and project information
GITLAB_URL = 'https://gitlab.com'
PRIVATE_TOKEN = 'your_private_token'  # Replace with your GitLab private token
PROJECT_NAME = 'FunmiBADev/DevOps-Course-Workshop-Module-07-Learners'
FILE_PATH = 'gitlab-ci.yml'
NEW_LINE = "- new/templata/scan_build_always"
COMMIT_MESSAGE = "scan changes"
BRANCH_NAME = 'main'  # Set the branch name here

# Create GitLab object
gl = Gitlab(GITLAB_URL, PRIVATE_TOKEN)

try:
    # Find the project by name
    project = gl.projects.get(PROJECT_NAME)

    # Get the file content
    file = project.files.get(file_path=FILE_PATH, ref=BRANCH_NAME)

    # Append the new line to the existing content
    new_content = file.decode().strip() + '\n' + NEW_LINE

    # Update the file with new content
    project.files.update({'file_path': FILE_PATH, 'branch': BRANCH_NAME, 'content': new_content, 'commit_message': COMMIT_MESSAGE})

    print(f"Changes to '{FILE_PATH}' committed successfully with the message '{COMMIT_MESSAGE}'.")
except exceptions.GitlabGetError:
    print("Project not found. Please check the project name and your credentials.")
except exceptions.GitlabCreateError:
    print("File not found. Please check the file path.")
except Exception as e:
    print(f"An error occurred: {e}")
