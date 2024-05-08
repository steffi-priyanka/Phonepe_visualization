#git clone https://github.com/PhonePe/pulse.git

import pandas as pd
import os
import json

## 1 DataFrame of Aggregated Insurance

agg_insurance_path = "C:/Users/user/PycharmProjects/capstone_2/pulse/data/aggregated/insurance/country/india/state/"
agg_insurance = os.listdir(agg_insurance_path)

agg_insurance_col_name = {'State': [], 'Year': [], 'Quarter': [], 'Trans_type': [],
                          'Trans_count': [], 'Amount': []}

for state in agg_insurance:
    curr_state = agg_insurance_path + state + "/"
    agg_year = os.listdir(curr_state)

    for year in agg_year:
        curr_year = curr_state + year + "/"
        agg_file = os.listdir(curr_year)

        for file in agg_file:
            curr_file = curr_year + file
            data = open(curr_file, 'r')
            agg_insurance_data = json.load(data)

            for i in agg_insurance_data['data']['transactionData']:
                name = i['name']
                count = i['paymentInstruments'][0]['count']
                amount = i['paymentInstruments'][0]['amount']
                agg_insurance_col_name['Trans_type'].append(name)
                agg_insurance_col_name['Trans_count'].append(count)
                agg_insurance_col_name['Amount'].append(amount)
                agg_insurance_col_name['State'].append(state)
                agg_insurance_col_name['Year'].append(year)
                agg_insurance_col_name['Quarter'].append(int(file.strip('.json')))

df_agg_insurance = pd.DataFrame(agg_insurance_col_name)

