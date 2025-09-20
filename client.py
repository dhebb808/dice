from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock 

import socket 
import threading
import json 

HOST,PORT="127.0.0.1",8080

class DiceApp(App):
    def build(self):
        self.socket=socket.socket 
        self.socket.connect((HOST,PORT))
        self.player_name="petro"

        msg=json.dumps({"name":self.player_name})
        self.socket.send(msg.encode())

        self.layout=BoxLayout(orientation="vertical")
        self.log=Label(text="log:\n",size_hint_y=0.8)

        self.button=Button(text="roll dice",size_hint_y=0.2)
        self.button.bind(on_press=None)

        self.layout.add_widget(self.log)
        self.layout.add_widget(self.button)

        return self.layout
    
    def roll(self,instance):
        try:
            msg={"name":self.player_name,"cmd":"roll"}
            self.sock.send(json.dumps(msg).encode())
        except:
            pass
    
    def listen_server(self):
        while True:
            try:
                data=self.sock.recv(1024)
                if not data:
                    break 
                msg=json.loads(data.decode())
                Clock.schedule_once(lambda dt:self.update.log(f"{msg["name"]}-{msg["result"]}"))
            except:
                pass
    def update_log(self,msg):
        self.log.text+=msg+"\n"