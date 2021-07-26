'''
This servers as the data layer
Features:
 - prevent SQL Injection
 - Error handling to catch and return error

'''

import mysql.connector

mydb = mysql.connector.connect(
  user='root',
  password="",
  database="classicmodels"
)
mycursor = mydb.cursor()


def get_customers(last_name, first_name):
  #list customers with able to search by first name, last name and order by credit limit
  customer_ls = []
  success = True
  error = ""
  try:
    # Alternative but not secure:
    #mycursor.execute(f"SELECT * FROM customers WHERE contactLastName='{last_name}' AND contactFirstName='{first_name}' ORDER BY creditLimit")
    
    # Preventing SQL Injection
    mycursor.execute("SELECT * FROM customers WHERE contactLastName=%s AND contactFirstName=%s ORDER BY creditLimit", (last_name,first_name))
    
    myresult = mycursor.fetchall()
    for i in myresult:
      customer_ls.append({
          "customerNumber":i[0],
          "customerName":i[1],
          "contactLastName":i[2],
          "contactFirstName":i[3],
          "phone":i[4],
          "addressLine1":i[5],
          "addressLine2":i[6],
          "city":i[7],
          "state":i[8],
          "postalCode":i[9],
          "country":i[10],
          "salesRepEmployeeNumber":i[11],
          "creditLimit":float(i[12]),
      })
  except mysql.connector.Error as err:
    error = "Something went wrong: {}".format(err)
    print(error)
    success = False
  return {"success":success, "error":error, "result":customer_ls}


def get_employees(last_name, first_name):
  # list employees with able to search by first name, last name and order by last name
  employee_ls = []
  success = True
  error = ""
  try:
    # Alternative but not secure:
    #mycursor.execute(f"SELECT * FROM employees WHERE lastName='{last_name}' AND firstName='{first_name}' ORDER BY lastName")
    
    # Preventing SQL Injection
    mycursor.execute("SELECT * FROM employees WHERE lastName=%s AND firstName=%s ORDER BY lastName",(last_name,first_name))
    myresult = mycursor.fetchall()
    for i in myresult:
      employee_ls.append({
          "employeeNumber":i[0],
          "lastName":i[1],
          "firstName":i[2],
          "extension":i[3],
          "email":i[4],
          "officeCode":i[5],
          "reportsTo":i[6],
          "jobTitle":i[7]
      })
  except mysql.connector.Error as err:
    error = "Something went wrong: {}".format(err)
    print(error)
    success = False
  return {"success":success, "error":error, "result":employee_ls}


def get_orders(last_name, first_name):
  #list orders with able to search by customer first name, last name and order by order date or customer last name
  order_ls = []
  success = True
  error = ""
  try:
    # Alternative but not secure:
    #mycursor.execute(f"SELECT orders.orderNumber,orders.orderDate,orders.requiredDate,orders.shippedDate,orders.status,orders.comments,orders.customerNumber FROM orders INNER JOIN customers ON orders.customerNumber=customers.customerNumber WHERE customers.contactLastName ='{last_name}' AND customers.contactFirstName='{first_name}' ORDER BY orders.orderDate, customers.contactLastName='{last_name}';")
    
    # Preventing SQL Injection
    mycursor.execute("SELECT orders.orderNumber,orders.orderDate,orders.requiredDate,orders.shippedDate,orders.status,orders.comments,orders.customerNumber FROM orders INNER JOIN customers ON orders.customerNumber=customers.customerNumber WHERE customers.contactLastName =%s AND customers.contactFirstName=%s ORDER BY orders.orderDate, customers.contactLastName=%s", (last_name,first_name,last_name))
    myresult = mycursor.fetchall()
    for i in myresult:
      order_ls.append({
          "orderNumber":i[0],
          "orderDate":i[1],
          "requiredDate":i[2],
          "shippedDate":i[3],
          "status":i[4],
          "comments":i[5],
          "customerNumber":i[6]
      })
  except mysql.connector.Error as err:
    error = "Something went wrong: {}".format(err)
    print(error)
    success = False
  return {"success":success, "error":error, "result":order_ls}
  

def create_product(product_code,product_name,product_line,product_scale,product_vendor,product_description,quantity_in_stock,buy_price,msrp):
  # create new product
  success = True
  error = ""
  try:
    # Alternative but not secure:
    #mycursor.execute(f"INSERT INTO products VALUES ('{product_code}','{product_name}','{product_line}','{product_scale}','{product_vendor}','{product_description}',{quantity_in_stock},'{buy_price}','{msrp}');")
    
    # Prevent SQL Injection
    statement = "INSERT INTO products VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(statement,(product_code,product_name,product_line,product_scale,product_vendor,product_description,quantity_in_stock,buy_price,msrp))

    mydb.commit() # Make sure data is committed to the database
  except mysql.connector.Error as err:
    error = "Something went wrong: {}".format(err)
    print(error)
    success = False
  return {"success":success, "error":error}


if __name__ =="__main__":
  print("get_customers")
  print(get_customers('Piestrzeniewicz', 'Zbyszek'))

  print("get_employees")
  print(get_employees('Bondur', 'Gerard'))

  print("get_orders")
  print(get_orders('Young','Dorothy'))

  print("create_product")
  print(create_product('S12_4484','1957 Roger','Trucks and Buses','1:12','Exoto Designs','1:12 scale die-cast about 20\" long Hood opens, Rubber wheels',6125,'55.70','118.50'))

