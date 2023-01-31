from datetime import datetime
from faker import Faker


def fill_list(columns, rows):
    fake = Faker()
    row_list = []
    for _ in range(rows):
        value_list = []
        for column in columns:
            int_from = column.int_from if type(column.int_from) == int else 0
            int_to = column.int_to if type(column.int_to) == int else 0
            type_dict = {
                "Full name": fake.name(),
                "Job": fake.job(),
                "Email": fake.email(),
                "Domain name": fake.domain_name(),
                "Phone number": fake.phone_number(),
                "Text": fake.text(),
                "Integer": fake.random_int(int_from, int_to),
                "Address": fake.address(),
                "Date": fake.date(),
            }
            value_list.append(type_dict[column.column_type])
        row_list.append(value_list)
    return row_list


def format_date(date_):
    return "-" if not date_ else datetime.strftime(date_, "%d/%m/%Y %H:%M:%S")
