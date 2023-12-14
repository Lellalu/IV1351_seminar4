import psycopg2
import integration

class Controller:

    def __init__(self, host, database, user, password):
        self.database_conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password)
        self.database_conn.autocommit = False
        self.database_cursor = self.database_conn.cursor()


    def get_avialable_instruments(self, instrument_kind):
        cursor = self.database_conn.cursor()
        instruments = integration.InstrumentDAO.read_available_instruments(
            cursor, instrument_kind)
        cursor.close()
        return instruments
    
    def student_rent_instrument(self, student_id, instrument_id):
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
        try:
            cursor = self.database_conn.cursor()

            rental = integration.RentalDAO.read_rental(cursor, rental_id)

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