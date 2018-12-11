nohup python3 -u server.py 9000 > client1.log 2>&1 &
nohup python3 -u server.py 9001 > client2.log 2>&1 &
python3 competition.py
