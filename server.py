import asyncio 
import random 
import json
import sqlite3
conn=sqlite3.connect("dice.db")
cursor=conn.cursor()
create="""
CREATE TABLE IF NOT EXISTS login_data(
id INTEGER PRIMARY KEY AUTOINCREMENT
login TEXT NOT NULL
passworld TEXT NOT NULL,
passord TEXT NOT NULL
)
"""
HOST,PORT="0.0.0.0",8080
cursor.execute(create_table)
clients=[]
async def add_user(login,password):
    query="""
    SELECT login
    FROM login_data
    WHERE login=?
    """
    cursor.execute(query,(login))
    rows=cursor.fetchall()
    if not rows:
        query="""
        INSERT INTO login_data(login,password)VALUES(?,?)
        """
        cursor.execute(query,(login,password))
        conn.commit
        return json.dumps({"respond":"success"})
    else:
        return json.dumps({"respond":"user alredy exists"})
async def broadcast(msg):
    for writer, _ in clients:
        try:
            writer.write((msg+"\n").encode())
            await writer.drain()
        except:
            pass
async def client_handler(reader,writer):
    data=await reader.read(1024)
    msg=json.loads(data.decode().strip())
    name=msg.get("name")
    clients.append((writer,name))

    print(f"[SERVER] connected{name}")
    await broadcast(f"{name} connect to game")

    try:
        while True:
            data=await reader.readline()
            if not data:
                break
            msg=data.decode().strip()
            cmd=json.loads(msg).get("cmd")
            if cmd=="roll":
                roll=random.randint(1,6)
                await broadcast(f"{name} got: {roll}")
            elif msg.get("cmd").lower()=="add_user":
                login,password=msg.get("login"),msg.get("password")
                respond=await add_user(login,password)
                writer.write(respond.encode())
                await writer.drain
    except:
        pass
async def main():
    server=await asyncio.start_server(None,HOST,PORT)
    print(f"[server] Listen on {HOST}:{PORT}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())