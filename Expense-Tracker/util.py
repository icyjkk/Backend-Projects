import json
import csv

def load_expenses(show_message=True):
    try:
        with open("expenses.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        if show_message:
            print("No expenses found. Please add a expense first.")
        return []

def obtain_next_id(expenses):
    
    if not expenses:
        return 1  # Si no hay tareas, empezar desde 1
    else:
        # Obtener el ID máximo actual y sumar 1
        max_id = max(expense['id'] for expense in expenses)
        return max_id + 1

def save_expenses(expenses):
    with open("expenses.json", 'w') as file:
        json.dump(expenses, file, indent=4)

def format(expenses):

    # Imprimir encabezado
    print(f"{'ID':<5}{'Date':<12}{'Description':<15}{'Amount':>10}")
    print("#" * 42)

    # Imprimir cada entrada
    for expense in expenses:
        # Formatear el monto con signo de moneda
        amount_str = f"${expense['amount']}"
        # Imprimir la línea con formato
        print(f"{expense['id']:<5}{expense['date']:<12}{expense['description']:<15}{amount_str:>10}")

def add_ammount(expenses):
    return sum(expense['amount'] for expense in expenses)

def add_ammount_month(expenses,month):
    month_str = f"{month:02}"  # Formatear el mes como '08' para agosto, por ejemplo.
    filtered_expenses = [expense for expense in expenses if expense['date'][5:7] == month_str]
    return sum(expense['amount'] for expense in filtered_expenses)

def search_expense(id,expenses):
    # Buscar el expense con el id proporcionado
    expense_to_update = None

    for expense in expenses:
        if expense['id'] == id:
            expense_to_update = expense
            break

    return expense_to_update

def update_expense(args,expense_to_update):
    # Actualizar la descripción si se ha proporcionado
        if args.description:
            expense_to_update['description'] = args.description
        
        # Actualizar el amount si se ha proporcionado
        if args.amount is not None:
            if args.amount >= 0:
                expense_to_update['amount'] = args.amount
            else:
                print("Please add an amount equal to or greater than 0.")
                return

        return expense_to_update    

def export_csv(args,expenses):
    # Nombre del archivo CSV
    filename = args.filename or 'expenses.csv'

    # Definir los campos del CSV
    fieldnames = ['id', 'date', 'description', 'amount']

    # Escribir en el archivo CSV
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Escribir el encabezado
            writer.writeheader()

            # Escribir los gastos
            for expense in expenses:
                writer.writerow(expense)

        print(f"Expenses exported successfully to {filename}")
    except Exception as e:
        print(f"Failed to export expenses: {e}")
