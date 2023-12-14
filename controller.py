import psycopg2
import integration

class Controller:
    """The controller class for calling methods from DAO."""

    def __init__(self, host, database, user, password):
        self.database_conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password)
        self.database_conn.autocommit = False
        self.database_cursor = self.database_conn.cursor()


    def get_available_instruments(self, instrument_kind):
        """Get available instruments based on the instrument kind.
        
        Args:
            instrument_kind: The instrument type as a string.

        Returns:
            The message to output in the view and the list of available instruments.
        """
        cursor = self.database_conn.cursor()
        instruments = integration.InstrumentDAO.read_available_instruments(
            cursor, instrument_kind)
        self.database_conn.commit()
        cursor.close()
        message = f'There are {len(instruments)} instruments'
        return message, instruments
    
    def student_rent_instrument(self, student_id, instrument_id):
        """Add rental for a student.

        In the function we first check if a student has rented more than two
        instruments, then we check if the instrument that the student want
        to rent is in stock. After that, we remove the instrument from stock
        if it is quantity is 1, or we decrease the quantity by 1. Finally, we
        add the rental information in the rental table.
        
        Args:
            student_id: The student id as a string.
            instrument_id: The rented instrument id as a string.

        Returns:
            The message to output in the view.
        """
        try:
            cursor = self.database_conn.cursor()
            num_rented_instrument_of_student = integration.InstrumentDAO.read_num_rented_instrument_of_student(cursor, student_id)
            if num_rented_instrument_of_student and num_rented_instrument_of_student[1] > 1:
                return f"Student with id {student_id} cannot rent more than two instruments."
            
            instrument_in_stock = integration.InstrumentDAO.read_if_instrument_is_available(cursor, instrument_id)
            if not instrument_in_stock:
                return f"Instrument with id {instrument_id} is not in stock."

            instrument_quantity = integration.InstrumentDAO.read_instrument_quantity(cursor, instrument_id)
            if int(instrument_quantity[0]) > 1:
                integration.InstrumentDAO.update_instrument_stock(cursor, instrument_id, -1)
            else:
                integration.InstrumentDAO.delete_instrument_from_stock(cursor, instrument_id)

            max_rental_id = integration.RentalDAO.read_max_rental_id(cursor)
            if not max_rental_id:
                max_rental_id = 1
            else:
                max_rental_id = max_rental_id[0]

            integration.RentalDAO.update_rental_with_new_rental(cursor, max_rental_id+1, student_id, instrument_id)

            self.database_conn.commit()
            cursor.close()
            return f"Student with id {student_id} has successfully rented instrument with id {instrument_id}"
        except psycopg2.DatabaseError as error:
            self.database_conn.rollback()
            return f"Caught DatabaseError when executing student_rent_instrument: {error}\nRolling back"
        except Exception as error:
            self.database_conn.rollback()
            return f"Caught Exception when executing student_rent_instrument: {error}\nRolling back"

    def terminate_rental(self, rental_id):
        """Terminate a rental.

        In the function we first check if there is a rental with this rental
        id. Then, we check if the returned instrument is in stock or not. If it
        is in stock, we simply increase the quantity by 1. Otherwise we insert
        a new instrument into the instrument_stock table. Finally, we terminate
        the rental by setting the end date to today.
        
        Args:
            rental_id: The rental id as a string.

        Returns:
            The message to output in the view.
        """
        try:
            cursor = self.database_conn.cursor()

            rental = integration.RentalDAO.read_rental(cursor, rental_id)
            if not rental:
                return f'There is no rental with id {rental_id}'

            instrument_id = integration.RentalDAO.read_instrument_id(cursor, rental_id)[0]

            instrument_in_stock = integration.InstrumentDAO.read_if_instrument_is_available(cursor, instrument_id)
            if not instrument_in_stock:
                max_stock_id = integration.InstrumentDAO.read_max_instrument_stock_id(cursor)[0]
                integration.InstrumentDAO.update_instrument_stock_by_insert(cursor, max_stock_id+1, instrument_id)
            else:
                integration.InstrumentDAO.update_instrument_stock(cursor, instrument_id, 1)

            integration.RentalDAO.update_rental_to_terminate(cursor, rental_id)
            self.database_conn.commit()
            cursor.close()
            return f"Rental with id {rental_id} has successfully terminated."
        except psycopg2.DatabaseError as error:
            self.database_conn.rollback()
            return f"Caught DatabaseError when executing update_rental_to_terminate: {error}\nRolling back"
        except Exception as error:
            self.database_conn.rollback()
            return f"Caught Exception when executing update_rental_to_terminate: {error}\nRolling back"
        
    def exit(self):
        self.database_conn.close()