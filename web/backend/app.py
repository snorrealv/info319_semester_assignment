from flask import Flask, request,jsonify
from flask_socketio import SocketIO,emit
from flask_cors import CORS
import json

from kafka import KafkaConsumer, KafkaProducer
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

# ========================== emits ===========================



# ========================== events ==========================
@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data':'This is a big dummy'}
    return jsonify(data)

@socketio.on("connect")
def connected():
    print("client has connected")
    
    emit("connect",{"data":f"id: {request.sid} is connected"})
    # This is where we change id:
    

@socketio.on('data')
def handle_message(data):
    # Data reciever message, here deal with query parameters
    print("data from the front end: ",str(data))
    print(data)
    # Send response:
    emit("data",{'data':data,'id':request.sid},broadcast=True)

@socketio.on('query')
def handle_message(data):
    # Data reciever message, here deal with query parameters
    print("data from the front end: ",str(data))
    print(data)
    # Send response:
    emit("query",{'data':data,'id':request.sid},broadcast=True)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)

@socketio.on('givedata')
def handle_message(data):
    def stream_tweets():
        consumer = KafkaConsumer(bootstrap_servers='127.0.0.1:9092')
        consumer.subscribe(topics=['tweets_implicit'])
        try:
            # this method should auto-commit offsets as you consume them.
            # If it doesn't, turn on logging.DEBUG to see why it gets turned off.
            # Not assigning a group_id can be one cause
            for msg in consumer:
                # TODO: process the kafka messages.
                msg = json.loads(msg.value.decode())
                yield msg
        finally:
            # Always close your producers/consumers when you're done
            consumer.close()
    # data2 = {'data':[
    #                 {
    #                 'text':'#somebody',
    #                 'count':5,
    #                 'color':'green',
    #                 },
    #                 {
    #                 'text':'#once',
    #                 'count':4,
    #                 'color':'green',
    #                 },
    #                 {
    #                 'text':'#told me',
    #                 'count':3,
    #                 'color':'none',
    #                 },
    #                 {
    #                 'text':'#the world',
    #                 'count':3,
    #                 'color':'none',
    #                 },
    #                 {
    #                 'text':'#was gonna change me',
    #                 'count':3,
    #                 'color':'none',
    #                 },
    #                 {
    #                 'text':'#HillaryForJerusalem',
    #                 'count':3,
    #                 'color':'none',
    #                 },
    # ]}
    # emit("tweets", data2, broadcast=True)
    for tweet in stream_tweets():
        emit('tweets', {'data':tweet})

# @socketio.on("tweet_view_explicit_day")
# def tweet_view_explicit_day():
#     # send dayview for explicit tweets
#     data = {data:['123', '142', '421', '124']}
#     emit("tweet_view_explicit_day", {'data':jsonify(data),'id':request.sid}, broadcast=True)

# @socketio.on("tweet_view_impicit_day")
# def tweet_view_explicit_day():
#     # send dayview for explicit tweets
#     data = ['123', '142', '421', '124']
#     emit("tweet_view_implicit_day", {'data':data,'id':request.sid}, broadcast=True)
if __name__ == '__main__':
    socketio.run(app, debug=True,port=5001)