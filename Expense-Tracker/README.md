# Expense Tracker CLI

This is a command-line interface (CLI) project for managing your expenses. You can add, list, update, delete, and export your expenses to a CSV file, as well as get summaries of your total expenses or filtered by month.

## Features

- **Add expenses**: Register an expense with a description and amount.
- **List expenses**: Display all registered expenses.
- **Expense summary**: Show the total expenses, with the option to filter by month.
- **Update expenses**: Update the description or amount of an existing expense.
- **Delete expenses**: Delete an expense by its ID.
- **Export to CSV**: Export all expenses to a CSV file.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/icyjkk/Backend-Projects.git
   cd Expense-Tracker
   ```
2. **Install Python** (if not already installed):  

3. **No additional libraries needed**:  
   The script uses only standard Python libraries, so no external dependencies are required.

## Usage

### Available Commands

- **Add an expense**:

   ```bash
   python expense-tracker.py add --description "Expense description" --amount 50
   ```

- **List all expenses**:

   ```bash
   python expense-tracker.py list
   ```

- **Show an expense summary** (total expenses or filtered by month):

   ```bash
   python expense-tracker.py summary
   ```

   To filter by a specific month:

   ```bash
   python expense-tracker.py summary --month 8  # August
   ```

- **Update an expense**:

   ```bash
   python expense-tracker.py update --id 1 --description "New description" --amount 100
   ```

   You can update only one field (description or amount):

   ```bash
   python expense-tracker.py update --id 1 --description "New description"
   ```

- **Delete an expense**:

   ```bash
   python expense-tracker.py delete --id 1
   ```

- **Export all expenses to a CSV file**:

   ```bash
   python expense-tracker.py export --filename my_expenses.csv
   ```

   If no filename is provided, it will default to `expenses.csv`.

## Project Structure

- `expense-tracker.py`: The main file that runs the CLI logic.
- `util.py`: A utility module containing functions to handle storage, loading, and operations on the expense data.

## Contributing

Contributions are welcome! If you have any improvements or fixes, feel free to fork the project and submit a pull request.


