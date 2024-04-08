#!/usr/bin/env python3
#

import time
import ifcopenshell
import ids
import reporter


start = time.time()

specs = ids.open(r"IDS.ids")
ifc = ifcopenshell.open(r"IDS.ifc")
print(specs, ifc)
print("Finished loading:", time.time() - start)
start = time.time()
specs.validate(ifc)

print("Finished validating:", time.time() - start)
start = time.time()


engine = reporter.Html(specs)
engine.report()
engine.to_file("report4.html")


