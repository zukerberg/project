import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

from flask import Flask , render_template , redirect , request , url_for
from flask_mail import Mail, Message

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import calculate 

app = Flask(__name__)
mail = Mail(app)              # instantiate the mail class

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'feedbackmonitor123@gmail.com'
app.config['MAIL_PASSWORD'] = 'puadmin@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_ASCII_ATTACHMENTS'] = True

mail = Mail(app)

# connect to gcloud
scopes = [
"https://www.googleapis.com/auth/spreadsheets",
"https://www.googleapis.com/auth/drive",
"https://spreadsheets.google.com/feeds",
"https://www.googleapis.com/auth/drive.file"
]
# get credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name("./config/credentials.json", scopes)    # access the json key you downloaded earlier 

# storing data in json format
now = datetime.datetime.now()                  # now = 2021-06-25 07:58:56.550604
#dt_string = now.strftime("%d-%m-%Y-%H-%M")   
dt_string2 = now.strftime("%d/%m/%Y %H:%M")    # 25/06/2021 07:58

""" Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    err = None
    if request.method == 'POST':
        if request.form['username'] == '' or request.form['password'] == '':
            err = "Enter your credentials to login"
        elif request.form['username'] != 'puisadmin@123' or request.form['password'] != 'puisadmin@123':
            err = "Invalid Credentials. Please try again."
        else:
            return redirect(url_for("display"))
    return render_template('login.html', error=err)
"""

@app.route('/')
def display():
    return render_template("adminLogin.html")


