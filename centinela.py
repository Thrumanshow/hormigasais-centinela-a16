import time, json, os, argparse, pathlib, sys
from datetime import datetime
try:
    from dotenv import load_dotenv
    load_dotenv()
except: pass
GATEWAY_IP=os.getenv("GATEWAY_IP","192.168.1.1")
TEMP_UMBRAL=float(os.getenv("TEMP_UMBRAL","39.0"))
INTERVALO=int(os.getenv("INTERVALO_SEG","60")) # 60s para prueba, luego 300
LOG_DIA="guardia_dia.log"

def emitir(tipo, detalle):
    f={"timestamp":time.time(),"datetime":datetime.now().isoformat(),"type":tipo,"origin":"nodo_a16_centinela_dia","status":"warning" if "ALERTA" in tipo else "info","detalle":detalle,"node":"A16","protocol":"LBH-v2.0","parent":"1d897b3","temp_umbral":TEMP_UMBRAL}
    with open(LOG_DIA,"a",encoding="utf-8") as log:
        log.write(f"🌡️ [XOXO-BUS-DIA] {json.dumps(f, ensure_ascii=False)}\n")
    print(f"{'🔥' if 'ALERTA' in tipo else '🐜'} {detalle}", flush=True)

def leer_router():
    import random
    return round(37.5+random.uniform(-1,3.5),1), round(-24+random.uniform(-4,1),1)

def vigilar_once():
    temp, rx = leer_router()
    if temp >= TEMP_UMBRAL: emitir("ALERTA_TEMP_DIA", f"ENJAMBRE ACTIVO {temp}°C >= {TEMP_UMBRAL}°C")
    elif temp >= 37.0: emitir("PRE_ALERTA_TEMP", f"Pre {temp}°C -> {TEMP_UMBRAL}°C")
    else: emitir("OK_DIA", f"Estable {temp}°C / {rx}dBm")
    return temp

def vigilar_fondo():
    print(f"🐜 FONDO 39°C cada {INTERVALO}s iniciado {datetime.now()}", flush=True)
    while True:
        try:
            vigilar_once()
            if int(time.time()) % 600 < INTERVALO: 
                os.system("python3 sello_lbh.py")
        except Exception as e:
            emitir("ERROR", str(e))
        sys.stdout.flush()
        time.sleep(INTERVALO)

def analizar_24h():
    p=pathlib.Path(LOG_DIA)
    if not p.exists(): print("Sin log"); return
    lines=p.read_text().splitlines()
    alertas=[l for l in lines if "ALERTA_TEMP_DIA" in l]
    print(f"📊 24H: {len(lines)} regs | 🔥 {len(alertas)} veces >=39°C | Último: {lines[-1][-120:] if lines else ''}")

if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--vigilar", action="store_true")
    ap.add_argument("--fondo", action="store_true")
    ap.add_argument("--analizar-24h", action="store_true")
    a=ap.parse_args()
    if a.analizar_24h: analizar_24h()
    elif a.fondo: vigilar_fondo()
    else: vigilar_once()
