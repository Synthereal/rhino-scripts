import rhinoscriptsyntax as rs

def arrange_surfaces_sequentially():
    # Prompt the user to select multiple surfaces
    surfaces = rs.GetObjects("Select surfaces to arrange sequentially", rs.filter.surface)
    
    if not surfaces:
        print("No surfaces selected.")
        return
    
    # Initialize the current X-offset for placing the next surface
    current_x_offset = 0
    
    # Deselect all objects at the start
    rs.UnselectAllObjects()
    
    # Loop through each surface
    for surface in surfaces:
        # Get the bounding box of the current surface
        bbox = rs.BoundingBox(surface)
        
        if bbox:
            # Calculate the width of the current surface
            surface_width = bbox[1].X - bbox[0].X
            
            # Move the surface to the correct position along the X-axis
            rs.MoveObject(surface, (current_x_offset - bbox[0].X, 0, 0))
            
            # Update the X-offset for the next surface
            current_x_offset += surface_width
    
    print("Surfaces have been arranged sequentially.")

# Run the function
arrange_surfaces_sequentially()