@app.route('/results' , methods=['POST'])
def single():
    if request.method== 'POST':
        # get values from drop down list
        block = request.form['block']
        floor = request.form['floor']
        washroom_type = request.form['type']
        s_date = request.form['startdate']        # 2021-10-03 - INPUT : year - month - date
        e_date = request.form['enddate']          # 2021-10-04
        # condition check for empty values
        if ((block is None) or (floor is None) or (washroom_type is None) or (len(s_date) == 0) or (len(e_date) == 0)):
            return render_template('adminLogin.html' , msg = "One or more fields is empty")
        if (block == "Block 3" and floor in ["Floor 1" , "Floor 2" , "Floor 3"]):
            return render_template('adminLogin.html' , msg = "Block 3 has only Ground floor, choose accordingly")
        #if (block == "All") and (floor == "All Floor") and (washroom_type == "Both"):
        #    return render_template('multiple.html') 
        # convert str into datetime object
        startdate = pd.to_datetime(s_date).date()  # year - month - date
        enddate = pd.to_datetime(e_date).date()
        # condition check for time period       
        if startdate > enddate:
            return render_template('adminLogin.html' , msg = "Please specify correct time period")       
        # this is rendered through google drive and sheets api
        try:
            client = gspread.authorize(credentials)          # authenticate the JSON key with gspread
            sheet = client.open("Feedback").sheet1           # open sheet 
            all_data = sheet.get_all_records()
            df = pd.DataFrame(all_data)
        except Exception as e:
            return "Could not fetch data from server\n" + e
        # label encoding of categorical data
        df = calculate.label_encode(df)
        # filter condition based on values of data recieved
        for i in range(len(df)):
            val = df['Timestamp'][i].split()[0].split('/')
            df['Timestamp'][i] = '/'.join([val[1], val[0], val[2]])
        df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.date
        fdf = df[(df['Timestamp'] >= startdate) & (df['Timestamp'] <= enddate)]

        # if no data available acc to date specified return no data gif
        if (fdf.shape[0]) == 0:
            return render_template('error.html')

        # filter condition based on values recieved
        elif (block == "All") and (floor == "All Floor") and (washroom_type == "Both"):
            blck = df['Select block'].unique().tolist()
            flor = df['Select floor'].unique().tolist()
            types = df['Select washroom'].unique().tolist()
            # Cleanliness
            category = ['Cleanliness', 'Water Supply', 'Light Condition', 'Smell']
            avg_of_all = {}
            m_plot_data = {}
            for i in blck:
                for j in flor:
                    for k in types:
                        f_data = calculate.filter_cond(df , i , j , k)
                        if avg_of_all.get(' '.join([i,j,k])) is None:
                            avg_of_all[' '.join([i,j,k])] = []
                        for cat in category:
                            sp_mean = calculate.avg_cat(f_data , cat)
                            ratings = calculate.get_rating(f_data)
                            m_plot_data[' '.join([i,j,k])] = ratings
                            avg_of_all[' '.join([i,j,k])].append(sp_mean)
            desc = {}
            for c in range(len(category)):
                clean, names, values, idx, table = calculate.multiple_plots(avg_of_all , c , category[c])
                desc[category[c]] = table
                if len(names) <= 10:
                    fig = plt.figure(figsize=(10, 8))
                    plt.barh(range(len(clean)), values)
                    plt.yticks(ticks = range(len(clean)) , labels = names, fontsize = 14)
                    plt.xticks(fontsize = 14)
                    plt.title(f'{category[c]} Comparison' , fontsize = 20 , fontweight = 60)
                    plt.xlabel(f'Average {category[c]} Rating' , fontsize = 15 , fontweight = 500)

                    # get current axis object
                    ax = plt.gca()
                    # Remove x, y Ticks
                    ax.xaxis.set_ticks_position('none')
                    ax.yaxis.set_ticks_position('none')
                    
                    # Add padding between axes and labels
                    ax.xaxis.set_tick_params(pad = 5)
                    ax.yaxis.set_tick_params(pad = 10)
                    
                    # Add annotation to bars - return position of bars
                    for l in ax.patches:
                        plt.text(l.get_width()+0.05 , l.get_y()+0.4 , str(round((l.get_width()), 2)) , fontsize = 13, fontweight = 400)
                    plt.savefig(f'./static/mplots{idx}.png' , bbox_inches='tight')
                else:
                    fig = plt.figure(figsize=(20, 15))
                    plt.barh(range(len(clean)), values)
                    plt.yticks(ticks = range(len(clean)) , labels = names, fontsize = 18)
                    plt.xticks(fontsize = 14)
                    plt.title(f'{category[c]} Comparison' , fontsize = 25 , fontweight = 90)
                    plt.xlabel(f'Average {category[c]} Rating' , fontsize = 20 , fontweight = 600)
                    # get current axis object
                    ax = plt.gca()
                    # Remove x, y Ticks
                    ax.xaxis.set_ticks_position('none')
                    ax.yaxis.set_ticks_position('none')                    
                    # Add padding between axes and labels
                    ax.xaxis.set_tick_params(pad = 5)
                    ax.yaxis.set_tick_params(pad = 10)                    
                    # Add annotation to bars - return position of bars
                    for l in ax.patches:
                        plt.text(l.get_width()+0.05 , l.get_y()+0.4 , str(round((l.get_width()), 2)) , fontsize = 19, fontweight = 500)
                    plt.savefig(f'./static/mplots{idx}.jpg' , bbox_inches='tight')
            # csv to be send in mail
            rep = pd.DataFrame.from_dict(desc)
            rep.index.rename('Name' , inplace = True)
            rep.fillna(' ' , inplace = True)
            rep.to_csv('./static/result.csv')
            # string format
            html = rep.to_html()
            # html code saved in file
            # with open("./templates/report.html" , "w") as f:
                # f.write(html)
            try:
                msg = Message(f'WASHROOM: FEEDBACK ANALYSIS {dt_string2}', sender = 'feedbackmonitor123@gmail.com', recipients = ['feedbackmonitor123@gmail.com'])
                msg.body = f"FEEDBACK ANALYSIS:\n\n" + f"Start Date: {s_date}\nEnd Date: {e_date}\n" + "--"*30 + "\n\n"
                with app.open_resource(f"./static/result.csv") as fp:
                    msg.attach("result.csv", "result/csv", fp.read())
                mail.send(msg)
                return render_template('showAll.html' , html = html , dates = [s_date , e_date] , message = 'Feedback Report mail successfully sent to Admin!!')
            except Exception as e:
                return render_template('showAll.html' , html = html , dates = [s_date , e_date] , message = 'Failed to send report. Please try again!!')

        else:
            html = calculate.single_table(fdf)
            fdf = calculate.filter_cond(fdf , block , floor , washroom_type)
            # email title baded on filtered condition
            report_title = block + ' , ' + floor + ' , ' + washroom_type.capitalize() + ' washroom'
            # Comments
            cmnts = list(fdf['Comments'][(fdf['Comments'] != '')]) 
            if len(cmnts)==0:
                cmnts = "No comments provided so far"
            else:
                cmnts = cmnts
            # mean calculation of all columns
            mean_1 = calculate.avg_cat(fdf , 'Cleanliness')
            mean_2 = calculate.avg_cat(fdf , 'Water Supply')
            mean_3 = calculate.avg_cat(fdf , 'Light Condition')
            mean_4 = calculate.avg_cat(fdf , 'Smell')
            overall_score = np.round((mean_1+mean_2+mean_3+mean_4)/4 , 1)
            # get values of different ratings of each column
            values = []
            ret_values = calculate.get_rating(fdf)
            for i in ret_values:
                values.append(i)
            # textual descriptions
            desc = []
            col1, sent1 = calculate.describe('Cleanliness' , mean_1)
            desc.append(sent1)
            col2, sent2 = calculate.describe('Water Supply' , mean_2)
            desc.append(sent2)
            col3, sent3 = calculate.describe('Light Condition' , mean_3)
            desc.append(sent3)
            col4, sent4 = calculate.describe1('Smell' , mean_4)
            desc.append(sent4)
            # plotting graphs
            titles = list(fdf.columns[4:-2])
            labels1 = ['Rate 1','Rate 2','Rate 3','Rate 4','Rate 5']   
            labels2 = ['Good','Neutral','Bad']    
            for idx in range(0, 4):
                fig = plt.figure(figsize=(8,8) , edgecolor='darkorange' , linewidth=15)
                if idx==3:
                    plt.bar(x = labels2 , height = values[idx] , color=['yellow','purple','red'] , width = 0.5,edgecolor='black')
                else:
                    plt.bar(x = labels1 , height = values[idx] , color=['cyan','yellow','purple','red','green'] , width = 0.5,edgecolor='black')
                plt.title(titles[idx], fontsize = 21, weight = 'demibold', pad = 15, fontstyle = 'italic')
                plt.xticks(rotation=0 , fontsize=16)
                plt.yticks([])
                plt.ylabel('')
                fig.subplots_adjust(bottom = 0.14)
                ax = plt.gca()
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['left'].set_visible(False)
                for p in ax.patches:
                    ax.annotate("%.2f" % (float(p.get_height())), (p.get_x() + p.get_width() / 2., abs(p.get_height())),
                    ha='center', va='bottom', color='black', xytext=(0, 5),rotation = 'horizontal',
                    textcoords='offset points', fontsize = 16 , fontweight = 'medium')
                plt.savefig(f'./static/plot{idx}.jpg')
            try:
                msg = Message(f'WASHROOM: FEEDBACK ANALYSIS {dt_string2}', sender = 'feedbackmonitor123@gmail.com', recipients = ['feedbackmonitor123@gmail.com'])
                msg.body = f"FEEDBACK ANALYSIS:\n\n{report_title}\n\n" + f"Start Date: {s_date}\nEnd Date: {e_date}\n" + "--"*30 + "\n\n" + f"Overall Cleanliness Rating: {mean_1}\n Overall Water Supply Rating: {mean_2}\n Overall Light Condition Rating: {mean_3}\n Overall Smell Rating: {mean_4}\n\n Overall Rating of the washroom on the scale of 1 to 5: {overall_score}\n\n Comments of the people are: {cmnts}"
                mail.send(msg)
                return render_template('SingleCategoryPage.html', title = report_title , text = desc , html = html , dates = [s_date , e_date] , message = 'Feedback Report mail successfully sent to Admin!!')
            except Exception as e:
                return render_template('SingleCategoryPage.html', title = report_title , text = desc , html = html , dates = [s_date , e_date] , message = 'Failed to sent email. Please try again')


if __name__ == '__main__':
    app.run(debug=True)
