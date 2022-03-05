import time

import psycopg2 as ps
from loguru import logger

from data.config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, DATABASE_URL


async def create_connection(host: str = None,
                            port: str = None,
                            db_name: str = None,
                            username: str = None,
                            password: str = None,
                            database_url: str = None,
                            sslmode: str = 'require'):
    """
    This function creates connection to database.

    :param host: Host name of database,
    :param port: Connection port,
    :param db_name: Database name,
    :param username: Username of database,
    :param password: User password
    :param database_url: URI Identifier
    :param sslmode: Is a secure connection required?
    """
    start_time = time.time()

    global db_connection, cursor

    _host = host or POSTGRES_HOST
    _port = port or POSTGRES_PORT
    _db_name = db_name or POSTGRES_DB
    _username = username or POSTGRES_USER
    _password = password or POSTGRES_PASSWORD
    _db_url = database_url or DATABASE_URL

    try:
        if _db_url:
            db_connection = ps.connect(_db_url)
        else:
            db_connection = ps.connect(
                host=_host,
                port=_port,
                database=_db_name,
                user=_username,
                password=_password,
                sslmode=sslmode
            )
        cursor = db_connection.cursor()
        execute_time = time.time() - start_time
        logger.info(f"Connection to PostgreSQL is successful! (in {str(execute_time)[:5]} sec)")

    except (Exception, ps.OperationalError) as error:
        logger.exception(f"An error occurred: {error}")


async def execute_read_query(query: str = None):
    """
    Executes the read request.
    :param query: Request text
    :return: list of tuples [(line1, line2), (line1, line2)]
    """
    start_time = time.time()
    try:
        logger.debug(f"Try to execute query: \"{query}\"")
        cursor.execute(query)
        result = cursor.fetchall()

        execute_time = time.time() - start_time
        logger.info(f'Read-request "{query}" completed successfully! (in {str(execute_time)[:5]} sec)')
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
    start_time = time.time()
    try:
        if not query:
            if isinstance(data, tuple):
                query = f"INSERT INTO {table} ({columns}) VALUES {data};"
            else:
                logger.warning(f"The type of 'data' ({type(data)}) is not a tuple! Request may contains an errors!")
                query = f"INSERT INTO {table} ({columns}) VALUES ({data};)"
        cursor.execute(query, data)
        db_connection.commit()

        execute_time = time.time() - start_time
        logger.info(f'Write-request "{query}" completed successfully! (in {str(execute_time)[:5]} sec)')
        return True
    except (Exception, ps.OperationalError) as error:
        logger.error(error)
        return False


async def execute_write_query_state(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO users VALUES %s)", tuple(data.values()))
        db_connection.commit()


async def is_user_registered(user_id: int) -> bool:
    """
    Is the user registered in the 'users' database?.

    :param user_id: user id from message
    :return: TRUE, if the user is found.
    """
    query = f"SELECT EXISTS(SELECT 1 FROM users WHERE user_id={user_id})"
    try:
        cursor.execute(query)
        result = cursor.fetchall()[0][0]
        return result
    except (Exception, ps.OperationalError, ps.DataError) as error:
        logger.exception(error)
        return False


async def get_groups(convert_to_str: bool = True):
    start_time = time.time()
    try:
        query = "SELECT DISTINCT group_code FROM schedule;"

        cursor.execute(query)
        user_groups_requested = cursor.fetchall()

        group_list = list()
        str_groups = str()

        # replace '_' with '-' and add it to list
        for item in user_groups_requested:
            group = item[0].split("_")
            group = group[0] + '-' + group[1]
            group_list.append(group)

            # Leave only unique values and sort alphabetically.
        else:
            group_list = list(set(group_list))
            group_list = sorted(group_list)

            # Prepare list items to print.
            if convert_to_str:
                for item in group_list:
                    str_groups += f"\n{item}"

        execute_time = time.time() - start_time
        logger.debug(f"Read request \"{query}\" completed successfully! (in {str(execute_time)[:5]} sec)")
        if convert_to_str:
            return str_groups
        else:
            return group_list
    except (ps.OperationalError, ps.DataError) as error:
        logger.exception(error)


async def get_user_schedule_for_day(user_group: str, week_day: str | int, fractional: int):
    fraction = None

    if int(fractional) == 0:
        fraction = "denominator"
    elif int(fractional) == 1:
        fraction = "numerator"

    query = f"SELECT schedule_{fraction} from schedule_new WHERE group_code = '{user_group}' and week_day='{week_day}'"

    logger.debug(f"Try to execute query: \"{query}\"")

    cursor.execute(query)
    result = cursor.fetchall()

    return result
