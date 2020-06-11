
import pya

layout = pya.Layout()


# Create Cell obj
UNIT = layout.create_cell("0_UNIT")


# Create layer #'s
l_1x1_outline = layout.layer(1, 0) # 1x1 Outline
l_metal = layout.layer(11, 0) # Metal


# Metal dimensions
line_width = 5*1000 # 10 um
pitch = 100*1000 # 100 um


# Draw outline
outline = UNIT.shapes(l_1x1_outline).insert( pya.Box(0, 0, pitch, pitch) ) 


# Draw metal legs
leg1 = UNIT.shapes(l_metal).insert( pya.Box(0, 0, line_width, pitch) ) 
leg2 = UNIT.shapes(l_metal).insert( pya.Box(0, pitch-line_width, pitch, pitch) ) 


# Export GDS
layout.write("0_unit_1x1.gds")
