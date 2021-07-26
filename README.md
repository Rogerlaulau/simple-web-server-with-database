# Tasks:

## LCJG-Backend-Engineer-Test
Backend engineer interview test for LCJG and you need to finish it within 24 hours.

**Task 1 :**
Follow the steps to setup a mysql database in local
- Install docker desktop and docker-compose (https://www.docker.com/products/docker-desktop)
- Download the [database.zip](https://raw.githubusercontent.com/ayking/LCJG-Backend-Engineer-Test/master/database.zip)
- Run the following command inside the folder to start database ```docker-compose  up --build --force-recreate --renew-anon-volumes db```

**Task 2 :**
You can use any *python* server framwork to implement a simple web server with the following routes (using the database in task 1)
- Route 1 - list customers with able to search by first name, last name and order by credit limit
- Route 2 - list employees with able to search by first name, last name and order by last name
- Route 3 - list orders with able to search by customer first name, last name and order by order date or customer last name
- Route 4 - create new product

After you finsih the test please zip them all to a single file and email to alanyu@lcjgroup.com


# My Solution:
using mysql.connector as ORM to access database   
using Flask as python server framwork     

scripts needed: **connect_DB.py** and **web_service.py**  

#### In data layer (connect_DB.py)
Features:   
 - prevent SQL Injection
 - Error handling to catch and return error


#### In presentation layer (web_service.py)

Route 1 - list customers with able to search by first name, last name and order by credit limit   
Route 2 - list employees with able to search by first name, last name and order by last name   
Route 3 - list orders with able to search by customer first name, last name and order by order date or customer last name   
Route 4 - create new product   

Features:   
 - basic authorization
 - support 20 concurrent queries
 - support cross origin resource sharing
 - error handling e.g. requested URL not found

To run the web service:   
```
python3 web_service.py
```



#### to do the testing with following data in json:
Basic Authorization:     
    - username: rogerlau   
    - password: rogerlau   


http://IP:8080/status with Method GET


http://IP:8080/get_customer with Method POST
```
{
	"last_name":"Piestrzeniewicz", 
	"first_name":"Zbyszek"
}
```


http://IP:8080/get_employee with Method POST
```
{
	"last_name":"Bondur", 
	"first_name":"Gerard"
}
```


http://IP:8080/get_order with Method POST
```
{
	"last_name":"Young", 
	"first_name":"Dorothy"
}
```


http://IP:8080/create_product with Method POST
```
{
    "product_code":"S12_4489", 
    "product_name":"1957 Roger",
    "product_line":"Trucks and Buses",
    "product_scale":"1:12",
    "product_vendor":"Exoto Designs",
    "product_description":"1:12 scale die-cast about 20\" long Hood opens, Rubber wheels",
    "quantity_in_stock":5262,
    "buy_price":"55.70",
    "msrp":	"118.50"
}
```


To know more about SQL Injection:

https://www.w3schools.com/sql/sql_injection.asp
https://blog.sqreen.com/preventing-sql-injections-in-python/


https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
```
from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector

cnx = mysql.connector.connect(user='scott', database='employees')
cursor = cnx.cursor()

tomorrow = datetime.now().date() + timedelta(days=1)

add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")
add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

# Insert new employee
cursor.execute(add_employee, data_employee)
emp_no = cursor.lastrowid

# Insert salary information
data_salary = {
  'emp_no': emp_no,
  'salary': 50000,
  'from_date': tomorrow,
  'to_date': date(9999, 1, 1),
}
cursor.execute(add_salary, data_salary)

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()
```
if there is NO .commit(), then your insertion to create new records will NOT take effect





Error handling using mysql.connector as ORM
https://dev.mysql.com/doc/connector-python/en/connector-python-api-errors-error.html
```
import mysql.connector

try:
  cnx = mysql.connector.connect(user='scott', database='employees')
  cursor = cnx.cursor()
  cursor.execute("SELECT * FORM employees")   # Syntax error in query
  cnx.close()
except mysql.connector.Error as err:
  print("Something went wrong: {}".format(err))
```