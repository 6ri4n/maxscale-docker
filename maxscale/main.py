# brian huang
# 2/12/23
# CNE370
#
# a python script that will communicate with a maxscale instance
#
# the script will retrieve the following:
# - the last 10 rows of zipcodes_one
# - the first 10 rows of zipcodes_two
# - the largest zipcode in zipcodes_one
# - the smallest zipcode in zipcodes_two
#
# the output of each query will be printed to the console

import mysql.connector


def connect_to_db():
    con = mysql.connector.connect(
        user = 'maxuser',
        password = 'maxpwd',
        host = '172.18.0.4',
        port = '4000'
    )
    return con

def query(cursor, query):
    cursor.execute(query)
    return cursor

def parse(data):
    for row in data:
        print(row)

def main():
    zipcode_db_con = connect_to_db()
    zipcode_db_cursor = zipcode_db_con.cursor()

    print('connection: started\n')

    print('1. Retrieve the last 10 rows of data from the zipcodes_one shard.\n')
    query_statement = "SELECT * FROM zipcodes_one.zipcodes_one ORDER BY Zipcode DESC, Zipcode ASC LIMIT 10;"
    retrieved_data = query(zipcode_db_cursor, query_statement).fetchall()
    parse(sorted(retrieved_data, key = lambda x:x[0]))

    print('\n2. Retrieve the first 10 rows of data from the zipcodes_two shard.\n')
    query_statement = "SELECT * FROM zipcodes_two.zipcodes_two ORDER BY Zipcode LIMIT 10;"
    retrieved_data = query(zipcode_db_cursor, query_statement).fetchall()
    parse(retrieved_data)

    print('\n3. Find the largest zipcode value in the zipcodes_one shard.\n')
    query_statement = "SELECT MAX(zipcode) FROM zipcodes_one.zipcodes_one;"
    retrieved_data = query(zipcode_db_cursor, query_statement).fetchall()
    parse(retrieved_data)

    print('\n4. Find the smallest zipcode value in the zipcodes_two shard.\n')
    query_statement = "SELECT MIN(zipcode) FROM zipcodes_two.zipcodes_two;"
    retrieved_data = query(zipcode_db_cursor, query_statement).fetchall()
    parse(retrieved_data)

    zipcode_db_cursor.close()
    zipcode_db_con.close()

    print('\nconnection: ended')


if __name__ == '__main__':
    main()