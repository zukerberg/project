import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def label_encode(df, category='Smell'):
    df[category]=df[category].replace("Average",2.5)
    df[category]=df[category].replace("Good",5)
    df[category]=df[category].replace("Bad",1)
    return df

def filter_cond(df , block , floor , washroom_type):
    return df[(df['Select block'] == block) & (df['Select floor'] == floor) & (df['Select washroom'] == washroom_type)]

def avg_cat(df , category):
    if category == 'Smell':
        return round(np.mean(df[category]),1)
    else:
        return round(np.mean(df[category].astype(np.int32)), 1)

def get_rating(df):
    clean_1=0
    clean_2=0
    clean_3=0
    clean_4=0
    clean_5=0
    for i in df['Cleanliness']:
        if i==1:
            clean_1+=1
        elif i==2:
            clean_2+=1
        elif i==3:
            clean_3+=1
        elif i==4:
            clean_4+=1
        else:
            clean_5+=1
    clean_rate = [clean_1,clean_2,clean_3,clean_4,clean_5]
    
    water_1=0
    water_2=0
    water_3=0
    water_4=0
    water_5=0
    for i in df['Water Supply']:
        if i==1:
            water_1+=1
        elif i==2:
            water_2+=1
        elif i==3:
            water_3+=1
        elif i==4:
            water_4+=1
        else:
            water_5+=1
    water_rate = [water_1,water_2,water_3,water_4,water_5]

    light_1=0
    light_2=0
    light_3=0
    light_4=0
    light_5=0
    for i in df['Light Condition']:
        if i==1:
            light_1+=1
        elif i==2:
            light_2+=1
        elif i==3:
            light_3+=1
        elif i==4:
            light_4+=1
        else:
            light_5+=1
    light_rate = [light_1,light_2,light_3,light_4,light_5]

    bad=0
    neutral=0
    good=0
    for i in df['Smell']:
        if i==1:
            bad+=1
        elif i==2.5:
            neutral+=1
        else:
            good+=1
    sm_rate = [good , neutral , bad]

    return clean_rate , water_rate , light_rate , sm_rate

def describe(col , value):
    if value == 3:
        sent = f"On an average, people have given 3⭐ rating (on a scale of 1-5) to {col} in washrooms"
    elif value < 3:
        sent = f"The {col} in washrooms is not upto the mark. On an average, people have rated less than 3⭐ which clearly shows that they are not satisfied with available services and hence there is a need to improve"
    else:
        sent = f"The {col} in washrooms is upto the mark. On an average, people have rated greater than 3⭐"
    return value , sent

def describe1(col , value):
    if value == 3:
        sent = f"On an average, people have rated {col} of this washroom as Neutral"
    elif value <3:
        sent = f"The {col} in washrooms is not upto the mark. On an average, people have rated smell as Bad which clearly shows that they are not satisfied with available services and hence there is a need to improve"
    else:
        sent = f"The {col} in washrooms is upto the mark. On an average, people have rated smell as Good"
    return value , sent

def multiple_plots(data , idx , cat):
    clean = {}
    for val in list(data.keys()):
        if clean.get(val) is None:
            clean[val] = []
    for val in list(data.keys()):
        if np.isnan(data[val][idx]):
            clean[val] = 0
        else:
            clean[val] = data[val][idx]       
    clean = {key:value for (key, value) in sorted(clean.items(), key=lambda x: x[1]) if value>0}
    names = list(clean.keys())
    values = list(clean.values())
    table = {key:value for (key, value) in clean.items() if value<=2}
    return clean, names, values , idx , table

def single_table(df):
    blck = df['Select block'].unique().tolist()
    flor = df['Select floor'].unique().tolist()
    types = df['Select washroom'].unique().tolist()
    category = ['Cleanliness', 'Water Supply', 'Light Condition', 'Smell']
    avg_of_all = {}
    m_plot_data = {}
    for i in blck:
        for j in flor:
            for k in types:
                f_data = filter_cond(df , i , j , k)
                if avg_of_all.get(' '.join([i,j,k])) is None:
                    avg_of_all[' '.join([i,j,k])] = []
                for cat in category:
                    sp_mean = avg_cat(f_data , cat)
                    ratings = get_rating(f_data)
                    m_plot_data[' '.join([i,j,k])] = ratings
                    avg_of_all[' '.join([i,j,k])].append(sp_mean)
    desc = {}
    for c in range(len(category)):
        clean, names, values, idx, table = multiple_plots(avg_of_all , c , category[c])
        desc[category[c]] = table
    # csv to be send in mail
    rep = pd.DataFrame.from_dict(desc)
    rep.index.rename('Name' , inplace = True)
    rep.fillna(' ' , inplace = True)
    #rep.to_csv('./static/result.csv')
    # string format
    html = rep.to_html()
    return html