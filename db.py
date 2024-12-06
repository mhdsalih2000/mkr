from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, insert,update


def create_row(session, imei, column_value_map, table_name='pump_data'):
    try:
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=session.bind)
        if 'imei' not in table.columns:
            raise ValueError(f"Column 'imei' does not exist in the table '{table_name}'.")
        existing_row = session.execute(
            table.select().where(table.c.imei == imei)
        ).fetchone()

        if existing_row:
            return dict(existing_row._mapping)
        new_row_data = {"imei": imei}
        for column_name, value in column_value_map.items():
            if column_name in table.columns:
                new_row_data[column_name] = value
            else:
                raise ValueError(f"Column '{column_name}' does not exist in the table '{table_name}'.")
        insert_query = insert(table).values(new_row_data)
        session.execute(insert_query)
        session.commit()
        created_row = session.execute(
            table.select().where(table.c.imei == imei)
        ).fetchone()
        return dict(created_row._mapping) if created_row else None
    except Exception as e:
        raise e  



def update_row(session, imei, column_value_map, table_name='pump_data'):
    try:
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=session.bind)

        if 'imei' not in table.columns:
            raise ValueError(f"Column 'imei' does not exist in the table '{table_name}'.")

        existing_row = session.execute(
            table.select().where(table.c.imei == imei)
        ).fetchone()

        if existing_row:
            update_query = table.update().where(table.c.imei == imei)
            for column_name, value in column_value_map.items():
                if column_name in table.columns:
                    update_query = update_query.values({column_name: table.c[column_name] + value})
                else:
                    raise ValueError(f"Column '{column_name}' does not exist in the table '{table_name}'.")
            session.execute(update_query)
            session.commit()
            updated_row = session.execute(
                table.select().where(table.c.imei == imei)
            ).fetchone()
            return dict(updated_row._mapping) if updated_row else None

        return None
    except Exception as e:
        raise e  






def reset_column_values_to_zero(session, columns = ["day_run_hours", "daily_water_discharge"] , imei=None , table_name='pump_data'):
    try:
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=session.bind)
        for column in columns:
            if column not in table.columns:
                raise ValueError(f"Column '{column}' does not exist in table '{table_name}'.")
        update_query = table.update()
        if imei is not None:
            condition = table.c.imei == imei
            update_query = update_query.where(condition)
        for column in columns:
            update_query = update_query.values({column: 0})
        session.execute(update_query)
        session.commit()
        print(f"Successfully reset columns {columns} to 0 in table '{table_name}'.")
    except Exception as e:
        session.rollback()
        print(f"Error resetting columns {columns} in table '{table_name}': {e}")




def establish_db_connection(host="localhost", username="postgres", password="root",
                            port=5432, db_name="mecwindb"):
    try:
        url = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"
        engine = create_engine(url)
        Session = sessionmaker(bind=engine)
        session = Session()
        print("Database connection established successfully.")
        return engine, session
    except Exception as e:
        print(f"Error establishing connection: {e}")
        return None, None



def get_column_values_by_imei(session,  imei, columns= ["day_run_hours", "cumulative_run_hours"] ,table_name='pump_data'):
    try:
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=session.bind)

        for column in columns:
            if column not in table.columns:
                raise ValueError(f"Column '{column}' does not exist in the table '{table_name}'.")

        selected_columns = [table.c[column] for column in columns]
        query = table.select().with_only_columns(*selected_columns).where(table.c.imei == imei)
        result = session.execute(query).fetchone()
        return dict(result._mapping) if result else None

    except Exception as e:
        print(f"Error fetching column values for imei '{imei}' from table '{table_name}': {e}")
        return None


