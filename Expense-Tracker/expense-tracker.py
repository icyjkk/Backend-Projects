import argparse
import util
from datetime import datetime

def add_command(args):

    if(args.amount>=0):
        expenses = util.load_expenses(show_message=False)
        new_id = util.obtain_next_id(expenses)
        new_expense = {
            "id": new_id, 
            "date": datetime.now().strftime('%Y-%m-%d'),
            "description": args.description,  
            "amount": args.amount,  
        }
        expenses.append(new_expense) 
        util.save_expenses(expenses) 
        print(f"Expense added successfully (ID: {new_id})")
    else:
        print("Please add an amount equal to or greater than 0")

def list_command(args):

    expenses = util.load_expenses(show_message=True)  
    if not expenses:
        return
    
    util.format(expenses)

def summary_command(args):

    expenses = util.load_expenses(show_message=True)  
    if not expenses:
        return
    
    if args.month:
        summary = util.add_ammount_month(expenses,args.month)
        print(f"Total expenses for month {args.month}: ${summary}")
    else:
        summary=util.add_ammount(expenses)
        print(f"Total expenses: ${summary}")

def delete_command(args):
    expenses = util.load_expenses(show_message=True)  
    if not expenses:
        return
    
    expense_to_delete = util.search_expense(args.id, expenses)

    if expense_to_delete:
        expenses.remove(expense_to_delete)
        util.save_expenses(expenses)
        print(f"Expense ID {args.id} deleted successfully.")
    else:
        print(f"Expense with ID {args.id} not found.")

def update_command(args):
    expenses = util.load_expenses(show_message=True)
    if not expenses:
        return

    expense_to_update = util.search_expense(args.id, expenses)

    if expense_to_update:
        expense_to_update=util.update_expense(args,expense_to_update)
        util.save_expenses(expenses)
        if(expense_to_update!=None):
            print(f"Expense ID {args.id} updated successfully.")
    else:
        print(f"Expense with ID {args.id} not found.")

def export_command(args):
    expenses = util.load_expenses(show_message=True)
    if not expenses:
        print("No expenses to export.")
        return

    util.export_csv(args,expenses)

def main():
    # Crear el parser principal
    parser = argparse.ArgumentParser(description="Expense tracker CLI")

    # Crea un conjunto de subcomandos
    subparsers = parser.add_subparsers(title='Comandos', description='Comandos disponibles', dest='comando')

    # Comando add
    parser_add = subparsers.add_parser('add', help='Users can add an expense with a description and amount.')
    parser_add.add_argument('--description', type=str, help='Expense description', required=True)
    parser_add.add_argument('--amount', type=int, help='Expense amount', required=True)
    parser_add.set_defaults(func=add_command)

    # Comando list
    parser_list = subparsers.add_parser('list', help='Users can view all expenses.')
    parser_list.set_defaults(func=list_command)

    # Comando summary
    parser_summary = subparsers.add_parser('summary', help='Show summary of expenses')
    parser_summary.add_argument('--month', type=int, help='Month to filter expenses by (1-12)')
    parser_summary.set_defaults(func=summary_command)

    # Comando delete
    parser_delete = subparsers.add_parser('delete', help='Users can delete an expense.')
    parser_delete.add_argument('--id', type=int, help='Expense id', required=True)
    parser_delete.set_defaults(func=delete_command)

    # Comando update
    parser_update = subparsers.add_parser('update', help='Users can update an expense description or amount.')
    parser_update.add_argument('--id', type=int, help='Expense ID to update', required=True)
    parser_update.add_argument('--description', type=str, help='New description for the expense')
    parser_update.add_argument('--amount', type=int, help='New amount for the expense')
    parser_update.set_defaults(func=update_command)

    # Comando export
    parser_export = subparsers.add_parser('export', help='Export all expenses to a CSV file.')
    parser_export.add_argument('--filename', type=str, help='Filename for the CSV file (default: expenses.csv)')
    parser_export.set_defaults(func=export_command)

    # Parsear los argumentos
    args = parser.parse_args()

    if args.comando:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
