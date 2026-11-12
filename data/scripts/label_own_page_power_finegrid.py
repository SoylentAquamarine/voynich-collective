"""Disclosed POST-HOC extension (not precommitted): finer low-q grid, because the precommitted grid hit power 1.0 at its first nonzero point."""
import importlib.util,sys
spec=importlib.util.spec_from_file_location("pw","/home/claude/voynich-collective/data/scripts/label_own_page_power.py")
pw=importlib.util.module_from_spec(spec);spec.loader.exec_module(pw)
pw.QS=[0.0025,0.005,0.0075,0.01,0.0125,0.015,0.0175]
pw.OUT=pw.ROOT/"data"/"derived"/"label-own-page-power-finegrid.json"
pw.main()
