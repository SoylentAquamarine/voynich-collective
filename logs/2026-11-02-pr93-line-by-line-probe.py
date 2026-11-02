import sys, os, csv, json, hashlib, io, contextlib, pathlib, tempfile
from unittest import mock
sys.path.insert(0, "os.environ.get("PR93_SCRIPTS", "data/scripts")")
import yale_ten_folio_native_fetch as kit
GOOD = bytes.fromhex("ffd8ffc000110800100010") + b"\x00"*20
SMALL = b"s"
def run(name, info=lambda u: {"width":16,"height":16}, native=lambda u: GOOD, drop=None):
    with tempfile.TemporaryDirectory() as t:
        t=pathlib.Path(t); (t/"r/research").mkdir(parents=True)
        m=t/"r/research/m.csv"; rc=t/"r/research/rc.csv"; tp=t/"r/research/tp.csv"
        with m.open("w",newline="") as fh:
            w=csv.DictWriter(fh,fieldnames=["folio_ids","canvas_index","iiif_1200px_url","sha256"]); w.writeheader()
            for i,f in enumerate(kit.FOLIOS):
                if f==drop: continue
                w.writerow({"folio_ids":f,"canvas_index":i,"iiif_1200px_url":f"https://x/iiif/2/{1000+i}/full/1200,/0/default.jpg","sha256":hashlib.sha256(SMALL).hexdigest()})
        def get(u,timeout=120):
            if u.endswith("info.json"): return json.dumps(info(u)).encode()
            if "/full/full/" in u: return native(u)
            return SMALL
        code=None
        with mock.patch.multiple(kit,REPO=str(t/"r"),MANIFEST=str(m),RECEIPT=str(rc),TEMPLATE=str(tp),get=get), \
             mock.patch.object(kit.time,"sleep",return_value=None), mock.patch.object(sys,"argv",["k","--image-dir",str(t/"img")]), \
             contextlib.redirect_stdout(io.StringIO()):
            try: kit.main()
            except SystemExit as e: code=e.code
            except Exception as e: code=f"UNCAUGHT {type(e).__name__}"
        errs=[r["error"] for r in csv.DictReader(l for l in rc.open() if not l.startswith("#"))] if rc.exists() else None
        print(f"{name}: exit={code} receipt={rc.exists()} template={tp.exists()} errs={[e for e in (errs or []) if e][:1]}")
run("baseline")
run("info width as string", info=lambda u: {"width":"16","height":"16"})
run("info missing dims", info=lambda u: {})
run("truncated native (SOI only)", native=lambda u: b"\xff\xd8\xff")
run("native downsampled vs info (maxWidth-style)", info=lambda u: {"width":32,"height":32})
run("SOF after SOS w/ stuffed 0xFF00 in scan", native=lambda u: bytes.fromhex("ffd8ffda0002ff00ffc000110800100010")+b"\x00"*20)
run("folio missing from manifest", drop="f50r")
