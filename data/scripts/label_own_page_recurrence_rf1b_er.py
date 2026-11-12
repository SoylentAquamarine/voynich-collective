"""Sensitivity: rerun label_own_page_recurrence.py with the RF input named in the precommit (RF1b-er.txt).
Committed script and output are untouched; this writes a separate JSON."""
import importlib.util, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lop", HERE / "label_own_page_recurrence.py")
lop = importlib.util.module_from_spec(spec); spec.loader.exec_module(lop)
lop.pr.RF = lop.pr.ROOT / "data" / "RF1b-er.txt"
lop.OUT = lop.pr.ROOT / "data" / "derived" / "label-own-page-recurrence-rf1b-er.json"
lop.main()
