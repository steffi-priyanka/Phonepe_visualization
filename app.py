import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as sql
import pandas as pd
import plotly.express as px
import json
import requests


mydb=sql.connect(host="localhost",
                   user="root",
                   password="root",
                   database= "phonepe_data",
                   port = "3306")
cursor = mydb.cursor()

#_________  1.  AGGREGATE INSURANCE TABLE  ____________

cursor.execute("SELECT * FROM agg_insurance")
ag_insurance = pd.DataFrame(cursor.fetchall(),columns=["State", "Year","Quarter", "Trans_type","Trans_count","Amount"])

#_______________ 2. Aggregated Transaction __________________

cursor.execute("SELECT * FROM agg_transaction")
ag_transaction = pd.DataFrame(cursor.fetchall(),columns=["State", "Year","Quarter", "Trans_type","Trans_count","Amount"])

#______________ 3. Aggregated USER ________________________

cursor.execute("SELECT * FROM agg_user")
ag_user = pd.DataFrame(cursor.fetchall(),columns=["State", "Year","Quarter", "Brand", "Count","Percentage"])
#
#________________ 4. MAP INSURANCE_____________________________

cursor.execute("SELECT * FROM map_insurance")
mp_insurance = pd.DataFrame(cursor.fetchall(),columns=["State", "Year","Quarter", "District","Trans_count","Amount"])
#
#_______________ 5. MAP TRANSACTION _________________________

cursor.execute("SELECT * FROM map_transaction")
mp_transaction = pd.DataFrame(cursor.fetchall(),columns=["State", "Year","Quarter", "District","Trans_count","Amount"])
#
#________________  6. MAP USER ________________________________

cursor.execute("SELECT * FROM map_user")
mp_user = pd.DataFrame(cursor.fetchall(),columns=["State","Year","Quarter","District","Registered_users","App_open"])
#
#__________________7. TOP INSURANCE_______________________________

cursor.execute("SELECT * FROM top_insurance")
tp_insurance = pd.DataFrame(cursor.fetchall(),columns=["State","Year","Quarter","Pincode","Trans_count","Amount"])

#__________________ 8. TOP TRANSACTION ____________________________

cursor.execute("SELECT * FROM top_transaction")
tp_transaction = pd.DataFrame(cursor.fetchall(),columns=["State","Year","Quarter","Pincode","Trans_count","Amount"])

#____________________ 9. TOP USER ______________________________

cursor.execute("SELECT * FROM top_user")
tp_user = pd.DataFrame(cursor.fetchall(),columns=["State","Year","Quarter","Pincode","User_count"])

#______________________1.1 AGGREGATED INSURANCE YEAR_________________________________________
def aggregate_insurance_Y(df,Year):

    tra_am_con_year= df[df["Year"]==Year] # specific year i year = 4 quarters
    tra_am_con_year.reset_index(drop=True,inplace=True )
    tra_g = tra_am_con_year.groupby("State")[["Trans_count","Amount"]].sum()
    tra_g.reset_index(inplace=True)

# Plotly BAR PLOT_YEAR

    col1,col2 = st.columns(2) # split columns for better visualization
    with col1:
        fig_tran_amount=px.bar(tra_g,x="State", y= "Amount",title=f"{Year} TRANSACTION AMOUNT",
                               color_discrete_sequence=px.colors.sequential.Agsunset, height= 650,width=600)
        st.plotly_chart(fig_tran_amount)
    with col2:
        fig_tran_count = px.bar(tra_g, x="State", y="Trans_count", title=f"{Year} TRANSACTION COUNT",
                                color_discrete_sequence=px.colors.sequential.Bluered, height= 650,width=600)
        st.plotly_chart(fig_tran_count)

