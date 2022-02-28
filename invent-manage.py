from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.core.window import Window
import mysql.connector
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp




class MainWindow(Screen):
    #Variables for the Product TextInput
    productid= ObjectProperty(None)
    productname= ObjectProperty(None)
    quantity= ObjectProperty(None)
    description= ObjectProperty(None)
    category= ObjectProperty(None)

    #Variables for Customers Textinput
    custname= ObjectProperty(None)
    custid= ObjectProperty(None)
    phone= ObjectProperty(None)

    #Variables for Orders TextInput
    orderid= ObjectProperty(None)
    orderdate= ObjectProperty(None)
    prodid= ObjectProperty(None)
    custido= ObjectProperty(None)
    qty= ObjectProperty(None)
    price= ObjectProperty(None)    


    def submit_for_product(self):


        mydb =mysql.connector.connect(
            host= "localhost",
            user = "root",
            passwd = "your_password",
            database="your_database"
            
        )

        c = mydb.cursor()

        #Add a record
        sql_command= "INSERT INTO product(product_id,product_name,quantity,description,category) VALUES (%s,%s,%s,%s,%s)"
        values=(self.productid.text,self.productname.text,
        self.quantity.text,self.description.text,
        self.category.text)

        
        

        c.execute(sql_command,values)


      

        #Add a little message
        # self.ids.main_label.text = f'Data Added'
        #Clear the Input
        self.productid.text = ''
        self.productname.text= ''
        self.quantity.text =''
        self.description.text=''
        self.category.text=''

        # print("Product id: ",self.productid.text,"Product Name: ",self.productname.text,"Quantity: ",self.quantity.text)
        # print(type(self.productid.text))
        # num = int(self.productid.text)
        # print(type(num))


        #Commit our changes
        mydb.commit()

        #Close the connection
        mydb.close()



    def submit_for_customer(self):
        
        mydb =mysql.connector.connect(
            host= "localhost",
            user = "root",
            passwd = "strongone@123",
            database="inventory_management"
        )

        c = mydb.cursor()

        #Add a record
        sql_command= "INSERT INTO customers(customer_id,customer_name,phone_no) VALUES (%s,%s,%s)"
        values=(self.custid.text,self.custname.text,self.phone.text
       )
        

        c.execute(sql_command,values)


      

        #Add a little message
        # self.ids.cust_label.text = f'Data Added'
        #Clear the Input
        self.custid.text = ''
        self.custname.text= ''
        self.phone.text =''
      



        #Commit our changes
        mydb.commit()

        #Close the connection
        mydb.close()

    
    def submit_for_order(self):
        
        mydb =mysql.connector.connect(
            host= "localhost",
            user = "root",
            passwd = "strongone@123",
            database="inventory_management"
        )

        c = mydb.cursor()

        #Add a record
        sql_command= "INSERT INTO orders(orderid,order_date,product_id,customer_id,qty,price,total) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        self.total =str( int(self.qty.text) * float(self.price.text))
        values=(self.orderid.text,self.orderdate.text,self.prodid.text,self.custido.text,self.qty.text,self.price.text,self.total)
        

        c.execute(sql_command,values)


      

        
        #Clear the Input
        self.orderid.text = ''
        self.orderdate.text= '1992-01-22'
        self.prodid.text =''
        self.custido.text =''
        self.qty.text =''
        self.price.text=''



      



        #Commit our changes
        mydb.commit()

        #Close the connection
        mydb.close()


class SecondWindow(Screen):
    pass

class ThirdWindow(Screen):
    pass

class FourthWindow(Screen):
    pass

class FifthWindow(Screen):
    pass
   



class WindowManager(ScreenManager):
    pass




