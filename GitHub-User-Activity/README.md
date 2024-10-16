Aquí tienes un ejemplo de un README para tu proyecto:

---

# GitHub User Activity Tracker CLI

This is a command-line tool built in Python that allows users to track GitHub events of a specific user, such as pushes, forks, issue creations, and more. It fetches data from the GitHub Events API and displays a summary of the activities grouped by repository.

## Features

- Fetch and display GitHub user activities, including:
  - Push events (number of commits pushed)
  - Branch creation
  - Repository creation
  - Branch deletion
  - Forking a repository
  - Watching a repository
  - Issue events (opened or closed)
  - Pull request events (opened or closed)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/github-activity-tracker.git
   cd github-activity-tracker
   ```

2. **Install Python** (if not already installed):  
   - Ensure you have Python 3.6+ installed. You can download it from [here](https://www.python.org/downloads/).

3. **No additional libraries needed**:  
   The script uses only standard Python libraries (`urllib`, `json`, and `argparse`), so no external dependencies are required.

## Usage

Run the script using the following command format:

```bash
python github-activity-cli.py github-activity <github-username>
```

For example, to track the activities of the user `icyjkk`, you would run:

```bash
python github-activity-cli.py github-activity icyjkk
```

### Example Output

```plaintext
Repository: icyjkk/Backend-Projects
- Pushed 3 commit(s)
- Created branch 'feature'

Repository: icyjkk/Discord-bot-inventory-wtn
- Deleted branch 'master'
- Forked repository to 'icyjkk/discord-bot-new-repo'
```

## Command-line Arguments

- `command`: The command to execute. In this case, it should always be `github-activity`.
- `name`: The GitHub username to track.

### Example:

```bash
python github-activity-cli.py github-activity icyjkk
```

## Error Handling

- **HTTP Errors**: If the GitHub API returns an error (e.g., rate-limiting, 404 for user not found), it will print the corresponding HTTP error code and message.
- **URL Errors**: If there is an issue with connecting to the API (e.g., no internet), the script will display the appropriate error.
- **General Errors**: Any other errors will be caught and displayed to the user.

## Contributing

If you'd like to contribute, feel free to fork the repository and submit a pull request. Make sure to include clear commit messages and ensure the code is well-tested.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize this based on any additional features or information you'd like to include!