df_agg_insurance["State"] = df_agg_insurance["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df_agg_insurance["State"] = df_agg_insurance["State"].str.replace("-", " ")
df_agg_insurance["State"] = df_agg_insurance["State"].str.title()
#print(df_agg_insurance)

## 2 DataFrame of Aggregated Transaction

agg_trans_path="C:/Users/user/PycharmProjects/capstone_2/pulse/data/aggregated/transaction/country/india/state/"
agg_transaction = os.listdir(agg_trans_path)

agg_trans_col_name = {'State': [], 'Year': [], 'Quarter': [], 'Trans_type': [], 'Trans_count': [],
                       'Amount': []}
for state in agg_transaction:
    curr_state = agg_trans_path + state + "/"
    agg_year = os.listdir(curr_state)

    for year in agg_year:
        curr_year = curr_state + year + "/"
        agg_file = os.listdir(curr_year)

        for file in agg_file:
            curr_file = curr_year + file
            data = open(curr_file, 'r')
            phone_data = json.load(data)

            for i in phone_data ['data']['transactionData']:
              name = i['name']
              count = i['paymentInstruments'][0]['count']
              amount = i['paymentInstruments'][0]['amount']
              agg_trans_col_name['Trans_type'].append(name)
              agg_trans_col_name['Trans_count'].append(count)
              agg_trans_col_name['Amount'].append(amount)
              agg_trans_col_name['State'].append(state)
              agg_trans_col_name['Year'].append(year)
              agg_trans_col_name['Quarter'].append(int(file.strip('.json')))

df_agg_trans = pd.DataFrame(agg_trans_col_name)

df_agg_trans["State"]=df_agg_trans["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df_agg_trans["State"]=df_agg_trans["State"].str.replace("-"," ")
df_agg_trans["State"]=df_agg_trans["State"].str.title()
#print(df_agg_trans)

## 3 DataFrame of Aggregated user

user_path = "C:/Users/user/PycharmProjects/capstone_2/pulse/data/aggregated/user/country/india/state/"
agg_user = os.listdir(user_path)

user_col_name = {'State': [], 'Year': [], 'Quarter': [], 'Brand': [], 'Count': [],
                 'Percentage': []}

for state in agg_user:
    curr_state = user_path + state + "/"
    agg_year = os.listdir(curr_state)

    for year in agg_year:
        curr_year = curr_state + year + "/"
        agg_file = os.listdir(curr_year)

        for file in agg_file:
            curr_file = curr_year + file
            data = open(curr_file, 'r')
            user_data = json.load(data)

            try:

                for i in user_data['data']['usersByDevice']:
                    brand = i['brand']
                    count = i['count']
                    percent = i['percentage']
                    user_col_name['Brand'].append(brand)
                    user_col_name['Count'].append(count)
                    user_col_name['Percentage'].append(percent)
                    user_col_name['State'].append(state)
                    user_col_name['Year'].append(year)
                    user_col_name['Quarter'].append(int(file.strip('.json')))  # strip removes ",json"
            except:
                pass

df_agg_user = pd.DataFrame(user_col_name)

df_agg_user["State"] = df_agg_user["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df_agg_user["State"] = df_agg_user["State"].str.replace("-", " ")
df_agg_user["State"] = df_agg_user["State"].str.title()

## 4 DataFrame of Map Insurance

map_insurance_path = "C:/Users/user/PycharmProjects/capstone_2/pulse/data/map/insurance/hover/country/india/state/"
map_insurance = os.listdir(map_insurance_path)

map_insurance_col_name = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Trans_count': [],
                          'Amount': []}

for state in map_insurance:
    curr_state = map_insurance_path + state + "/"
    agg_year = os.listdir(curr_state)

    for year in agg_year:
        curr_year = curr_state + year + "/"
        agg_file = os.listdir(curr_year)

        for file in agg_file:
            curr_file = curr_year + file
            data = open(curr_file, 'r')
            map_insurance_data = json.load(data)

            for i in map_insurance_data['data']['hoverDataList']:
                district = i['name']
                count = i['metric'][0]['count']
                amount = i['metric'][0]['amount']
                map_insurance_col_name['District'].append(district)
                map_insurance_col_name['Trans_count'].append(count)
                map_insurance_col_name['Amount'].append(amount)
                map_insurance_col_name['State'].append(state)
                map_insurance_col_name['Year'].append(year)
                map_insurance_col_name['Quarter'].append(int(file.strip('.json')))  # strip removes ",json"

df_map_insurance = pd.DataFrame(map_insurance_col_name)

df_map_insurance["State"] = df_map_insurance["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df_map_insurance["State"] = df_map_insurance["State"].str.replace("-", " ")
df_map_insurance["State"] = df_map_insurance["State"].str.title()

## 5 DataFrame of Mapped Transaction

map_trans_path = "C:/Users/user/PycharmProjects/capstone_2/pulse/data/map/transaction/hover/country/india/state/"
map_trans = os.listdir(map_trans_path)

map_col_name = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Trans_count': [],
                'Amount': []}

for state in map_trans:
    curr_state = map_trans_path + state + "/"
    agg_year = os.listdir(curr_state)

    for year in agg_year:
        curr_year = curr_state + year + "/"
        agg_file = os.listdir(curr_year)

        for file in agg_file:
            curr_file = curr_year + file
            data = open(curr_file, 'r')
            map_data = json.load(data)

            for i in map_data['data']['hoverDataList']:
                district = i['name']
                count = i['metric'][0]['count']
                amount = i['metric'][0]['amount']
                map_col_name['District'].append(district)
                map_col_name['Trans_count'].append(count)
                map_col_name['Amount'].append(amount)
                map_col_name['State'].append(state)
                map_col_name['Year'].append(year)
                map_col_name['Quarter'].append(int(file.strip('.json')))  # strip removes ",json"

df_map_trans = pd.DataFrame(map_col_name)

df_map_trans["State"] = df_map_trans["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df_map_trans["State"] = df_map_trans["State"].str.replace("-", " ")
df_map_trans["State"] = df_map_trans["State"].str.title()

## 6 DataFrame of Mapped User

user_map_path = "C:/Users/user/PycharmProjects/capstone_2/pulse/data/map/user/hover/country/india/state/"
user_map = os.listdir(user_map_path)

user_map_col_name = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Registered_users': [],
                     'App_open': []}

for state in user_map:
    curr_state = user_map_path + state + "/"
    agg_year = os.listdir(curr_state)

    for year in agg_year:
        curr_year = curr_state + year + "/"
        agg_file = os.listdir(curr_year)

        for file in agg_file:
            curr_file = curr_year + file
            data = open(curr_file, 'r')
            user_map_data = json.load(data)

            for i in user_map_data['data']['hoverData'].items():
                district = i[0]
                registered_user = i[1]['registeredUsers']
                app_open = i[1]['appOpens']
                user_map_col_name['District'].append(district)
                user_map_col_name['Registered_users'].append(registered_user)
                user_map_col_name['App_open'].append(app_open)
                user_map_col_name['State'].append(state)
                user_map_col_name['Year'].append(year)
                user_map_col_name['Quarter'].append(int(file.strip('.json')))  # strip removes ",json"

df_map_user = pd.DataFrame(user_map_col_name)

df_map_user["State"] = df_map_user["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df_map_user["State"] = df_map_user["State"].str.replace("-", " ")
df_map_user["State"] = df_map_user["State"].str.title()

## 7 DataFrame of Top Insurance

top_insurance_path = "C:/Users/user/PycharmProjects/capstone_2/pulse/data/top/insurance/country/india/state/"
top_insurance = os.listdir(top_insurance_path)

top_insurance_col_name = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Trans_count': [],
                          'Amount': []}

for state in top_insurance:
    curr_state = top_insurance_path + state + "/"
    agg_year = os.listdir(curr_state)

    for year in agg_year:
        curr_year = curr_state + year + "/"
        agg_file = os.listdir(curr_year)

        for file in agg_file:
            curr_file = curr_year + file
            data = open(curr_file, 'r')
            top_insurance_data = json.load(data)

            for i in top_insurance_data['data']['pincodes']:
                entity_name = i['entityName']
                count = i['metric']['count']
                amount = i['metric']['amount']
                top_insurance_col_name['Pincode'].append(entity_name)
                top_insurance_col_name['Trans_count'].append(count)
                top_insurance_col_name['Amount'].append(amount)
                top_insurance_col_name['State'].append(state)
                top_insurance_col_name['Year'].append(year)
                top_insurance_col_name['Quarter'].append(int(file.strip('.json')))  # strip removes ",json"

df_top_insurance = pd.DataFrame(top_insurance_col_name)

df_top_insurance["State"] = df_top_insurance["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df_top_insurance["State"] = df_top_insurance["State"].str.replace("-", " ")
df_top_insurance["State"] = df_top_insurance["State"].str.title()

## 8 DataFrame of Top transaction

top_transaction_path = "C:/Users/user/PycharmProjects/capstone_2/pulse/data/top/transaction/country/india/state/"
top_transaction = os.listdir(top_transaction_path)

top_transaction_col_name = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Trans_count': [],
                            'Amount': []}

for state in top_transaction:
    curr_state = top_transaction_path + state + "/"
    agg_year = os.listdir(curr_state)

    for year in agg_year:
        curr_year = curr_state + year + "/"
        agg_file = os.listdir(curr_year)

        for file in agg_file:
            curr_file = curr_year + file
            data = open(curr_file, 'r')
            top_transaction_data = json.load(data)

            for i in top_transaction_data['data']['pincodes']:
                entity_name = i['entityName']
                count = i['metric']['count']
                amount = i['metric']['amount']
                top_transaction_col_name['Pincode'].append(entity_name)
                top_transaction_col_name['Trans_count'].append(count)
                top_transaction_col_name['Amount'].append(amount)
                top_transaction_col_name['State'].append(state)
                top_transaction_col_name['Year'].append(year)
                top_transaction_col_name['Quarter'].append(int(file.strip('.json')))

df_top_transaction = pd.DataFrame(top_transaction_col_name)

df_top_transaction["State"] = df_top_transaction["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df_top_transaction["State"] = df_top_transaction["State"].str.replace("-", " ")
df_top_transaction["State"] = df_top_transaction["State"].str.title()

## 9 DataFrame of Top user

top_user_path = "C:/Users/user/PycharmProjects/capstone_2/pulse/data/top/user/country/india/state/"
top_user = os.listdir(top_user_path)

top_user_col_name = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'User_count': []}

for state in top_user:
    curr_state = top_user_path + state + "/"
    agg_year = os.listdir(curr_state)

    for year in agg_year:
        curr_year = curr_state + year + "/"
        agg_file = os.listdir(curr_year)

        for file in agg_file:
            curr_file = curr_year + file
            data = open(curr_file, 'r')
            top_user_data = json.load(data)

            for i in top_user_data['data']['pincodes']:
                name = i['name']
                user_count = i['registeredUsers']
                top_user_col_name['Pincode'].append(name)
                top_user_col_name['User_count'].append(user_count)
                top_user_col_name['State'].append(state)
                top_user_col_name['Year'].append(year)
                top_user_col_name['Quarter'].append(int(file.strip('.json')))  # strip removes ",json"

df_top_user = pd.DataFrame(top_user_col_name)

df_top_user["State"] = df_top_user["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df_top_user["State"] = df_top_user["State"].str.replace("-", " ")
df_top_user["State"] = df_top_user["State"].str.title()

#___________________________________________________________________
#

