import sqlite3

# Connection to sqlite
connection1 = sqlite3.connect("DTS.db")

# Create an object of cursor to perform CRUD operation
cursor1 = connection1.cursor()

# Create the DB Table
table_info = """
Create table LANG(LANGLOCALEKEY INT PRIMARY KEY,COUNTRY VARCHAR(4),LANGUAGE VARCHAR(4),LOCALE VARCHAR(6),MAPKEY INT)
"""
cursor1.execute(table_info)

# Insert records into the table
cursor1.execute('''Insert Into LANG values(1,'US','en','en-US', 1) ''')
cursor1.execute('''Insert Into LANG values(2,'CN','zh','zh-CN', 2) ''')
cursor1.execute('''Insert Into LANG values(3,'DE','de','de-DE', 3) ''')
cursor1.execute('''Insert Into LANG values(4,'FR','fr','fr-FR', 4) ''')
cursor1.execute('''Insert Into LANG values(5,'GB','en','en-GB', 5) ''')
cursor1.execute('''Insert Into LANG values(6,'ES','es','es-ES', 6) ''')
cursor1.execute('''Insert Into LANG values(7,'NL','nl','nl-NL', 7) ''')
cursor1.execute('''Insert Into LANG values(8,'IT','it','it-IT', 8) ''')
cursor1.execute('''Insert Into LANG values(9,'PL','pl','pl-PL', 9) ''')
cursor1.execute('''Insert Into LANG values(10,'IE','en','en-IE', 10) ''')
cursor1.execute('''Insert Into LANG values(11,'BE','nl','nl-BE', 11) ''')
cursor1.execute('''Insert Into LANG values(12,'BE','fr','fr-BE', 12) ''')
cursor1.execute('''Insert Into LANG values(13,'US','en','en-US', 12) ''')
cursor1.execute('''Insert Into LANG values(14,'CN','zh','zh-CN', 11) ''')
cursor1.execute('''Insert Into LANG values(15,'DE','de','de-DE', 10) ''')
cursor1.execute('''Insert Into LANG values(16,'FR','fr','fr-FR', 9) ''')
cursor1.execute('''Insert Into LANG values(17,'GB','en','en-GB', 8) ''')
cursor1.execute('''Insert Into LANG values(18,'ES','es','es-ES', 7) ''')
cursor1.execute('''Insert Into LANG values(19,'NL','nl','nl-NL', 6) ''')
cursor1.execute('''Insert Into LANG values(20,'IT','it','it-IT', 5) ''')
cursor1.execute('''Insert Into LANG values(21,'PL','pl','pl-PL', 4) ''')
cursor1.execute('''Insert Into LANG values(22,'IE','en','en-IE', 3) ''')
cursor1.execute('''Insert Into LANG values(23,'BE','nl','nl-BE', 2) ''')
cursor1.execute('''Insert Into LANG values(24,'BE','fr','fr-BE', 1) ''')


# Displaying all the records
print("The inserted records from LANG table is : ")
data = cursor1.execute('''Select * From LANG''')
for row in data:
    print(row)

# Close the connection
connection1.commit()
connection1.close()