import csv
from typing import Optional

from levenshtein_automata import replace_strings


def write_to_csv(filename: str, headers, rows, encoding: Optional[str] = None):
    with open(filename, mode="w", encoding=encoding, newline="") as csvfile:
        csv_writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=headers)
        csv_writer.writerow(dict((head, head) for head in headers))
        csv_writer.writerows(rows)


def read_csv(filename: str, encoding: Optional[str] = None):
    with open(filename, encoding=encoding, newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        headers = csv_reader.fieldnames
        rows = list(csv_reader)
    return headers, rows


def replace_csv_column(rows: list, column_name: str, new_column: list):
    new_rows = []
    for i, row in enumerate(rows):
        row[column_name] = new_column[i]
        new_rows.append(row)
    return new_rows


def main():
    print('Limpando arquivo "PakistanSuicideAttacks.csv" ...')

    headers, rows = read_csv("PakistanSuicideAttacks.csv", encoding="latin1")
    cities = [row["City"].lower().strip() for row in rows]
    new_rows = replace_csv_column(rows, "City", replace_strings(cities, distance=1))
    write_to_csv("PakistanSuicideAttacks_clean.csv", headers, new_rows, encoding="latin1")

    print('Limpando arquivo "ramen-ratings.csv" ...')

    headers, rows = read_csv("ramen-ratings.csv")
    brands = [row["Brand"].lower().strip() for row in rows]
    new_rows = replace_csv_column(rows, "Brand", replace_strings(brands, distance=2))
    write_to_csv("ramen-ratings_clean.csv", headers, new_rows)


if __name__ == "__main__":
    main()
