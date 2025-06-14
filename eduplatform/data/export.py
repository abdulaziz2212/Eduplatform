import csv
import os
from openpyxl import Workbook
from datetime import datetime

def export_to_csv(data, headers, filename):
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", f"{filename}.csv")
    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    return path

def export_to_xlsx(data, headers, filename):
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", f"{filename}.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.title = filename
    ws.append(headers)
    for row in data:
        ws.append([row.get(h, "") for h in headers])
    wb.save(path)
    return path

def export_to_sql(data, table_name, filename):
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", f"{filename}.sql")
    with open(path, mode="w", encoding="utf-8") as f:
        # Optional: generate CREATE TABLE (simplified)
        columns = ", ".join([f"{k} TEXT" for k in data[0].keys()])
        f.write(f"CREATE TABLE {table_name} ({columns});\n")
        for row in data:
            keys = ", ".join(row.keys())
            values = ", ".join([f"'{str(v)}'" for v in row.values()])
            f.write(f"INSERT INTO {table_name} ({keys}) VALUES ({values});\n")
    return path

