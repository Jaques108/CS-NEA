from flask import Flask,request,jsonify


app = Flask(__name__)

#In API's we have types of requests

#The ones we care about are GET and POST

#Get is getting something quickly

#POST is giving some data to the server in exchange for some more (sometimes)

#Tasks

#Research flask API's understand what a POST method is

#Implement a login through your API (simple if statements for now, SQL later)

@app.route('/')     #My first endpoint (Where someone gets something)
def hello_world():
    return 'hello forld !'
@app.route('/login',methods=['POST'])
def login():

    if password =='Password123':
        return True
    #Do this !
    pass
@app.route('/Multiplyby5',methods=['GET'])
def Multiply():
    data_id = request.args.get('input')
    if data_id:
        return f'{int(data_id) * 5}'
    else:
        return 'no data !'
app.run(debug=True)