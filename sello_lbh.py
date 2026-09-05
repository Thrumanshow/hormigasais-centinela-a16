import hmac, hashlib, json, time, pathlib, os
SECRET=os.environ.get('LBH_SECRET','HormigasAIS-Soberano-A16-2025').encode()
for log in ['guardia_dia.log','guardia_nocturna.log','centinela_fondo.out']:
    p=pathlib.Path(log)
    if not p.exists() or p.stat().st_size==0: continue
    data=p.read_bytes()
    seal={
      "file": log,
      "sha256": hashlib.sha256(data).hexdigest(),
      "hmac_sha256": hmac.new(SECRET, data, hashlib.sha256).hexdigest(),
      "size": len(data),
      "issuer": "HormigasAIS-Ecosystem",
      "node": "A16",
      "timestamp": int(time.time()),
      "protocol": "LBH-v2.0",
      "parent_commit": "1d897b3",
      "temp_umbral": 39.0,
      "type": "swarm-log-diurno"
    }
    pathlib.Path(f"{log}.lbh.json").write_text(json.dumps(seal, indent=2))
    print(f"[LBH] {log} sellado {len(data)}B sha:{seal['sha256'][:10]}")
