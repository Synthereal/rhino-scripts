import rhinoscriptsyntax as rs

def unroll_multiple_surfaces():
    # Prompt user to select multiple surfaces
    surfaces = rs.GetObjects("Select surfaces to unroll", rs.filter.surface)
    
    if not surfaces:
        print("No surfaces selected.")
        return
    
    # Deselect all objects at the start
    rs.UnselectAllObjects()
    
    # Loop through each surface, unroll with automated options
    for surface in surfaces:
        # Select the current surface
        rs.SelectObject(surface)
        
        # Run the UnrollSrf command with desired options (Explode=No)
        # '_Enter' simulates the completion of each command without any user interaction.
        rs.Command("_UnrollSrf _Explode=No _Enter", echo=False)
        
        # Unselect the surface after unrolling
        rs.UnselectObject(surface)
    
    print("Finished unrolling all selected surfaces.")

# Run the function
unroll_multiple_surfaces()
