
from random import randint
import csv
import hashlib
import json
from util import util


#sum_all_score(percentage denominator) = 52100
percentage_denominator=52100

#4
avg_monthly_bank_balance=[
	[0,100],
	[5,200],
	[10,400],
	[20,500],
	[40,580],
	[60,650],
	[100,710],
	[150,750],
	[300,800],
	[500,840],
	[100000,900]
]

#3
avg_monthly_income=[
	[0,100],
	[5,500],
	[10,1100],
	[20,2100],
	[40,4010],
	[60,6010],
	[100,10100],
	[100000,10500]
]

#x+rootx: 2
median_ticket_size=[
	[0,100],
	[50,57],
	[100,110],
	[150,163],
	[200,214],
	[300,317],
	[500,523],
	[1000,1031],
	[2000,2041],
	[5000,5071],
	[10000,6000]
]

#1
history_length=[
	[1,100],
	[3,300],
	[6,600],
	[12,1200],
	[18,1800],
	[24,2400],
	[48,4800],
	[40000,5000]
]

def gen_y(x,range_dict):
	for a,b in range_dict:
		if a>x:
			return b

#print gen_y(110,avg_monthly_bank_balance)

def push2salesforce(object_name,value):
	pass

def gen_random_data():
	for i in range(1,10):
		d1={}
		d1["avg_monthly_bank_balance"]=randint(0,600)
		d1["avg_monthly_income"]=randint(0,200)
		d1["median_ticket_size"]=randint(0,7000)
		d1['history_length']=randint(1,70)

		d={}
		d1['score_avg_monthly_bank_balance']=gen_y(d1["avg_monthly_bank_balance"],avg_monthly_bank_balance)
		d1['score_avg_monthly_income']=gen_y(d1["avg_monthly_income"],avg_monthly_income)
		d1['score_median_ticket_size']=gen_y(d1["median_ticket_size"],median_ticket_size)
		d1['score_history_length']=gen_y(d1['history_length'],history_length)
		
		d1['credit_score'] = (d1['score_avg_monthly_bank_balance']*4
							+ d1['score_avg_monthly_income']*3
							+ d1['score_median_ticket_size']*2
							+ d1['score_history_length'])*80/percentage_denominator
		#print d1
		#print d
		return d1
		#push2salesforce(object_name,value)

def read_csv():
	'''
	email,phone,pincode,city,name,emailFromTC,website,twitter,facebook,avatar,address,Country,created at,updated_at
	email,phone,address(city,address,Country,pincode),-,website,twitter,facebook
	'''
	with open('data.csv', 'rb') as f:
	    reader = csv.reader(f)
	    for row in reader:
	        print row

def clean_string(text):
	text = text.replace("'","")
	text = text.replace("`","")
	text=text.strip()
	return text

def read2():
	ifile  = open('data.csv', "rb")
	reader = csv.reader(ifile)
	arr=[]
	rownum = 0
	for row in reader:
	    # Save header row.
	    if rownum == 0:
	        header = row
	    else:
	        colnum = 0
	        d=gen_random_data()
	        temp_arr=[]
	        for col in row:
	            #print '%-8s: %s' % (header[colnum], col)
	            temp_arr.append(clean_string(col))
	            colnum += 1
	        #d['columns']=temp_arr
	        new_arr=[]
	        #new_arr.append(temp_arr[9])#dp
	        d['profile_pic']=temp_arr[9]
	        d['fb']=temp_arr[8]
	        d['tw']=temp_arr[7]
	        d['wb']=temp_arr[6]

	        new_arr.append(temp_arr[4])#name
	        new_arr.append(temp_arr[0])#email
	        new_arr.append(temp_arr[1])#phone
	        new_arr.append("%s %s %s %s"%(temp_arr[3],temp_arr[10],temp_arr[11],temp_arr[2]))#address
	        new_arr.append(hashlib.md5(temp_arr[0]+temp_arr[1]).hexdigest()[:7])
	        new_arr.append(d['credit_score'])

	        final_arr=[]
	        final_arr.append(new_arr)
	        final_arr.append(d)
	        
	        arr.append(final_arr)

	    rownum += 1
	    

	print arr
	with open("data_dump.json", "w") as f:
		f.write(json.dumps(arr))


def push():
	access_token = util.get_access_token()['access_token']
	headers = {'Authorization': 'Bearer ' + access_token,
	           'Content-type': 'application/json'}

	url = '/services/data/v34.0/sobjects/Account/'

	new_account = {"Name": "BlueDart"}
	json_new_account = json.dumps(new_account)

	conn = util.get_connection()
	conn.request("POST", url, json_new_account, headers)
	res = conn.getresponse()
	data = res.read().decode("utf-8")
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(json.loads(data))
	print(data)

if __name__ == '__main__':
	push()
	#print gen_random_data()


