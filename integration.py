import model

from dateutil.relativedelta import relativedelta
from datetime import datetime

class InstrumentDAO:
    @staticmethod
    def read_available_instruments(database_cursor, instrument_kind):
        query = f"""\
SELECT instrument.id, instrument.brand, instrument.rented_price_per_month
FROM instrument_stock
LEFT JOIN instrument ON instrument_stock.instrument_id = instrument.id
WHERE instrument.type = '{instrument_kind}'
"""
        database_cursor.execute(query)
        result = database_cursor.fetchall()
        instrument_list = []
        for res in result:
            instrument_list.append(model.Instrument(*res))
        return instrument_list
    
    @staticmethod
    def read_num_rented_instrument_of_student(database_cursor, student_id):
        num_instrument_query = f"""\
SELECT student_id, count(*)
FROM rental
WHERE student_id = {student_id}
GROUP BY student_id
"""
        database_cursor.execute(num_instrument_query)
        return database_cursor.fetchone()
    
    @staticmethod
    def read_if_instrument_is_available(database_cursor, instrument_id):
        instrument_is_available_query = f"""\
SELECT *
FROM instrument_stock
WHERE instrument_id = {instrument_id}
"""
        database_cursor.execute(instrument_is_available_query)
        return database_cursor.fetchone()
    
    @staticmethod
    def read_instrument_quantity(database_cursor, instrument_id):
        select_instrument_for_update_query = f"""\
SELECT quantity FROM instrument_stock WHERE instrument_stock.instrument_id = {instrument_id} FOR UPDATE
"""
        database_cursor.execute(select_instrument_for_update_query)
        return database_cursor.fetchone()
    
    @staticmethod
    def delete_instrument_from_stock(database_cursor, instrument_id):
        delete_instrument_query = f"""\
DELETE FROM
instrument_stock
WHERE instrument_stock.instrument_id = {instrument_id}
"""
        database_cursor.execute(delete_instrument_query)

    @staticmethod
    def update_instrument_stock(database_cursor, instrument_id, update_number):
        decrease_instrument_stock_query = f"""\
UPDATE instrument_stock
SET quantity = CAST(CAST(quantity AS INTEGER) + {update_number} AS VARCHAR(10))
WHERE instrument_stock.instrument_id = {instrument_id}
"""
        database_cursor.execute(decrease_instrument_stock_query)

        


class RentalDAO:
    @staticmethod
    def read_max_rental_id(database_cursor):
        read_max_rental_id_query = """\
SELECT id
FROM rental
ORDER BY id DESC
LIMIT 1
"""
        database_cursor.execute(read_max_rental_id_query)
        return database_cursor.fetchone()

    @staticmethod
    def update_rental_with_new_rental(database_cursor, rental_id, student_id, instrument_id):
        insert_new_rental_query = f"""\
INSERT INTO rental (id, start_date, end_date, instrument_id, student_id, rental_policy_id)
VALUES ({rental_id},
        '{datetime.today().strftime('%Y-%m-%d')}',
        '{(datetime.today() + relativedelta(months=12)).strftime('%Y-%m-%d')}',
        {instrument_id},
        {student_id},
        1)
"""
        database_cursor.execute(insert_new_rental_query)

    @staticmethod
    def read_rental(database_cursor, rental_id):
        read_rental_end_date_query = f"""\
SELECT * FROM rental WHERE id = {rental_id} FOR UPDATE
"""
        database_cursor.execute(read_rental_end_date_query)
        result = database_cursor.fetchone()
        return model.Rental(id=int(result[0]),
                            start_date=result[1],
                            end_date=result[2],
                            instrument_id=int(result[3]),
                            student_id=int(result[4]),
                            rental_policy_id=int(result[5]))

    @staticmethod
    def update_rental_to_terminate(database_cursor, rental_id):
        update_rental_to_terminate_query = f"""\
UPDATE rental
SET end_date = '{datetime.today().strftime('%Y-%m-%d')}'
WHERE id = {rental_id}
"""
        database_cursor.execute(update_rental_to_terminate_query)
        
    

        

        
