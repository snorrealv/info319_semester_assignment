from flask import Flask, request,jsonify
from flask_socketio import SocketIO,emit
from flask_cors import CORS

from dotenv import load_dotenv, find_dotenv
import os
from pathlib import Path



# ========================== setup ==========================

dotenv_path = Path('../../.env')
load_dotenv(dotenv_path=dotenv_path)

# =========================== app ===========================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('REACT_SECRET_KEY')
CORS(app,resources={r"/*":{"origins":"*"}}) # not smart with all origins? 
socketio = SocketIO(app,cors_allowed_origins="*")



# ========================== events ==========================
@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data':'This is a big dummy'}
    return jsonify(data)

@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")

    # This is where we change id:
    emit("connect",{"data":f"id: {request.sid} is connected"})

@socketio.on('data')
def handle_message(data):
    # Data reciever message, here deal with query parameters
    print("data from the front end: ",str(data))
    print(data)
    # Send response:
    emit("data",{'data':data,'id':request.sid},broadcast=True)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)


@socketio.on("tweet_view_explicit_day")
def tweet_view_explicit_day():
    # send dayview for explicit tweets
    data = {data:['123', '142', '421', '124']}
    emit("tweet_view_explicit_day", {'data':data,'id':request.sid}, broadcast=True)

@socketio.on("tweet_view_impicit_day")
def tweet_view_explicit_day():
    # send dayview for explicit tweets
    data = ['123', '142', '421', '124']
    emit("tweet_view_implicit_day", {'data':data,'id':request.sid}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True,port=5001)