# PLOTLY GEO VISUALIZATION _ YEAR
    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data = json.loads(response.content)
        state_name = []
        for feature in data["features"]:
            state_name.append(feature["properties"]["ST_NM"])
        state_name.sort()
        tran_amt_fig = px.choropleth(tra_g, geojson=data, locations="State", featureidkey="properties.ST_NM", color='Amount',
                            color_continuous_scale="sunset", hover_name="State", title=f"{Year} TRANSACTION AMOUNT",
                            fitbounds="locations", width=600, height=600)
        tran_amt_fig.update_geos(visible=False)
        st.plotly_chart(tran_amt_fig)

    with col2:
        tran_count_fig = px.choropleth(tra_g, geojson=data, locations="State",featureidkey="properties.ST_NM",color='Trans_count',
                                    color_continuous_scale="sunset", hover_name="State", title=f"{Year} TRANSACTION COUNT",
                                    fitbounds="locations", width=600, height=600)
        tran_count_fig.update_geos(visible=False)
        st.plotly_chart(tran_count_fig)
    return tra_am_con_year


# _________________ AGGREGATED INSURANCE_QUARTER
def agg_insu_Y_Q(df, quarter):
    aiyq = df[df["Quarter"] == quarter]  # specific year i year = 4 quarters
    aiyq.reset_index(drop=True, inplace=True)
    aiyq_g = aiyq.groupby("State")[["Trans_count", "Amount"]].sum()
    aiyq_g.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        q_fig_amount = px.bar(aiyq_g, x="State", y="Amount",
                              title=f"{aiyq['Year'].min()} AND {quarter} QUARTER TRANSACTION AMOUNT", width=600, height=650,
                              color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(q_fig_amount)

    with col2:
        q_fig_count = px.bar(aiyq_g, x="State", y="Trans_count",
                             title=f"{aiyq['Year'].min()} AND {quarter} QUARTER TRANSACTION COUNT", width=600, height=650,
                             color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(q_fig_count)

    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data = json.loads(response.content)
        state_name = []
        for feature in data["features"]:
            state_name.append(feature["properties"]["ST_NM"])
        state_name.sort()
        tran_amt_fig = px.choropleth(aiyq_g, geojson=data, locations="State", featureidkey="properties.ST_NM", color='Amount',
                            color_continuous_scale="sunset", hover_name="State", title= f"{aiyq['Year'].min()} AND {quarter} QUARTER TRANSACTION AMOUNT",
                            fitbounds="locations", width=600, height=600)
        tran_amt_fig.update_geos(visible=False)
        st.plotly_chart(tran_amt_fig)

    with col2:
        tran_count_fig = px.choropleth(aiyq_g, geojson=data, locations="State",featureidkey="properties.ST_NM",color='Trans_count',
                                    color_continuous_scale="sunset", hover_name="State", title= f"{aiyq['Year'].min()} AND {quarter} QUARTER TRANSACTION COUNT",
                                    fitbounds="locations", width=600, height=600)
        tran_count_fig.update_geos(visible=False)
        st.plotly_chart(tran_count_fig)
    return aiyq

# 1.2 AGGREGATED TRANSACTION TYPE
def aggre_tran_type(df,State):
    at_type = df[df["State"] == State]
    at_type.reset_index(drop=True, inplace=True)
    at_type_g = at_type.groupby("Trans_type")[["Trans_count", "Amount"]].sum()
    at_type_g.reset_index(inplace=True)
    col1,col2 =st.columns(2)
    with col1:
        at_fig_amount = px.pie(at_type_g, names="Trans_type", values="Amount",width=600,  height=650,
                              title=f"{State} TRANSACTION TYPE & AMOUNT",hole=0.2,
                              color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(at_fig_amount)
    with col2:
        at_fig_count = px.pie(at_type_g, names="Trans_type" , values="Trans_count",width=600,  height=650,
                              title=f"{State} TRANSACTION TYPE & COUNT", hole=0.2,
                              color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(at_fig_count)

# 1.3 AGGREGATED USER- YEAR
def agg_user_Y(df,Year):
    agu_y=df[df["Year"]== Year]
    agu_y.reset_index(drop=True, inplace=True)
    agu_y_g =  pd.DataFrame(agu_y.groupby("Brand")["Count"].sum()) #grouping 1 vaiable so pd. dataframe
    agu_y_g.reset_index(inplace=True)
    agu_fig_B_TC= px.bar(agu_y_g, x="Brand", y="Count",title=f"{Year} Brand & Transaction Count", width=800,
                          color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(agu_fig_B_TC)
    return agu_y

def agg_user_Q(df,Quarter):
    agu_Q=df[df["Quarter"]== Quarter]
    agu_Q.reset_index(drop=True, inplace=True)
    agu_Q_g = pd.DataFrame(agu_Q.groupby("Brand")["Count"].sum())
    agu_Q_g.reset_index(inplace=True)

    aguQ_fig_B_TC= px.pie(agu_Q_g, names="Brand", values="Count",  hole=0.2,
                          title=f"{Quarter} Quarter Transaction Count", width=1000,
                          color_discrete_sequence=px.colors.sequential.Magenta_r)
    st.plotly_chart(aguQ_fig_B_TC)
    return agu_Q

def agg_user_S(df,State):
    agu_S=df[df["State"]== State]
    agu_S.reset_index(drop=True, inplace=True)

    agu_S_fig_B_TC= px.line(agu_S, x="Brand", y="Count", markers=True, width=1000, hover_data= "Percentage",
                          title=f"{State} Brand, Transaction Count & Percentage")

    st.plotly_chart(agu_S_fig_B_TC)

# 2.1 MAP INSURANCE_DISTRICT

def map_ins_D(df,State):
    mi_D=df[df["State"]==State]
    mi_D.reset_index(drop=True, inplace=True)
    mi_Dg = mi_D.groupby("District")[["Amount","Trans_count"]].sum()
    mi_Dg.reset_index(inplace=True)
    col1,col2 = st.columns(2)
    with col1:
        mi_D_fig_DTA = px.bar(mi_Dg, x="District", y="Amount", width=500, height=600, title=f"{State} DISTRICT & TRANSACTION AMOUNT",
                               color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(mi_D_fig_DTA)
    with col2:
        mi_D_fig_DTC = px.bar(mi_Dg, x="District", y="Trans_count", width=600, height=600, title=f"{State} DISTRICT & TRANSACTION COUNT",
                               color_discrete_sequence=px.colors.sequential.Mint)
        st.plotly_chart(mi_D_fig_DTC)

# 2.2 MAP USER
def map_user_Y(df,Year):
    mpu_y = df[df["Year"] == Year]
    mpu_y.reset_index(drop=True, inplace=True)
    mpu_y_g = mpu_y.groupby("State")[["Registered_users","App_open"]].sum()
    mpu_y_g.reset_index(inplace=True)
    mpu_y_fig = px.line(mpu_y , x="State", y=["Registered_users","App_open"], markers=True, width=1000, height=800,
                             title= "Registered_users & App_open")

    st.plotly_chart(mpu_y_fig)
    return mpu_y

def map_user_Y_Q(df,Quarter):
    mpu_yQ = df[df["Quarter"] == Quarter]
    mpu_yQ.reset_index(drop=True, inplace=True)
    mpu_yQ_g = mpu_yQ.groupby("State")[["Registered_users","App_open"]].sum()
    mpu_yQ_g.reset_index(inplace=True)
    mpu_yQ_fig = px.line(mpu_yQ , x="State", y=["Registered_users","App_open"], markers=True, width=1000, height=800,
                             title= f"{Quarter} Registered_users & App_open",color_discrete_sequence= px.colors.sequential.Rainbow_r)

    st.plotly_chart(mpu_yQ_fig)
    return mpu_yQ

def map_user_S(df,State):
    mpu_S = df[df["State"] == State]
    mpu_S.reset_index(drop=True, inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        mpu_S_fig_RU = px.bar(mpu_S , x="Registered_users", y="District", height=800, title= f"{State} Registered_users",
                                 color_discrete_sequence= px.colors.sequential.Rainbow_r)

        st.plotly_chart(mpu_S_fig_RU)
    with col2:
        mpu_S_fig_AppOp = px.bar(mpu_S, x="App_open", y="District", height=800, title=f"{State} App_open",
                              color_discrete_sequence=px.colors.sequential.Rainbow_r)

        st.plotly_chart(mpu_S_fig_AppOp)

# 3.1 TOP INSURANCE
def topi_S(df,State):
    topi_S = df[df["State"] == State]
    topi_S.reset_index(drop=True, inplace=True)
    col1, col2 = st.columns(2)
    with col1:
        topi_S_fig_A = px.bar(topi_S, x="Quarter", y="Amount",hover_data= "Pincode", height=600,width=500, title= "Transaction Amount",
                              color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(topi_S_fig_A)
    with col2:
        topi_S_fig_C = px.bar(topi_S, x="Quarter", y="Trans_count",hover_data= "Pincode", height=600, width=500,title= "Transaction Count",
                              color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(topi_S_fig_C)

# 3.3 TOP USER

def top_user_Y(df,Year):
    tpu_y = df[df["Year"] == Year]
    tpu_y.reset_index(drop=True, inplace=True)
    tpu_y_g = pd.DataFrame(tpu_y.groupby(["State","Quarter"])["User_count"].sum())
    tpu_y_g.reset_index(inplace=True)
    tpu_y_fig = px.bar(tpu_y , x="State", y="User_count", width=1000, height=800, color="Quarter",
                             title= f"{Year} Registered_user_Count ",color_discrete_sequence=px.colors.sequential.Burgyl)

    st.plotly_chart(tpu_y_fig)
    return tpu_y

def top_user_S(df,State):
    tpu_S = df[df["State"] == State]
    tpu_S.reset_index(drop=True, inplace=True)

    tpu_S_fig = px.bar(tpu_S , x="Quarter", y="User_count", width=1000, height=800, color="User_count", hover_data="Pincode",
                             title= "Registered_user_Count ",color_continuous_scale=px.colors.sequential.Magenta)

    st.plotly_chart(tpu_S_fig)

#______________________ TOP CHART SQL QUERY _______________

def top_chart_tran_amount(table_name):

    query1 = f'''SELECT State, SUM(Amount) AS Amount FROM {table_name}
                   GROUP BY State ORDER BY Amount DESC LIMIT 10;'''
    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()
    df1 = pd.DataFrame(table, columns=["State","Amount"])
    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df1, x="State", y="Amount", title="TOP 10 Transaction Amount",
                            hover_name="State", color_discrete_sequence=px.colors.sequential.Agsunset_r, height=650, width=500)
        st.plotly_chart(fig_amount)

# QUERY 2_ASCENDING TRANSACTION_AMOUNT

    query2 = f'''SELECT State, SUM(Amount) AS Amount  FROM {table_name}
                       GROUP BY State ORDER BY Amount LIMIT 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()
    df2 = pd.DataFrame(table2 , columns=["State", "Amount"])
    col1, col2 = st.columns(2)
    with col1:
        fig_amount2 = px.bar(df2, x="State", y="Amount", title="ASCEN_Transaction Amount", hover_name="State",
                             color_discrete_sequence=px.colors.sequential.Blues_r, height=650, width=500)
        st.plotly_chart(fig_amount2)

# QUERY 3_ AVERAGE TRANSACTION_AMOUNT

    query3 = f'''SELECT State, AVG(Amount) AS Amount  FROM {table_name}
                       GROUP BY State ORDER BY Amount;'''

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()
    df3 = pd.DataFrame(table3 , columns=["State", "Amount"])
    col1, col2 = st.columns(2)
    with col1:
        fig_amount3 = px.bar(df3, x="State", y="Amount", title="AVERAGE_Transaction Amount", hover_name="State",
                            color_discrete_sequence=px.colors.sequential.Electric_r, height=800, width=1000)
        st.plotly_chart(fig_amount3)

def top_chart_tran_count(table_name):
    query1 = f'''SELECT State, SUM(Trans_count) AS Trans_count FROM {table_name}
                   GROUP BY State ORDER BY Trans_count DESC LIMIT 10;'''

    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()
    df1 = pd.DataFrame(table, columns=["State","Trans_count"])
    col1, col2 = st.columns(2)
    with col1:
        fig_count = px.bar(df1, x="State", y="Trans_count", title="TOP 10 Transaction Count", hover_name="State",
                             color_discrete_sequence=px.colors.sequential.Electric_r, height=650, width=500)
        st.plotly_chart(fig_count)

# QUERY 2_ASCENDING TRANSACTION_COUNT

    query2 = f'''SELECT State, SUM(Trans_count) AS Trans_count  FROM {table_name}
                       GROUP BY State ORDER BY Trans_count LIMIT 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()
    df2 = pd.DataFrame(table2 , columns=["State", "Trans_count"])
    col1, col2 = st.columns(2)
    with col1:
        fig_count2 = px.bar(df2, x="State", y="Trans_count", title="ASCEN_Transaction Count", hover_name="State",
                             color_discrete_sequence=px.colors.sequential.Blues_r, height=650, width=500)
        st.plotly_chart(fig_count2)

# QUERY 3_ AVERAGE TRANSACTION_COUNT

    query3 = f'''SELECT State, AVG(Trans_count) AS Trans_count  FROM {table_name}
                       GROUP BY State ORDER BY Trans_count;'''

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()
    df3 = pd.DataFrame(table3 , columns=["State","Trans_count"])
    col1, col2 = st.columns(2)
    with col1:
        fig_count3 = px.bar(df3, x="State", y="Trans_count", title="AVERAGE_Transaction Count", hover_name="State",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=800, width=1000)
        st.plotly_chart(fig_count3)

def top_chart_regis_users(table_name,State):
    query1 = f'''SELECT District, SUM(Registered_users) AS Registered_users
                 FROM {table_name}  WHERE State = "{State}" 
                 GROUP BY District
                 ORDER BY Registered_users DESC  LIMIT 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=["District", "Registered_users"])

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="District", y="Registered_users", title="TOP 10 REGISTERED USERS",
                            hover_name="District",
                            color_discrete_sequence=px.colors.sequential.Blues_r, height=650, width=500)
        st.plotly_chart(fig_amount)

# LAST 10 REGISTERED USER
    query2= f'''SELECT District, SUM(Registered_users) AS Registered_users
                 FROM {table_name}  WHERE State = "{State}" 
                 GROUP BY District
                 ORDER BY Registered_users LIMIT 10;'''
    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=["District", "Registered_users"])

    with col2:

        fig_amount_2= px.bar(df_2, x="District", y="Registered_users", title="LAST 10 REGISTERED USERS", hover_name= "District",
                            color_discrete_sequence=px.colors.sequential.Electric_r, height= 650,width= 500)
        st.plotly_chart(fig_amount_2)

 # AVERAGE REGISTERED USERS
    query3= f'''SELECT District, AVG(Registered_users) AS Registered_users
                 FROM {table_name}  WHERE State = "{State}" 
                 GROUP BY District
                 ORDER BY Registered_users;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=["District", "Registered_users"])

    fig_amount_3= px.bar(df_3, y="District", x="Registered_users", title="AVERAGE REGISTERED USERS", hover_name= "District", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

def top_chart_app_open(table_name,State):
    query1 = f'''SELECT District, SUM(App_open) AS App_open
                     FROM {table_name}  WHERE State = "{State}" 
                     GROUP BY District
                     ORDER BY App_open DESC  LIMIT 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=["District", "App_open"])

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="District", y="App_open", title="TOP 10 App_open",
                            hover_name="District",
                            color_discrete_sequence=px.colors.sequential.Blues_r, height=650, width=500)
        st.plotly_chart(fig_amount)

    # LAST 10 APP OPEN
    query2 = f'''SELECT District, SUM(App_open) AS App_open
                     FROM {table_name}  WHERE State = "{State}" 
                     GROUP BY District
                     ORDER BY App_open LIMIT 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=["District", "App_open"])

    with col2:
        fig_amount_2 = px.bar(df_2, x="District", y="App_open", title="LAST 10 App_open",
                              hover_name="District",
                              color_discrete_sequence=px.colors.sequential.Electric_r, height=650, width=500)
        st.plotly_chart(fig_amount_2)

    # AVERAGE APP_OPEN
    query3 = f'''SELECT District, AVG(App_open) AS App_open
                     FROM {table_name}  WHERE State = "{State}" 
                     GROUP BY District
                     ORDER BY App_open;'''

    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=["District", "App_open"])

    fig_amount_3 = px.bar(df_3, y="District", x="App_open", title="AVERAGE App_open",
                          hover_name="District", orientation="h",
                          color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_amount_3)

def top_chart_user_count(table_name):
    query1 = f'''SELECT State, SUM(User_count) AS User_count FROM {table_name}
                       GROUP BY State 
                       ORDER BY User_count DESC LIMIT 10;'''

    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()
    df1 = pd.DataFrame(table, columns=["State", "User_count"])
    col1, col2 = st.columns(2)
    with col1:
        fig_count = px.bar(df1, x="State", y="User_count", title="TOP 10 User_count", hover_name="User_count",
                           color_discrete_sequence=px.colors.sequential.Electric_r, height=650, width=500)
        st.plotly_chart(fig_count)

    # LAST 10 User_count
    query2 = f'''SELECT State, SUM(User_count) AS User_count FROM {table_name}
                           GROUP BY State 
                           ORDER BY User_count LIMIT 10;'''

    cursor.execute(query2)
    table = cursor.fetchall()
    mydb.commit()
    df2 = pd.DataFrame(table, columns=["State", "User_count"])
    col1, col2 = st.columns(2)
    with col1:
        fig_count = px.bar(df2, x="State", y="User_count", title="LEAST 10 User_count",
                           hover_name="User_count",
                           color_discrete_sequence=px.colors.sequential.Electric_r, height=650, width=500)
        st.plotly_chart(fig_count)
    # AVERAGE User_count
        query3 = f'''SELECT State, AVG(User_count) AS User_count FROM {table_name}
                               GROUP BY State 
                               ORDER BY User_count;'''

        cursor.execute(query3)
        table = cursor.fetchall()
        mydb.commit()
        df3 = pd.DataFrame(table, columns=["State", "User_count"])
        col1, col2 = st.columns(2)
        with col1:
            fig_count = px.bar(df3, x="State", y="User_count", title="AVERAGE User_count",
                               hover_name="User_count",
                               color_discrete_sequence=px.colors.sequential.Electric_r, height=650, width=500)
            st.plotly_chart(fig_count)


#_______________________ STREAMLIT ______________________
##                 STREAMLIT PAGE CONFIGURATION        ##

st.set_page_config(layout="wide")
st.title(":green[PHONEPE DATA VISUALIZATION AND EXPLORATION]")
st.sidebar.header(":wave: :violet[**Welcome to the dashboard!**]")

# Creating option menu in the side bar

with st.sidebar:
    select =option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select=="HOME":

    col1,col2 =st.columns(2)
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe:] ")
        st.write(
            "##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, "
            "users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments." 
             "PhonePe has since launched several Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, "
            "a dedicated insurance product for the COVID-19 pandemic among others.")
    with col2:
        st.write(" ")
        st.write(" ")
        st.write("**:violet[My Project GitHub link]** ⬇️")
        st.write("https://github.com/steffi-priyanka/Phonepe_visualization")

#________________________________________DATA EXPLORATION ______________________
elif select =="DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis","Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("Select the Method",["Insurance Analysis", "Transaction Analysis","User Analysis"])

#--------- YEAR - AGG INSURANCE ANALYSIS --------------------------
        if method == "Insurance Analysis":
            col1,col2 = st.columns(2)
            with col1:
                Year = st.slider("SELECT YEAR",min_value=2020, max_value=2023)
            agg_ins_Y = aggregate_insurance_Y(ag_insurance,Year)

        # QUARTER
            col1, col2 = st.columns(2)
            with col1:
                quarter = st.slider("**SELECT QUARTER**", min_value=1, max_value=4)
            agg_insu_Y_Q(agg_ins_Y, quarter)
#------------------------------------------------------------------------------------------------------
        elif method == "Transaction Analysis":
            col1, col2 = st.columns(2)
            with col1:
                Year = st.slider("SELECT YEAR", min_value=2018, max_value=2023)
            agg_trans_Y = aggregate_insurance_Y(ag_transaction, Year)

            col1,col2 =st.columns(2)
            with col1:
                State = st.selectbox("Select STATE",agg_trans_Y["State"].unique())
            aggre_tran_type(agg_trans_Y, State)
        # QUARTER
            col1, col2 = st.columns(2)
            with col1:
                quarter = st.slider("**SELECT QUARTER**", min_value=1, max_value=4)
            agg_trans_Q = agg_insu_Y_Q(agg_trans_Y, quarter)

        # STATE for Trans_type
            col1, col2 = st.columns(2)
            with col1:
                State = st.selectbox("Select STATE for Transaction_Type", agg_trans_Q["State"].unique())
            aggre_tran_type(agg_trans_Q, State)

#_____________________________________________________________________________________________________
        elif method == "User Analysis":
            col1, col2 = st.columns(2)
            with col1:
                Year = st.slider("SELECT YEAR", min_value=2018, max_value=2023)
            agg_userY = agg_user_Y(ag_user, Year)
        # Quarter
            col1, col2 = st.columns(2)
            with col1:
                quarter = st.slider("**SELECT QUARTER**", min_value=1, max_value=4)
            agg_userQ =  agg_user_Q(agg_userY, quarter)
        # STATE
            col1, col2 = st.columns(2)
            with col1:
                State = st.selectbox("Select STATE", agg_userQ ["State"].unique())
            agg_user_S(agg_userQ , State)

#____________________________________________________________________________________________________________________

    with tab2:
        map_method = st.radio("Select the Method", ["Map Insurance", "Map Transaction", "Map User"])

        if map_method == "Map Insurance":
            col1, col2 = st.columns(2)
            with col1:
                Year = st.slider("SELECT YEAR to view MAP INSURANCE", min_value=2020, max_value=2023)
            map_ins_Y = aggregate_insurance_Y(mp_insurance, Year)
        # STATE
            col1, col2 = st.columns(2)
            with col1:
                State = st.selectbox("Select STATE", map_ins_Y["State"].unique())
            map_ins_D(map_ins_Y, State)
        # QUARTER
            col1, col2 = st.columns(2)
            with col1:
                quarter = st.slider("**SELECT THE QUARTER**", min_value=1, max_value=4)
            map_ins_Y_Q = agg_insu_Y_Q(map_ins_Y, quarter)
        # DISTRICT
            col1, col2 = st.columns(2)
            with col1:
                State = st.selectbox("Select State to view its District", map_ins_Y_Q["State"].unique())
            map_ins_D(map_ins_Y_Q ,State)


        elif map_method == "Map Transaction":

            col1, col2 = st.columns(2)
            with col1:
                Year = st.slider("SELECT YEAR to view MAP INSURANCE", min_value=2020, max_value=2023)
            map_tra_Y = aggregate_insurance_Y(mp_transaction, Year)
         # STATE
            col1, col2 = st.columns(2)
            with col1:
                State = st.selectbox("Select STATE", map_tra_Y["State"].unique())
            map_ins_D(map_tra_Y, State)
         # QUARTER
            col1, col2 = st.columns(2)
            with col1:
                quarter = st.slider("**SELECT THE QUARTER**", min_value=1, max_value=4)
            map_tran_Y_Q = agg_insu_Y_Q(map_tra_Y, quarter)
        # DISTRICT
            col1, col2 = st.columns(2)
            with col1:
                State = st.selectbox("Select State to view its District", map_tran_Y_Q["State"].unique())
            map_ins_D(map_tran_Y_Q, State)

        elif map_method == "Map User":
            col1, col2 = st.columns(2)
            with col1:
                Year = st.slider("SELECT YEAR", min_value=2018, max_value=2023)
            mp_userY = map_user_Y(mp_user, Year)
        # QUARTER
            col1, col2 = st.columns(2)
            with col1:
                quarter = st.slider("SELECT QUARTER For MAP USER", min_value=1, max_value=4)
            map_u_Q = map_user_Y_Q(mp_userY, quarter)
        # STATE
            col1, col2 = st.columns(2)
            with col1:
                State = st.selectbox("Select STATE To VIEW", map_u_Q["State"].unique())
            map_user_S(map_u_Q, State)
#____________________________________________________

    with tab3:
        top_method = st.radio("Select the Method", ["Top Insurance", "Top Transaction", "Top User"])

        if top_method == "Top Insurance":

            col1, col2 = st.columns(2)
            with col1:
                Year = st.slider("SELECT YEAR to view TOP INSURANCE", min_value=2020, max_value=2023)
            top_ins_Y = aggregate_insurance_Y(tp_insurance, Year)
        # STATE
            col1, col2 = st.columns(2)
            with col1:
                State = st.selectbox("Select State to view its District", top_ins_Y["State"].unique())
            topi_S(top_ins_Y, State)
        # QUARTER _GEO
            col1, col2 = st.columns(2)
            with col1:
                quarter = st.slider("**SELECT THE QUARTER", min_value=1, max_value=4)
            top_ins_Y_Q = agg_insu_Y_Q(top_ins_Y, quarter)
    #--------------------------------------------------------------------------------------
        elif top_method == "Top Transaction":

            col1, col2 = st.columns(2)
            with col1:
                Year = st.slider("SELECT YEAR to view TOP TRANSACTION", min_value=2020, max_value=2023)
            top_tran_Y = aggregate_insurance_Y(tp_transaction, Year)
        # STATE
            col1, col2 = st.columns(2)
            with col1:
                State = st.selectbox("Select State to view", top_tran_Y["State"].unique())
            topi_S(top_tran_Y, State)
            # QUARTER _GEO
            col1, col2 = st.columns(2)
            with col1:
                quarter = st.slider("**SELECT THE QUARTER**", min_value=1, max_value=4)
            top_tran_Y_Q = agg_insu_Y_Q(top_tran_Y, quarter)
    #-------------------------------------------------------------------------------------
        elif top_method == "Top User":
            col1, col2 = st.columns(2)
            with col1:
                Year = st.slider("SELECT YEAR to view TOP USER", min_value=2020, max_value=2023)
            top_user_Y = top_user_Y(tp_user, Year)
        # STATE
            col1, col2 = st.columns(2)
            with col1:
                State = st.selectbox("SELECT State to view", top_user_Y["State"].unique())
            top_user_S(top_user_Y, State)

#-----------------------------------------------------------------------------------------------------
elif select == "TOP CHARTS":
    question = st.selectbox("Select Question", ["1. Transaction Amount and Count of Aggregated Insurance",
                                                "2. Transaction Amount and Count of Aggregated Transaction",
                                                "3. Transaction Amount and Count of Map Insurance",
                                                "4. Transaction Amount and Count of Map Transaction",
                                                "5. Transaction Amount and Count of Top Insurance",
                                                "6. Transaction Amount and Count of Top Transaction",
                                                "7. Transaction Count of Aggregated User",
                                                "8. Registered users of Map User",
                                                "9. App opens of Map User",
                                                "10. User Count of Top User",
                                                ])
    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        st.subheader("AGG_INS TRANSACTION AMOUNT")
        top_chart_tran_amount("agg_insurance")

        st.subheader("AGG_INS TRANSACTION COUNT")
        top_chart_tran_count("agg_insurance")

    elif question == "2.Transaction Amount and Count of Aggregated Transaction":

        st.subheader("AGG_TRA TRANSACTION AMOUNT")
        top_chart_tran_amount("agg_transaction")

        st.subheader("AGG_TRA TRANSACTION COUNT")
        top_chart_tran_count("agg_transaction")

    elif question == "3. Transaction Amount and Count of Map Insurance":

        st.subheader("MAP_INS TRANSACTION AMOUNT")
        top_chart_tran_amount("map_insurance")

        st.subheader("MAP_INS TRANSACTION COUNT")
        top_chart_tran_count("map_insurance")

    elif question == "4. Transaction Amount and Count of Map Transaction":

        st.subheader("MAP_TRA TRANSACTION AMOUNT")
        top_chart_tran_amount("map_transaction")

        st.subheader("MAP_TRA TRANSACTION COUNT")
        top_chart_tran_count("map_transaction")

    elif question == "5. Transaction Amount and Count of Top Insurance":

        st.subheader("TOP_INS TRANSACTION AMOUNT")
        top_chart_tran_amount("top_insurance")

        st.subheader("TOP_INS TRANSACTION COUNT")
        top_chart_tran_count("top_insurance")

    elif question == "6. Transaction Amount and Count of Top Transaction":

        st.subheader("TOP_TRA TRANSACTION AMOUNT")
        top_chart_tran_amount("top_transaction")

        st.subheader("TOP_TRA TRANSACTION COUNT")
        top_chart_tran_count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("AGG_USER TRANSACTION COUNT")
        top_chart_tran_count("agg_user")

    elif question == "8. Registered users of Map User":

        State = st.selectbox("Select State", mp_user["State"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_regis_users("map_user", State)

    elif question == "9. App opens of Map User":

        State = st.selectbox("Select State", mp_user["State"].unique())
        st.subheader("APP_OPEN")
        top_chart_app_open("map_user",State)

    elif question == "10. Registered users of Top User":

        st.subheader("REGISTERED USERS")
        top_chart_user_count("top_user")
