EETools
=======

This is serioulsy just a scrap repository to keep some of the scripts I use for electrical engineering tasks organized.  There's no real rhyme or reason, just a storage bin for anything I found useful doing circuit design.

eetools.netlist
---------------
Reads netlists in TANGO format.  No reason to prefer tango, other than it's something that Altium Designer actually spits out.  Use it thus:

```python
netlist = eetools.netlist.load('file.net')

for net_name in netlist.nets:
    print net_name
```

or, if you like, you can create a new netlist from scratch:

```python
# Create a netlist with a single resistor that's shorted out
netlist = eetools.netlist.Netlist()
netlist.add_component('R1')
netlist.add_to_net('NET_1', 'R1', 1)
netlist.add_to_net('NET_1', 'R1', 2)
```

eetools.pin_planner
-------------------
eetools.pin_planner is a gem, but is kind of a mess.  It lets you load a microcontroller pin map (in a currently undocumented awful format) and create a pin plan, detailing how each pin will be used.  The module can be used interactively, so pins can be claimed and unclaimed in real-time, easing the hassle of planning the pin utilization in a complex microcontroller design.  The module also provides convenient queries, so that pin constraints can be examined, and resolved
more easily.

Without having to clean it up or explain myself, check out the source, as well as the `examples/pin_planner.py`

eetools.eia
-----------
The eetools.eia package keeps some static lists of standard EIA component values, as well as provides some convenient functions for searching and accessing them.  Examples!

```python
from eetools.eia import one_percent_resistors as res

# I need a 221 ohm resistor
print res.nearest(221.0)

# If I'm desigining a circuit, and I want to err on one side or the other
print res.nearest_above(221.0)
print res.nearest_below(221.0)

