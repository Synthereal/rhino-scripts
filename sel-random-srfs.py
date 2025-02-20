import rhinoscriptsyntax as rs

def thin_out_surfaces():
    # Step 1: Get the user's selection of surfaces
    surfaces = rs.GetObjects("Select surfaces to thin out", rs.filter.surface)
    if not surfaces or len(surfaces) < 2:
        print("You need to select at least 2 surfaces.")
        return

    # Step 2: Get the percentage of surfaces to select (default to 50%)
    percentage = rs.GetReal("Enter percentage of surfaces to select (0-100)", 50, 0, 100)
    if percentage <= 0:
        print("Percentage must be greater than 0.")
        return

    # Calculate how frequently to select surfaces (spacing)
    spacing = max(1, int(100 / percentage))

    # Step 3: Select every Nth surface based on spacing
    surfaces_to_select = [surface for i, surface in enumerate(surfaces) if i % spacing == 0]

    # Step 4: Select the chosen surfaces
    rs.UnselectAllObjects()  # Clear any previous selections
    rs.SelectObjects(surfaces_to_select)
    
    print("Selected {} of {} surfaces ({}% selected).".format(len(surfaces_to_select), len(surfaces), percentage))

if __name__ == "__main__":
    thin_out_surfaces()
