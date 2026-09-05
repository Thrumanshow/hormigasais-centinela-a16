#!/data/data/com.termux/files/usr/bin/bash
cd ~/hormigasais-centinela-a16
echo "🐜 Lanzando 39°C sin buffer..."
nohup python3 -u centinela.py --fondo > centinela_fondo.out 2>&1 &
echo $! > centinela.pid
sleep 1
echo "PID $(cat centinela.pid)"
tail -n 20 centinela_fondo.out
