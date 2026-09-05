# hormigasais-centinela-a16
Centinela diurno 39°C - Nodo A16 Soberano
Parent: hormigasais-site 1d897b3 | Audio star4 61.78KB sellado LBH v2.0

Umbral trabajo enjambre: 39.0°C (no 48°C)
Modo fondo: python3 -u centinela.py --fondo cada 300s

Comandos:
- Un chequeo: python3 -u centinela.py --vigilar
- Fondo: ./enjambre_fondo.sh && tail -f centinela_fondo.out
- Análisis 24h: python3 -u centinela.py --analizar-24h
- Sello LBH: python3 sello_lbh.py

Logs sellados con parent_commit 1d897b3
