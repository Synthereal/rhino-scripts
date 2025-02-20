import rhinoscriptsyntax as rs

def select_smallest_surfaces():
    # Step 1: Get the collection of surfaces
    surfaces = rs.GetObjects("Select surfaces to process", rs.filter.surface)
    if not surfaces:
        print("No surfaces selected.")
        return

    # Step 2: Ask user for the percentage of smallest surfaces to select
    percentage = rs.GetReal("Enter the percentage of smallest surfaces to select (0-100%)", 10, 0, 100)
    if percentage <= 0 or percentage > 100:
        print("Invalid percentage value.")
        return

    # Step 3: Calculate areas of surfaces and store them along with their IDs
    surfaces_with_areas = [(surface, rs.SurfaceArea(surface)[0]) for surface in surfaces]
    surfaces_with_areas.sort(key=lambda x: x[1])  # Sort by area (smallest first)

    # Step 4: Determine the number of surfaces to select
    num_to_select = int((percentage / 100.0) * len(surfaces_with_areas))

    # Step 5: Select the smallest surfaces
    smallest_surfaces = [surface for surface, area in surfaces_with_areas[:num_to_select]]
    rs.SelectObjects(smallest_surfaces)

    print("Selected {} surfaces.".format(len(smallest_surfaces)))

if __name__ == "__main__":
    select_smallest_surfaces()
