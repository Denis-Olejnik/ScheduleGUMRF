import psycopg2 as ps
# from loguru import logger
import logging


def create_connection(host: str = None,
                      port: str = None,
                      db_name: str = None,
                      username: str = None,
                      password: str = None):
    """
    This function creates connection to database.

    :param host: Host name of database,
    :param port: Connection port,
    :param db_name: Database name,
    :param username: Username of database,
    :param password: User password
    :return: psycopg2.extensions.connection
    """
    db_connection = None

    _host = host or DB_HOST
    _port = port or DB_PORT
    _db_name = db_name or DB_NAME
    _username = username or DB_USER
    _password = password or DB_PASS

    try:
        db_connection = ps.connect(
            host=_host,
            port=_port,
            database=_db_name,
            user=_username,
            password=_password,
        )
        logging.info("[OPEN] Connection to PostgreSQL is successful!")
    except (Exception, ps.OperationalError) as error:
        logging.error(f"An error occurred: {error}")
    return db_connection


def execute_read_query(query: str = None):
    """
    Executes the read request.

    :param query: Request text
    :return: list of tuples [(content_id, author_id, ***), (content_id, author_id, ***)]
    """

    connection = create_connection()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        # logger.info(f'Read-request "{query}" completed successfully!')
        # logger.debug(f"Total rows count = {cursor.rowcount}")

        print(f'Read-request "{query}" completed successfully!')
        print(f"Total rows count = {cursor.rowcount}")
        return result

    except (Exception, ps.OperationalError) as error:
        # logger.error(error)
        print(error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            # logger.info("[CLOSED] Connection to PostgreSQL is successfully closed!")
            print("[CLOSED] Connection to PostgreSQL is successfully closed!")


def execute_write_query(data: tuple = None,
                              table: str = None,
                              columns: str = None) -> bool:
    """
    This function executes a write request to the database.

    :param data: Data to insert into a table;
    :param table: The table into which to insert data;
    :param columns: Columns to insert data.
    :return:

    Example of right request:
    "INSERT INTO user_content (author_id, content_rating, content_reports, content_sources)
    VALUES ('180061292', '10', '0', 'photo180061292_457253956')"
    """

    connection = create_connection()
    cursor = None
    try:
        if isinstance(data, tuple):
            query = f"INSERT INTO {table} ({columns}) VALUES {data}"
        else:
            # logger.warning(f"The type of 'data' ({type(data)}) is not a tuple! Request may contains an errors!")
            print(f"The type of 'data' ({type(data)}) is not a tuple! Request may contains an errors!")
            query = f"INSERT INTO {table} ({columns}) VALUES ({data})"

        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()

        # logger.info(f'Write-request "{query}" completed successfully!')
        print(f'Write-request "{query}" completed successfully!')
        return True
    except (Exception, ps.OperationalError) as error:
        # logger.error(error)
        print(error)
        return False
    finally:
        cursor.close()
        connection.close()
        # logger.info("[CLOSED] Connection to PostgreSQL is successfully closed!")
        print("[CLOSED] Connection to PostgreSQL is successfully closed!")