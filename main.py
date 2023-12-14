"""
The main file calling the controller and the view to handle
all user input and output.

Example usage:
python3 main.py --host localhost --database soundgoods4 --user postgres \
    --query_type list --kind Violin
"""


import controller
import view

def main():
    args, password = view.cli_input()

    contr = controller.Controller(args.host, args.database, args.user, password)

    if args.query_type == 'list':
        message, instruments = contr.get_available_instruments(args.kind)
        view.output_message(message)
        view.output_instruments(instruments)
    elif args.query_type == 'rent':
        message = contr.student_rent_instrument(args.student_id, args.instrument_id)
        view.output_message(message)
    elif args.query_type == 'terminate':
        message = contr.terminate_rental(args.rental_id)
        view.output_message(message)

    contr.exit()

if __name__ == "__main__":
    main()