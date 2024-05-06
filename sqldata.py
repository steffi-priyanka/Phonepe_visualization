import dataframe
import mysql.connector as sql

# Table Creation for SQL Connection
mydb=sql.connect(host="localhost",
                   user="root",
                   password="root",
                   database= "phonepe_data",
                   port = "3306")
cursor =mydb.cursor()

#################  1.  AGGREGATE INSURANCE TABLE   #################
create_query_1 = '''CREATE TABLE if not exists agg_insurance(State varchar(255),
                                              Year int,
                                              Quarter int,
                                              Trans_type varchar(255),
                                              Trans_count bigint,
                                              Amount bigint)'''
cursor.execute(create_query_1)
insert_query_1 = '''INSERT INTO agg_insurance(State, Year,Quarter, Trans_type,
                                              Trans_count,Amount )
                                              values(%s,%s,%s,%s,%s,%s)'''
data = dataframe.df_agg_insurance.values.tolist()  ############## remove dataframe. while code merge
cursor.executemany(insert_query_1,data)
mydb.commit()


########## 2. Aggregated Transaction #########

create_query_2 = '''CREATE TABLE if not exists agg_transaction(State varchar(255),
                                              Year int,
                                              Quarter int,
                                              Trans_type varchar(255),
                                              Trans_count bigint,
                                              Amount bigint)'''
cursor.execute(create_query_2)
insert_query_2= '''INSERT INTO agg_transaction(State, Year,Quarter, Trans_type,
                                              Trans_count,Amount )
                                              values(%s,%s,%s,%s,%s,%s)'''
data = dataframe.df_agg_trans.values.tolist()  ############## remove dataframe. while code merge
cursor.executemany(insert_query_2,data)
mydb.commit()

########## 3. Aggregated USER #########

create_query_3 = '''CREATE TABLE if not exists agg_user(State varchar(255),
                                              Year int,
                                              Quarter int,
                                              Brand varchar(100),
                                              Trans_count bigint,
                                              Percentage float)'''
cursor.execute(create_query_3)
insert_query_3= '''INSERT INTO agg_user(State, Year,Quarter, Brand ,
                                              Trans_count,Percentage)
                                              values(%s,%s,%s,%s,%s,%s)'''
data = dataframe.df_agg_user.values.tolist()  ############## remove dataframe. while code merge
cursor.executemany(insert_query_3,data)
mydb.commit()

########## 4. MAP INSURANCE #########

create_query_4 = '''CREATE TABLE if not exists map_insurance(State varchar(255),
                                              Year int,
                                              Quarter int,
                                              District varchar(100),
                                              Trans_count bigint,
                                              Amount bigint)'''
cursor.execute(create_query_4)
insert_query_4= '''INSERT INTO map_insurance(State, Year, Quarter, District,
                                              Trans_count,Amount)
                                              values(%s,%s,%s,%s,%s,%s)'''
data = dataframe.df_map_insurance.values.tolist()  ############## remove dataframe. while code merge
cursor.executemany(insert_query_4,data)
mydb.commit()

########## 5. MAP TRANSACTION #########

create_query_5 = '''CREATE TABLE if not exists map_transaction(State varchar(255),
                                              Year int,
                                              Quarter int,
                                              District varchar(100),
                                              Trans_count bigint,
                                              Amount bigint)'''
cursor.execute(create_query_5)

insert_query_5= '''INSERT INTO map_transaction(State, Year, Quarter, District,
                                              Trans_count,Amount)
                                              values(%s,%s,%s,%s,%s,%s)'''
data = dataframe.df_map_trans.values.tolist()  ############## remove dataframe. while code merge
cursor.executemany(insert_query_5,data)
mydb.commit()

########## 6. MAP USER #########

create_query_6 = '''CREATE TABLE if not exists map_user(State varchar(255),
                                              Year int,
                                              Quarter int,
                                              District varchar(100),
                                              Registered_users bigint,
                                             App_open bigint)'''
cursor.execute(create_query_6)

insert_query_6= '''INSERT INTO map_user(State, Year, Quarter, District,
                                              Registered_users,App_open)
                                              values(%s,%s,%s,%s,%s,%s)'''
data = dataframe.df_map_user.values.tolist()  ############## remove dataframe. while code merge
cursor.executemany(insert_query_6,data)
mydb.commit()

########## 7. TOP INSURANCE #########

create_query_7= '''CREATE TABLE if not exists top_insurance(State varchar(255),
                                              Year int,
                                              Quarter int,
                                              Pincode varchar(100),
                                              Trans_count bigint,
                                             Amount bigint)'''
cursor.execute(create_query_7)

insert_query_7= '''INSERT INTO top_insurance(State, Year, Quarter, Pincode,
                                              Trans_count,Amount)
                                              values(%s,%s,%s,%s,%s,%s)'''
data = dataframe.df_top_insurance.values.tolist()  ############## remove dataframe. while code merge
cursor.executemany(insert_query_7,data)
mydb.commit()

########### 8. TOP TRANSACTION #########

create_query_8= '''CREATE TABLE if not exists top_transaction(State varchar(255), 
                                              Year int, 
                                              Quarter int, 
                                              Pincode varchar(100), 
                                              Trans_count bigint, 
                                             Amount bigint)'''
cursor.execute(create_query_8)

insert_query_8= '''INSERT INTO top_transaction(State, Year, Quarter, Pincode,                                                                                           
                                              Trans_count,Amount)
                                              values(%s,%s,%s,%s,%s,%s)'''
data = dataframe.df_top_transaction.values.tolist()  ############## remove dataframe. while code merge
cursor.executemany(insert_query_8,data)
mydb.commit()

########### 9. TOP USER #########

create_query_9= '''CREATE TABLE if not exists top_user(State varchar(255), 
                                              Year int, 
                                              Quarter int, 
                                              Pincode varchar(100), 
                                              User_count bigint 
                                             )'''
cursor.execute(create_query_9)

insert_query_9= '''INSERT INTO top_user(State, Year, Quarter, Pincode,                                                                                           
                                              User_count)
                                              values(%s,%s,%s,%s,%s)'''
data = dataframe.df_top_user.values.tolist()  ############## remove dataframe. while code merge
cursor.executemany(insert_query_9,data)
mydb.commit()
#__________________________________________________
#        LIST OF TABLES
cursor.execute("show tables")
cursor.fetchall()
