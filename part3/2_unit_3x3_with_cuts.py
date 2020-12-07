
import os
root = os.path.dirname( os.path.abspath(__file__) )

# Create KLayout object
import pya
KLAYOUT = pya.Layout()

# Dimensions
pitch = 100*1000 # 100 um

# Create Top Cell Name & Obj of the GDS to be EXPORTED
TOP_CELL = KLAYOUT.create_cell("1_UNIT_CUTS")

# Define array of GDS files to read
gds_files = [ "1_unit_3x3.gds" ]

# Define layer #'s
l_metal     = KLAYOUT.layer(11, 0) # Metal
l_cut_box   = KLAYOUT.layer(8, 0) # Cut Box

# Define dimensions
dim = {
  "line_width": 5*1000, # 5 um
  "cut_width": 5*1000, # 5 um
  "pitch": 100*1000, # 100 um
}

# Define cut locations
cut_loc = {
    "1_unit_3x3_with_cuts" : [ 
        "7_t", "8_l", "9_t",
        "4_t",        "6_l",
        "1_l", "2_t", "3_t",
    ]
}


def main():

    # Loop each cut locations, & assign GDS name from key
    for key in cut_loc:
        filename = key
        print ( "\nfilename : ", filename )
    
        # Read 1_UNIT (no cuts as a reference) & create SINGLE instance
        for each_gds in gds_files:
            KLAYOUT.read(each_gds)

            # Read Top Cell for each GDS file
            for top_cell_read in KLAYOUT.top_cells():
                if (top_cell_read.name != "1_UNIT_CUTS"): # Don't insert TOP_CELL("1_UNIT_CUTS") on itself
                    # print ( "Adding " + top_cell_read.name )
                    cell_index = top_cell_read.cell_index()
                    new_instance=pya.CellInstArray( cell_index, pya.Trans(pya.Point(0,0)) )
                        # pya.Trans(pya.Point(0,0)) --> defines the LOCATION at which instance should be placed
                    TOP_CELL.insert( new_instance )
    
        # Define imported metal as a region (for boolean)
        region_metal = pya.Region( KLAYOUT.top_cell().begin_shapes_rec(l_metal) )

        # Define cut area & make as region
        for ind, each_cut in enumerate(cut_loc[key]):
            cut_box_coord = get_cut_coord( each_cut, dim )
            TOP_CELL.shapes(l_cut_box).insert( cut_box_coord ) 
            region_cut_box = pya.Region( cut_box_coord )   
            # Do boolean (XOR)
            # For more than 1 cuts, need to loop and take XOR of previous XOR results
            if ind == 0:
                region_xor = region_metal ^ region_cut_box
            else:
                region_xor = region_xor ^ region_cut_box

        # Remove existings metal layer + cut boxes
        # (!!! SKIP THIS TO CHECK CUT BOXES IN GDS !!!)
        KLAYOUT.clear_layer(l_metal)
        KLAYOUT.clear_layer(l_cut_box)    

        # INSERT BOOLEAN RESULT AS ORIGINAL METAL LAYER
        TOP_CELL.shapes(l_metal).insert(region_xor)

        # Check if filename gds exists -> If so skip "write"
        if os.path.isfile( root+"/"+filename+".gds" ):
            print ("**** GDS name by : "+filename+".gds already exists!" )
            print ("**** SKIPPING GDS WRITE!!!" )
        else:
            # Export GDS
            KLAYOUT.write( filename+".gds" )
    

def get_cut_coord( each_cut_s, dim ):
    # First, get COL number from name ("2_l")
    if "1" in each_cut_s or "4" in each_cut_s or "7" in each_cut_s:
        col = 0
    elif "2" in each_cut_s or "5" in each_cut_s or "8" in each_cut_s:
        col = 1
    elif "3" in each_cut_s or "6" in each_cut_s or "9" in each_cut_s:
        col = 2
    
    # Next, get ROW number from name ("2_l")
    if "1" in each_cut_s or "2" in each_cut_s or "3" in each_cut_s:
        row = 0
    elif "4" in each_cut_s or "5" in each_cut_s or "6" in each_cut_s:
        row = 1
    elif "7" in each_cut_s or "8" in each_cut_s or "9" in each_cut_s:
        row = 2
        
    # Get location info from name ("2_l")
    # (pre-define some of re-used coordinates here)
    l_x1 = dim["pitch"]*col
    l_x2 = dim["pitch"]*col + dim["cut_width"]
    l_y1 = dim["pitch"]*row + (dim["pitch"]/2 - dim["cut_width"]/2)
    l_y2 = dim["pitch"]*row + (dim["pitch"]/2 + dim["cut_width"]/2)
    
    t_x1 = dim["pitch"]*col + (dim["pitch"]/2 - dim["cut_width"]/2)
    t_x2 = dim["pitch"]*col + (dim["pitch"]/2 + dim["cut_width"]/2)
    t_y1 = dim["pitch"]*row + (dim["pitch"] - dim["cut_width"])
    t_y2 = dim["pitch"]*row + dim["pitch"]
  
      
    if "l" in each_cut_s:
        cut_box = pya.Box( l_x1, l_y1, l_x2, l_y2 ) 
    elif "t" in each_cut_s:
        cut_box = pya.Box( t_x1, t_y1, t_x2, t_y2 ) 
    else:
        print ("NO cut name such as : ", each_cut_s )
    
    return cut_box


if __name__ == '__main__':
  main()