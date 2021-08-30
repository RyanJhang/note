
import os

import sqlite3

import pandas as pd
folder_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(folder_path, "circle_value.db")


class Column(dict):
    barcode = []
    xy = []


def select_x_y_from_local_db():
    db_conn = sqlite3.connect(db_path)
    c = db_conn.cursor()

    column = Column()
    for row in c.execute('SELECT barcode, x, y FROM CircleValue'):
        barcode, x, y = row
        if x is None or y is None or str(x).strip() == '' or str(y).strip() == '':
            raise Exception('Lens Barcode:{} ,x: {}, y: {}'.format(barcode, x, y))

        column.barcode.append(barcode)
        column.xy.append(f"{x},{y}")

    return column


def save_as_excel(column):
    # dataframe columns
    df = pd.DataFrame({'barcode': column.barcode,
                       'xy': column.xy})

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    xlsx_path = os.path.join(folder_path, "circle_value.xlsx")
    writer = pd.ExcelWriter(xlsx_path, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


if __name__ == "__main__":
    column = select_x_y_from_local_db()
    save_as_excel(column)
