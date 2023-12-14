import controller
import view

def main():
    args, password = view.cli_input()

    contr = controller.Controller("localhost", "soundgoods4", "postgres", "1404852")

    if args.type == 'list':
        instruments = contr.get_avialable_instruments(args.kind)
        view.output_row_result(instruments)
    elif args.type == 'rent':
        message = contr.student_rent_instrument(args.student_id, args.instrument_id)
        view.output_message(message)
    elif args.type == 'terminate':
        message = contr.terminate_rental(args.rental_id)
        view.output_message(message)

    contr.exit()

if __name__ == "__main__":
    main()