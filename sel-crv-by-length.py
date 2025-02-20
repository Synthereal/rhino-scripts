import rhinoscriptsyntax as rs

def select_shortest_curves():
    # Get the collection of curves
    curves = rs.GetObjects("Select curves to process", rs.filter.curve)
    if not curves:
        print("No curves selected.")
        return

    # Ask user for the percentage of shortest curves to select
    percentage = rs.GetReal("Enter the percentage of shortest curves to select (0-100%)", 10, 0, 100)
    if percentage <= 0 or percentage > 100:
        print("Invalid percentage value.")
        return

    # Calculate lengths of curves and store them along with their IDs
    curves_with_lengths = [(curve, rs.CurveLength(curve)) for curve in curves]
    curves_with_lengths.sort(key=lambda x: x[1])  # Sort by length (shortest first)

    # Determine the number of curves to select
    num_to_select = int((percentage / 100.0) * len(curves_with_lengths))

    # Select the shortest curves
    shortest_curves = [curve for curve, length in curves_with_lengths[:num_to_select]]
    rs.SelectObjects(shortest_curves)

    print("Selected {} curves.".format(len(shortest_curves)))

if __name__ == "__main__":
    select_shortest_curves()
