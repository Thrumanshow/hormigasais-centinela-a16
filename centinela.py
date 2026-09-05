import time, json, os, sys
from datetime import datetime
TEMP_UMBRAL=float(os.getenv("TEMP_UMBRAL","39.0"))
LOG="guardia_dia.log"

def leer():
    import random
    return round(37.5+random.uniform(-1,3.5),1)

def emitir(tipo, detalle):
    f={"ts":time.time(),"datetime":datetime.now().isoformat(),"type":tipo,"detalle":detalle,"temp":detalle,"node":"A16","protocol":"LBH-v2.0","parent":"1d897b3"}
    open(LOG,"a").write(f"🌡️ {json.dumps(f)}\n")
    print(f"🔥 {detalle}" if "ACTIVO" in tipo else f"🐜 {detalle}", flush=True)

def fondo():
    intervalo=300  # base 5min
    print(f"🐜 FONDO 39°C cada {intervalo}s {datetime.now()} [anti-bucle ON]", flush=True)
    while True:
        t=leer()
        if t >= 40.0:  # sobrecalentado = enfría centinela
            intervalo=900  # baja a 15min
            emitir("ALERTA_TEMP_DIA", f"ENJAMBRE ACTIVO {t}°C >= {TEMP_UMBRAL}°C | backoff 900s para no calentar")
        elif t >= 39.0:
            intervalo=600  # 10min en umbral
            emitir("ALERTA_TEMP_DIA", f"ENJAMBRE ACTIVO {t}°C >= {TEMP_UMBRAL}°C | intervalo {intervalo}s")
        elif t >= 37.5:
            intervalo=300
            emitir("PRE_ALERTA_TEMP", f"Pre {t}°C -> {TEMP_UMBRAL}°C")
        else:
            intervalo=300
            emitir("OK_DIA", f"Estable {t}°C")
        time.sleep(intervalo)

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("--fondo",action="store_true"); a=ap.parse_args()
    fondo() if a.fondo else fondo()
