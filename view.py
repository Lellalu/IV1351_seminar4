import argparse
import getpass

from pprint import pprint


def cli_input():
    parser = argparse.ArgumentParser("The command line interface for soundGood")
    parser.add_argument('--host', 
                        help='The database host.')
    parser.add_argument('--database', 
                        help='The database name.')
    parser.add_argument('--user', 
                        help='The database user.')
    parser.add_argument('--query_type',
                        required=True,
                        choices=['list', 'rent', 'terminate'],
                        help='Choose between list, rent or terminate rentals.')
    parser.add_argument('--kind', 
                        help='The instrument kind when listing the instruments.')
    parser.add_argument('--student_id',
                        help='The student id when renting.')
    parser.add_argument('--instrument_id',
                        help='The instrument id when renting.')
    parser.add_argument('--rental_id',
                        help='The rental id when terminating.')
    args = parser.parse_args()

    password = getpass.getpass("Please enter the password for the database: ")
    return args, password


def output_instruments(instrument_list):
    for instrument in instrument_list:
        print(instrument)

def output_message(message):
    print(message)