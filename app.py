import requests
import time
from datetime import datetime, timedelta
from flask import Flask, render_template, request


app = Flask("VaccineSlotApp")

@app.route("/")
def home():
    return render_template("myform.html")

@app.route("/output", methods=[ "GET" ] )
def slot():
    x1 = int(request.args.get("z1"))
    x2 = int(request.args.get("z2"))
    person_age = x2
    area_pincode = [x1]
    total_days = 1
    print_flag = 'y'
    data = ("Started searching for covid vaccine slots !!!")
    current = datetime.today()
    form = [current+timedelta(days=i) for i in range(total_days)]
    correct_date = [i.strftime("%d-%m-%y") for i in form]
    while True:
        i=0
        for find_code in area_pincode:
            for enter_date in correct_date:
                
                url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
                    find_code, enter_date)
                
                requirements = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
                
                final_op = requests.get(url, headers=requirements)
                
                if final_op.ok:
                    file_json = final_op.json()
                    
                    flag = False
                    if file_json["centers"]:
                        if(print_flag.lower() == "y"):
                            
                            for place in file_json["centers"]:
                                for availability in place["sessions"]:
                                    if(availability["min_age_limit"]<= person_age and availability["available_capacity"]>0):
                                        ##print('The pincode for which you are finding is : ' + find_code)
                                        ##print('it is available in : {}'.format(enter_date))
                                        data1 = ("Name of hospital and destination is :  "+place["name"])
                                        data2 = ("Name for the block is : "+place["block_name"])
                                        data3 = ("Price for the vaccine is : "+ place["fee_type"])
                                        data4 = ("availability status of the vaccine is : "+ str(availability["available_capacity"]))
                                        
                                        if (availability["vaccine"] != ''):
                                            data5 = ("The type of vaccine is : "+availability["vaccine"])
                                            
                                        i=i+1
                                        
                                    else:
                                        pass
                        else:
                            pass
                        
                    else:
                        pass
        if(i==0):
            data1 = ("Right now no vaccine slots are available !...Try after sometime...")
            return render_template("result.html", data=data ,data1=data1)
            
        else:
            data6 = ("The search is finished !")
            return render_template("result.html", data=data , data1=data1 , data2=data2 , data3=data3 , data4=data4 , data5=data5 , data6=data6 )
        
app.run(debug=True)




