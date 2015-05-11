[![Join the chat at https://gitter.im/cfelton/gizflo](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/cfelton/gizflo?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

NOTE:  This is a work in progress and has not reached a minor release 
point, yet.  The FPGA flow from 
[myhdl_tools](https://bitbucket.org/cfelton/myhdl_tools) has been 
moved to this project, the myhdl_tools version will not be updated, 
all future FPGA flow development will occur in this repository.



Introduction
============
The name of this project, *gizflo*, is a play on the the word 
gizmo.  It is intended to mean "that FPGA flow".  This project 
simplifies, the sometimes complicated, FPGA tool-chains. 
This tool was originally developed to automate the FPGA flow 
for FPGA designs implemented in [MyHDL](www.myhdl.org).  The
flow provides a one-button approach to the tool flow.

This project initiated as a quick tool to create a simple
tool-flow for an [FPGA workshop]
(http://www.fpgarelated.com/showarticle/437.php).  The tool-chain 
automation allowed the participants to start 
**hacking** an FPGA instantly (well, almost, you still need to 
go through the hassle to install the vendor tools).

This tool is intended to let developers easily map HDL designs to
FPGA development boards for quick analysis and allow the designer 
to focus on the HDL design and not the tool-flow.  The first version 
of the tool-flow existed in the [myhdl_tool]
(https://bitbucket.org/cfelton/myhdl_tools) 
package but it was eventually determined 
the tool-flow needed a separate project and moved here.

This project is built with [myhdl](www.myhdl.org) and can 
also be used to auto-majically map [myhdl](www.myhdl.org) designs to an FPGA 
development board.

*gizflo* goals
--------------

  * generate a large collection of board definitions [^1].

  * automate the FPGA tool-chains.

  * easily map [myhdl](www.myhdl.org) designs to a development board.


Example Usage
=============
This is how it works, simply retrieve a board based on the 
board name.  

```python
import gizflo as gf
brd = gf.get_board('xula2')
```

At this point three different paths can be taken:

  1. *Fuse*, given a board definition and a MyHDL top-level
     automatically match ports and execute the tool-flow.

  2. *Bootstrap*, generate a Verilog or VHDL stub and
     FPGA project files.

  <!-- extract -->
  3. *Map*, dynamically map HDL modules to external interfaces.
  
  4. *Stitching*, this uses generic wrappers to *stitch* 
     existing HDL cores together.    


Fuse 
----
Given a MyHDL top-level and a board definition find a
match for each port. 

```python
import gizflo as gf
brd = gf.get_board('xula2')
flow = brd.get_flow(top=m_blinky)
flow.run()
```

A *port* is the signal in the top-level HDL module and a *pin* is 
the physical pin on a device.  A board definition contains the 
default port names, if the HDL module port names match the default 
port names the names are matched.  If the port names do not match 
the ports can manually be added, linked, or renamed (added if the 
pin is known, linked if the default port name is known, or renamed 
if conflicts exist).

<!-- @todo: -->
Currently ports will only be matched by name, the goal of this 
functionality is to find a match for every port in the top-level,
this feature needs to be extended to find a best match if the 
names do not match.  In some scenarios this will not be possible, 
example if the top-level has too many ports, obviously they will 
not be matched with a board port definition.  Even if the port 
names do not match future functionality will find an appropriate 
match.  This allows quick prototyping and analysis of designs.


Bootstrap
---------
As mentioned, bootstrap will create a skeleton Verilog or
VHDL files to match the board definition.  Bootstrap will 
also create a default tool-chain (flow) project files.

```python
import gizflo as gf
brd = gf.get_board('xula2')
brd.bootstrap('verilog')
brd.bootstrap('vhdl')
```


<!-- 
 ** not sure about the name for this feature **
 This example should show how a module defines the HDL 
 based on the interfaces available.
-->

Map
---
Most designs require a minimal set of external interfaces but
many designs can utilize many different sets of interfaces.  
In this case 
the design determines which external interfaces it wants to 
utilize.  

<!-- 
  This example needs some more thought, the example 
  needs to capture mithro's intention, extracting 
  interfaces and building the design around the available
  interfaces.


```python
import gizflo as gf

# get a particular board
brd = gf.get_board('xula2')

# pass the board to the top-level, the top-level will 
# create the portmap, the "ports()" provides a dictionary
# of ports.
g = m_top_level(**brd.get_portmap())

# now the top-level determine which external interfaces
# to include, run the FPGA flow
brd.run(m_top_level)
```

```python
def m_top_level(brd=brd):
    
```

-->

Creating a Board Definition
===========================
The board definitions encapsulate majority of the information
needed for an FPGA project.  The board definition captures the
pins, timing information, and external interface.

A board definition can be created by defining the default ports.
The default ports are typically the pin names given in the 
manufactures documentation or schematics.

Example: XESS Xula2
-------------------
The following is a minimal example creating a board definition
for the [Xess Xula2](http://www.xess.com/shop/product/xula2-lx25/).

```python
class Xula2(_fpga):
      vendor = 'xilinx'
      family = 'spartan6'
      device = 'XC6SLX25'
      default_clocks = {'clock': dict(frequency=12e6, pins=('A9',)),
                        'chan_clk': dict(frequency=1e6, pins=('T7')
			}

      default_ports = {'chan': dict(pins=(
                                 'R7','R15','R16','M15','M16','K15',  #0-5
                                 'K16','J16','J14','F15','F16','C16', #6-11
                                 'C15','B16','B15','T4','R2','R1',    #12-17
                                 'M2','M1','K3','J4','H1','H2',       #18-23
                                 'F1','F2','E1','E2','C1','B1',       #24-29
                                 'B2','A2',) 
                      }

```

Creating External Interface Definitions
=======================================
Many FPGA development boards have similar peripherals on the boards, 
things like Ethernet PHYs, video PHYs, external memory, etc.  The 
external interfaces encapsulate the information required to configure
the interfaces (setting up the pins and constraints).  In some cases
defining an external interfaces is simply adding the common name and
associating the pins with the common port names for the interface.

<!--
Example: VGA
------------

Example: Ethernet
-----------------
-->

Work In Progress
================
This package has not met a 0.1 revision yet, the *fuse* option 
is fully implemented and the *bootstrap* and *map* are currently
being developed.

<!--
MyHDL Version
=============
Currently a modified version of the MyHDL package needs to be
utilized to use the *bootstrap* function.  A [MEP]() has been
created and the required feature should be incorporate soon.
Go [here]() and up-vote the issue to insensitive the addition.
-->


Notes
=====
[^1] explain why board definition is used, the whole thing about 
     FPGA instance but FPGA def is misleading, etc.

<!--
References
==========
-->