class MainApp(MDApp):



    def build(self):
        #Window.clearcolor = (0.76,0.71,0.46,0.8)
        # self.theme_cls.theme_style="Light"
        # self.theme_cls.primary_palette="BlueGray"
        mydb =mysql.connector.connect(
            host= "localhost",
            user = "root",
            passwd = "strongone@123",
            database="inventory_management"
        )

        c = mydb.cursor()

        c.execute("CREATE DATABASE IF NOT EXISTS inventory_management")

        # c.execute("SHOW DATABASES")
        # for db in c:
        #     print(db)        
        # return ProductModule()

        #Create Table product
        c.execute("""CREATE TABLE if not exists product(
            product_id varchar(10) primary key,
            product_name varchar(50) Not NULL,
            quantity int,
            description varchar(150),
            category varchar(20) constraint category_const CHECK(category IN('Stationary','Food','Garment','Footwear'))
        )""")
        #Create Table Customers
        c.execute("""CREATE TABLE if not exists customers(
            customer_id varchar(10) primary key,
            customer_name varchar(50) not null,
            phone_no int
        )""")

        #Create Table Orders
        c.execute("""CREATE TABLE if not exists orders(
            orderid varchar(10) primary key,
            order_date date not null,
            product_id varchar(10),
            customer_id varchar(10),
            qty int not null,
            price float not null,
            total float not null,
            Foreign Key(product_id) references product(product_id),
            Foreign Key(customer_id) references customers(customer_id)

        )""")

        #Commit our changes
        mydb.commit()

        #Close the connection
        mydb.close()


        return Builder.load_file('layout.kv')


    def connect_and_grab_database(self,query):
        #################Connecting to Database##########################
        self.mydb =mysql.connector.connect(
            host= "localhost",
            user = "root",
            passwd = "strongone@123",
            database="inventory_management"
            
        )
        self.query =query

        self.mycursor = self.mydb.cursor()

        self.mycursor.execute(self.query)

        self.myresult=self.mycursor.fetchall()

        self.data_fetched=[]

        for row in self.myresult:
            self.data_fetched.append(row)
        
        return self.data_fetched





        ###############################################################

    def add_datatable(self):

        self.data_fetched = MainApp().connect_and_grab_database("select * from product")
        # print(self.data_fetched)
        self.table =MDDataTable(
            size_hint=(1,1),
            rows_num=200,
            # pos_hint={'center_x':0.5,'center_y':0.5},
            check=True,
            column_data = [
                ("Product Id",dp(30)),
                ("Product Name",dp(30)),
                ("Quantity",dp(30)),
                ("Descrption",dp(30)),
                ("Category",dp(30))
            ],
            row_data=self.data_fetched

    
            )
        #Add table widget
        self.root.ids.data_scr.ids.data_layout.add_widget(self.table)

    def add_datatable_cust(self):
        self.data_fetched = MainApp().connect_and_grab_database("select * from customers")
        print(self.data_fetched)
        self.table =MDDataTable(
            size_hint=(1,1),
            rows_num=200,
            # pos_hint={'center_x':0.5,'center_y':0.5},
            check=True,
            column_data = [
                ("Customer Id",dp(50)),
                ("Customer Name",dp(50)),
                ("Phone No.",dp(50))
            ],
            row_data=self.data_fetched

    
            )
        #Add table widget
        self.root.ids.data_scr_third.ids.data_layout_third.add_widget(self.table)

    def add_datatable_order(self):
        self.data_fetched = MainApp().connect_and_grab_database("select * from orders")
        print(self.data_fetched)
        self.table =MDDataTable(
            size_hint=(1,1),
            rows_num=200,
            # pos_hint={'center_x':0.5,'center_y':0.5},
            check=True,
            column_data = [
                ("Order Id",dp(30)),
                ("Order Date",dp(30)),
                ("Product Id",dp(30)),
                ("Customer Id",dp(30)),
                ("Qty",dp(30)),
                ("Price",dp(30)),
                ("Total",dp(30))
                




            ],
            row_data=self.data_fetched

    
            )
        #Add table widget
        self.root.ids.data_scr_fourth.ids.data_layout_fourth.add_widget(self.table)

    def add_datatable_all(self):
        query="""select * from product inner join orders on product.product_id=orders.product_id inner join 
                customers on orders.customer_id=customers.customer_id"""
        self.data_fetched = MainApp().connect_and_grab_database(query)
        print(self.data_fetched)
        self.table =MDDataTable(
            size_hint=(1,1),
            rows_num=200,
            # pos_hint={'center_x':0.5,'center_y':0.5},
            check=True,
            column_data = [
                ("Product Id",dp(30)),
                ("Product Name",dp(30)),
                ("Quantity",dp(30)),
                ("Descrption",dp(30)),
                ("Category",dp(30)),
                ("Order Id",dp(30)),
                ("Order Date",dp(30)),
                ("Product Id",dp(30)),
                ("Customer Id",dp(30)),
                ("Qty",dp(30)),
                ("Price",dp(30)),
                ("Total",dp(30)),
                ("Customer Id",dp(30)),
                ("Customer Name",dp(30)),
                ("Phone No.",dp(30))




            ],
            row_data=self.data_fetched

    
            )
        #Add table widget
        self.root.ids.data_scr_fifth.ids.data_layout_fifth.add_widget(self.table)


    def change_screen(self, screen: str):
        self.root.current = screen
        



MainApp().run()
