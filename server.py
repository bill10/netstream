from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
from collections import deque
import pandas as pd
import random

queue=deque();
df=pd.read_csv('data/AllYearsReport.csv')
df.loc[df['Organization Name'].isnull(),'Organization Name']="Unknown"

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print("User connected!")
    queue.clear()
    node2id={}
    edges=set()
    N=0
    E=0
    for t in sorted(df['Year'].unique()):
        queue.append({'title': str(t)})
        df2=df[df['Year']==t]
        for i in xrange(df2.shape[0]):
            s=df2.iloc[i]['Contact PI / Project Leader']
            t=df2.iloc[i]['Organization Name']
            if s not in node2id:
                N+=1
                node2id[s]=str(N)
                if t not in node2id:
                    N+=1
                    node2id[t]=str(N)
                    queue.append({'aenn': {'source': {'id': node2id[s], 'label': s, 'size': 1, 'color': '#43a2ca'},
                                           'target': {'id': node2id[t], 'label': t, 'size': 1, 'color': '#C32148'}}})
                else:
                    queue.append({'aen': {'new': {'id': node2id[s], 'label': s, 'size': 1, 'color': '#43a2ca'},
                                          'old': node2id[t],
                                          'source': node2id[s], 'target': node2id[t]}})
                edges.add(node2id[s]+'_'+node2id[t])
            else:
                if t not in node2id:
                    N+=1
                    node2id[t]=str(N)
                    queue.append({'aen': {'new': {'id': node2id[t], 'label': t, 'size': 1, 'color': '#C32148'},
                                          'old': node2id[s],
                                          'source': node2id[s], 'target': node2id[t]}})
                    edges.add(node2id[s]+'_'+node2id[t])
                else:
                    queue.append({'ae': {'source': node2id[s], 'target': node2id[t]}})

@socketio.on('GET')
def handle_message(message):
    if queue:
        data=queue.popleft()
        for key in data:
            emit(key, data[key])
            break
    else:
        emit('none','')

if __name__ == '__main__':
    socketio.run(app)
