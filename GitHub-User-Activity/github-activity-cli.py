import urllib.request
import json
import argparse

def fetch_data(user):
    url = f"https://api.github.com/users/{user}/events"

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode("utf-8")
            json_data = json.loads(data)
            return json_data
    
    except urllib.error.HTTPError as e:
        # Manejar errores HTTP específicos
        print(f"HTTPError: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        # Manejar errores de URL o de conexión
        print(f"URLError: {e.reason}")
    except Exception as e:
        # Capturar cualquier otra excepción
        print(f"An error occurred: {e}")

def format_data(data):

    repos_activity = {}

    for event in data:
        repo_name = event['repo']['name']
        
        if repo_name not in repos_activity:
            repos_activity[repo_name] = []
        
        if event['type'] == "PushEvent":
            commit_count = event['payload']['size']
            repos_activity[repo_name].append(f"Pushed {commit_count} commit(s)")
        
        elif event['type'] == "CreateEvent":
            if event['payload']['ref_type'] == "branch":
                branch_name = event['payload']['ref']
                repos_activity[repo_name].append(f"Created branch '{branch_name}'")
            elif event['payload']['ref_type'] == "repository":
                repos_activity[repo_name].append("Created repository")
        
        elif event['type'] == "DeleteEvent":
            if event['payload']['ref_type'] == "branch":
                branch_name = event['payload']['ref']
                repos_activity[repo_name].append(f"Deleted branch '{branch_name}'")
        elif event['type'] == "ForkEvent":
            repo_forked = event['payload']['forkee']['full_name']
            repos_activity[repo_name].append(f"Forked repository to {repo_forked}")
        
        elif event['type'] == "WatchEvent":
            repos_activity[repo_name].append("Started watching repository")
        
        elif event['type'] == "IssuesEvent":
            action = event['payload']['action']
            issue_number = event['payload']['issue']['number']
            repos_activity[repo_name].append(f"{action.capitalize()} issue #{issue_number}")
        
        elif event['type'] == "PullRequestEvent":
            action = event['payload']['action']
            pr_number = event['payload']['pull_request']['number']
            repos_activity[repo_name].append(f"{action.capitalize()} pull request #{pr_number}")
    
    for repo, activities in repos_activity.items():
        print(f"Repository: {repo}")
        for activity in activities:
            print(f"- {activity}")
        print() 

def github_activity_command(args):

    data = fetch_data(args.name)
    format_data(data)
    # print(data)

def main():

    parser = argparse.ArgumentParser(description="Task tracker CLI")
    parser.add_argument('command', type=str, choices=['github-activity'], help='Command to execute') #el primer argumento tiene k ser github-activity
    parser.add_argument('name', type=str, help='Task description')
    args = parser.parse_args()

    if args.command == 'github-activity' and args.name:
        github_activity_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

