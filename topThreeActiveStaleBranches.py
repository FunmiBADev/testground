import gitlab
from datetime import datetime, timedelta

# Initialize the GitLab connection
gl = gitlab.Gitlab('https://gitlab.com', private_token='your_private_token')

def get_project_and_branches(project_id):
    project = gl.projects.get(project_id)
    branches = project.branches.list(all=True)
    return project, branches

def sort_branches_by_activity(branches, top_n=3):
    # Sort branches by the date they were last committed to
    branches.sort(key=lambda x: x.commit['committed_date'], reverse=True)
    
    # Get top N active branches
    active_branches = branches[:top_n]
    
    # Get top N stale branches
    stale_branches = branches[-top_n:]
    
    return active_branches, stale_branches

def format_branch_info(branch):
    # Get the creation date from the branch's commit
    creation_date = branch.commit['created_at']
    
    return {
        'name': branch.name,
        'creation_date': creation_date,
        'last_commit_date': branch.commit['committed_date'],
        'last_commit_message': branch.commit['message'],
    }

def get_top_branches(project_id, top_n=3):
    project, branches = get_project_and_branches(project_id)
    
    active_branches, stale_branches = sort_branches_by_activity(branches, top_n=top_n)
    
    active_branches_info = [format_branch_info(branch) for branch in active_branches]
    stale_branches_info = [format_branch_info(branch) for branch in stale_branches]
    
    return {
        'project_name': project.name,
        'top_active_branches': active_branches_info,
        'top_stale_branches': stale_branches_info,
    }

# Example usage
project_id = 12345678  # Replace with your project ID
top_branches = get_top_branches(project_id, top_n=3)
print("Project Name:", top_branches['project_name'])
print("Top 3 Active Branches:", top_branches['top_active_branches'])
print("Top 3 Stale Branches:", top_branches['top_stale_branches'])
