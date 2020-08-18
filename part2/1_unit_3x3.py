
# Create KLayout object
import pya
KLAYOUT = pya.Layout()

# Dimensions
pitch = 100*1000 # 100 um

# Create Top Cell Name & Obj of the GDS to be EXPORTED
TOP_CELL = KLAYOUT.create_cell("1_UNIT")

# Define array of GDS files to read
gds_files = [ "0_unit_1x1.gds" ]

# Read each GDS files
for each_gds in gds_files:
  KLAYOUT.read(each_gds)

  # Read Top Cell for each GDS file
  for top_cell_read in KLAYOUT.top_cells():
      if (top_cell_read.name != "1_UNIT"): # Don't insert TOP_CELL("1_UNIT") on itself
          # print ( "Adding " + top_cell_read.name )
          cell_index = top_cell_read.cell_index()
          new_instance = pya.CellInstArray( cell_index, pya.Trans(pya.Point(0,0)), pya.Vector(pitch, 0), pya.Vector(0, pitch), 3, 3 )
              # pya.Trans(pya.Point(0,0)) --> defines the LOCATION at which instance should be placed
              # pya.Vector(pitch, 0) --> defines the PITCH at which instance should repeat
              # 3, 3 --> defines number of repeats
          TOP_CELL.insert( new_instance )


# Create layer #'s
l_3x3_outline = KLAYOUT.layer(3, 0) # 3x3 Outline

# Draw outline (of 3x3)
TOP_CELL.shapes(l_3x3_outline).insert( pya.Box(0, 0, 3*pitch, 3*pitch) ) 

# Export GDS
KLAYOUT.write("1_unit_3x3.gds")