import psycopg2 as ps
from _distutils_hack import override
from loguru import logger

from data.config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_URI

global db_connection, cursor


async def create_connection(host: str = None,
                            port: str = None,
                            db_name: str = None,
                            username: str = None,
                            password: str = None,
                            database_uri: str = None,
                            sslmode: str = 'require'):
    """
    This function creates connection to database.

    :param host: Host name of database,
    :param port: Connection port,
    :param db_name: Database name,
    :param username: Username of database,
    :param password: User password
    :param database_uri: URI Identifier
    :param sslmode: Is a secure connection required?
    """
    global db_connection, cursor

    _host = host or POSTGRES_HOST
    _port = port or POSTGRES_PORT
    _db_name = db_name or POSTGRES_DB
    _username = username or POSTGRES_USER
    _password = password or POSTGRES_PASSWORD
    _db_uri = database_uri or POSTGRES_URI

    try:
        db_connection = ps.connect(
            host=_host,
            port=_port,
            database=_db_name,
            user=_username,
            password=_password,
            sslmode=sslmode
        )
        cursor = db_connection.cursor()

        logger.info("Connection to PostgreSQL is successful!")
    except (Exception, ps.OperationalError) as error:
        logger.exception(f"An error occurred: {error}")


async def execute_read_query(query: str = None):
    """
    Executes the read request.
    :param query: Request text
    :return: list of tuples [(line1, line2), (line1, line2)]
    """

    try:
        logger.debug(f"Try to execute query: \"{query}\"")
        cursor.execute(query)
        result = cursor.fetchall()

        logger.info(f'Read-request "{query}" completed successfully!')
        logger.debug(f"Total rows count = {cursor.rowcount}")

        return result

    except (Exception, ps.OperationalError) as error:
        logger.error(error)


async def execute_write_query(table: str = None,
                              data: tuple = None,
                              columns: str = None,
                              query: str = None) -> bool:
    """
    This function executes a write request to the database.
    :param table: The table into which to insert data;
    :param data: Data to insert into a table;
    :param columns: Columns to insert data;
    :param query: full line request;
    :return: bool

        Example of right request:
    "INSERT INTO users (user_id, data_1, ..., ) VALUES ('01234', 'some_data_1', ...,)"
    """
    try:
        if not query:
            if isinstance(data, tuple):
                query = f"INSERT INTO {table} ({columns}) VALUES {data};"
            else:
                logger.warning(f"The type of 'data' ({type(data)}) is not a tuple! Request may contains an errors!")
                query = f"INSERT INTO {table} ({columns}) VALUES ({data};)"

        cursor.execute(query, data)
        db_connection.commit()

        logger.info(f'Write-request "{query}" completed successfully!')
        return True
    except (Exception, ps.OperationalError) as error:
        logger.error(error)
        return False


async def execute_write_query_state(state):
    async with state.proxy() as data:
        print(tuple(data.values()))
        cursor.execute("INSERT INTO users VALUES %s)", tuple(data.values()))
        db_connection.commit()
