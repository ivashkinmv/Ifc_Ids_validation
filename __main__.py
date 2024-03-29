#!/usr/bin/env python3


import time
import ifcopenshell
import ids
import reporter


start = time.time()

specs = ids.open(r"C:/test_IDS/ids/TSGE_TSIM_RII_1_0_Atributivnyy-sostav.ids")
ifc = ifcopenshell.open(r"C:/test_IDS/ifc/Ю35-9__К10_Р_КР_тестIDS.ifc")
print(specs, ifc)
print("Finished loading:", time.time() - start)
start = time.time()
specs.validate(ifc)

print("Finished validating:", time.time() - start)
start = time.time()


engine = reporter.Html(specs)
engine.report()
engine.to_file("report4.html")


