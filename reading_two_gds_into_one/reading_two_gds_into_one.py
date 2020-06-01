# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
'''
Summary
- [1] Create TOP layout (LAYOUT_TOP, where layouts A & B would be merged)
- [2] Create two separate layouts (LAYOUT_A, LAYOUT_B), and read each GDS
- [3] In TOP layout, create two (empty) target cells (ta, tb) 
- [4] From [3], copy over the layouts from A to TA, using ta.move_tree(layout_A.top_cell() )
- [5] From [3], copy over the layouts from B to TB, using tb.move_tree(layout_B.top_cell() )
'''
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Pitch of cells (to be placed as instances)
p = 288*1000 # um (x1000 to convert nm -> um)


import pya


# [1]
LAYOUT_TOP = pya.Layout()
CELL_TOP = LAYOUT_TOP.create_cell("CELL_TOP")


# [2]
LAYOUT_A = pya.Layout()
LAYOUT_A.read( "first.gds" )

LAYOUT_B = pya.Layout()
LAYOUT_B.read( "second.gds" )


# [3]
CELL_TA = LAYOUT_TOP.create_cell("CELL_TA")
CELL_TOP.insert( pya.CellInstArray( CELL_TA.cell_index(), pya.Trans(pya.Point( p*(1-1), p*(1-1) )) ) )

CELL_TB = LAYOUT_TOP.create_cell("CELL_TB")
CELL_TOP.insert( pya.CellInstArray( CELL_TB.cell_index(), pya.Trans(pya.Point( p*(2-1), p*(1-1) )) ) )

	# (x,y) coordinates of the instance placement is defined by :
	# pya.Trans( pya.Point( p*(x-1), p*(y-1) ))
	# "p" is used to define placement in units of pitch


# [4] & [5]
CELL_TA.move_tree( LAYOUT_A.top_cell() )
CELL_TB.move_tree( LAYOUT_B.top_cell() )


# Export GDS
LAYOUT_TOP.write( "3_PANEL_test.gds" )