import sqlite3

# Connection to sqlite
connection = sqlite3.connect("DTS.db")

# Create an object of cursor to perform CRUD operation
cursor = connection.cursor()

# Create the DB Table
table_info = """
Create table MAP(MAPKEY INT PRIMARY KEY,WARNING VARCHAR(6),DTC VARCHAR(4),FAILURE VARCHAR(2),CAUTION VARCHAR(100),SEVERITY INT)
"""
cursor.execute(table_info)

# Insert records into the table
cursor.execute('''Insert Into MAP values(1,'600E00','0000','00','Start Engine Alert', 1) ''')
cursor.execute('''Insert Into MAP values(2,'600E01','0001','01','Turn ON AC', 1) ''')
cursor.execute('''Insert Into MAP values(3,'600E02','0002','02','Check Side Indicator', 1) ''')
cursor.execute('''Insert Into MAP values(4,'600E03','0003','03','Turn On Headlight', 1) ''')
cursor.execute('''Insert Into MAP values(5,'600E10','0010','10','Oil Life Alert', 2) ''')
cursor.execute('''Insert Into MAP values(6,'600E11','0011','11','Tyre Slow Leak Alert', 2) ''')
cursor.execute('''Insert Into MAP values(7,'600E12','0012','12','Door Ajar Alert', 2) ''')
cursor.execute('''Insert Into MAP values(8,'600E13','0013','13','Bonnet Ajar Alert', 2) ''')
cursor.execute('''Insert Into MAP values(9,'600E20','0020','20','Vehicle Engine Damage ALert', 3) ''')
cursor.execute('''Insert Into MAP values(10,'600E21','0021','21','Drive Belt Distortion Alert', 3) ''')
cursor.execute('''Insert Into MAP values(11,'600E22','0022','22','Steering Wheel Malfunction Alert', 3) ''')
cursor.execute('''Insert Into MAP values(12,'600E23','0023','23','Battery Dead Alert', 3) ''')

# Displaying all the records
print("The inserted records from MAP table is : ")
data = cursor.execute('''Select * From MAP''')
for row in data:
    print(row)

# Close the connection
connection.commit()
connection.close()