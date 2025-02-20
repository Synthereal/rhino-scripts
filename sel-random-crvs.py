import rhinoscriptsyntax as rs

def thin_out_curves():
    # Step 1: Get the user's selection of curves
    curves = rs.GetObjects("Select curves to thin out", rs.filter.curve)
    if not curves or len(curves) < 2:
        print("You need to select at least 2 curves.")
        return

    # Step 2: Get the percentage of curves to delete (default to 50%)
    percentage = rs.GetReal("Enter percentage of curves to delete (0-100)", 50, 0, 100)
    if percentage <= 0:
        print("Percentage must be greater than 0.")
        return

    # Calculate how frequently to delete curves (spacing)
    spacing = max(1, int(100 / percentage))

    # Step 3: Delete every Nth curve based on spacing
    curves_to_delete = [curve for i, curve in enumerate(curves) if i % spacing == 0]

    # Step 4: Delete the selected curves
    rs.DeleteObjects(curves_to_delete)
    
    print("Deleted {} of {} curves ({}% thinned out).".format(len(curves_to_delete), len(curves), percentage))

if __name__ == "__main__":
    thin_out_curves()
