'''
I failed to use peewee as ORE to access some table of the DB
since when using foregin key referring to another table, the extra Column
name of the column will be created and fail to access the Table
e.g.  officeCode from table Employees could be changed to officeCode.officeCode

To prevent this, usin library mysql.connector
but need to prevent SQL injection

'''

from peewee import * 
#from playhouse.pool import *
import json
import traceback
#from playhouse.shortcuts import model_to_dict, dict_to_model


db_name     = 'classicmodels'
db_username = 'root'
db_password = ''
db_port     = 3306

db = MySQLDatabase(db_name, user=db_username, passwd=db_password, port=db_port)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db

class Offices(BaseModel):
    officeCode = CharField(primary_key=True)
    city         = CharField(50)
    phone        = CharField(50)
    addressLine1 = CharField(50)
    addressLine2 = CharField(50)
    state        = CharField(50)
    country      = CharField(50)
    postalCode   = CharField(15)
    territory    = CharField(10)

class Employees(BaseModel):
    employeeNumber = PrimaryKeyField()
    lastName  = CharField(50)
    firstName = CharField(50)
    extension = CharField(10)
    email     = CharField(100)
    officeCode = ForeignKeyField(Offices)
    reportsTo = IntegerField()
    jobTitle  = CharField(50)

class Customers(BaseModel):
    customerNumber  = PrimaryKeyField()
    customerName    = CharField(50)
    contactLastName = CharField(50)
    contactFirstName= CharField(50)
    phone           = CharField(50)
    addressLine1    = CharField(50)
    addressLine2    = CharField(50)
    city            = CharField(50)
    state           = CharField(50)
    postalCode      = CharField(15)
    country         = CharField(50)
    salesRepEmployeeNumber = ForeignKeyField(Employees)
    creditLimit     = DecimalField()



# def initialize_database():
#     ######################  Composulory to be run when initialize the Database #######################
#     log.info(f'initialize_database')
#     db.create_tables([Record])   # create tables in DB if not exist
#     log.info(f"[Success] Tables created")

def get_office():
    find = Offices.select().where(Offices.city=='San Francisco')
    if len(find) == 1:
        postalCode = find[0].postalCode
    else:
        postalCode = "NOT FOUND"
        #raise ValueError(f"The city NOT exist")
    return postalCode

def get_office2():
    find = Offices.select().order_by(Offices.postalCode)
    office_list = []
    if len(find) > 0:
        for i in find:
            print(f"i:{i}")
            office = {
                'postalCode':i.postalCode,
                'officeCode':i.officeCode
            }
            office_list.append(office)
    
    return office_list


def get_customers(lastname,firstname):
    # return customer list with parameters firstname and lastname
    # return empty list if there is no matching records 
    # params - firstname:Schmitt, lastname:Carine
    # return 
    find = Customers.select().where(Customers.contactLastName==lastname,Customers.contactFirstName==firstname).order_by(Customers.creditLimit)
    customers_list = []
    if len(find) > 0:
        for i in find:
            print(f"i:{i}")
            customer_dict = {
                'customerNumber':i.customerNumber,
                'customerName':i.customerName,
                'contactLastName':i.contactLastName,
                'contactFirstName':i.contactFirstName,
                'phone':i.phone,
                'addressLine1':i.addressLine1,
                'addressLine2':i.addressLine2,
                'city':i.city,
                'state':i.state,
                'postalCode':i.postalCode,
                'country':i.country,
                #'salesRepEmployeeNumber':i.salesRepEmployeeNumber.employeeNumberd,
                'creditLimit': i.creditLimit
            }
            customers_list.append(customer_dict)
    
    return customers_list



'''
def create_record(data):
    log.info(f"DB.create_record: data - {data}")
    record = Record.create(Device_ID=data["device_id"],
                         Firstname=data["firstname"], 
                         Lastname=data["lastname"], 
                         Gender=data["gender"], 
                         Birthday=data["birthday"], 
                         Weight=data["weight"], 
                         Height=data["height"], 
                         Keto_Level=data["keto_level"], 
                         Start_Date=data["start_date"], 
                         Test_Date=data["test_date"], 
                         Test_Time=data["test_time"], 
                         Remark=data["remark"]
    )
    log.warning(f"record.R_ID: {record.R_ID}")


def get_records():
    log.info(f"DB.get_records")
    result = []
    query = Record.select()
    for i in query:
        item = {}
        item["record_id"] = i.R_ID
        item["device_id"] = i.Device_ID
        item["firstname"] = i.Firstname
        item["lastname"] = i.Lastname
        item["gender"] = i.Gender
        item["birthday"] = i.Birthday
        item["weight"] = i.Weight
        item["height"] = i.Height
        item["keto_level"] = i.Keto_Level
        item["start_date"] = i.Start_Date
        item["test_date"] = i.Test_Date
        item["test_time"] = i.Test_Time
        item["remark"] = i.Remark
        result.append(item)
    
    return result
'''


if __name__=="__main__":
    
    print(f"get_customers: {get_customers('Schmitt','Carine')}")
    #pass

# CREATE DATABASE keto CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;