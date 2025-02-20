import rhinoscriptsyntax as rs
import random
import math

# Editable variables
num_points = 48  # Total number of points to generate
min_distance = 0.5  # Minimum distance (radius) between points in inches

def is_far_enough(point, existing_points, min_distance):
    """
    Checks if a point is at least `min_distance` away from all points in `existing_points`.
    """
    for other_point in existing_points:
        distance = math.sqrt((point[0] - other_point[0])**2 + (point[1] - other_point[1])**2)
        if distance < min_distance:
            return False
    return True

def fill_polygon_with_random_points_no_overlap(num_points, min_distance):
    """
    Prompts the user to select a closed polygon and fills it with evenly distributed random points
    without overlaps in 4 equal sections (2x2 grid). Groups all points at the end.
    """
    polygon = rs.GetObject("Select a closed polygon to fill with random points", rs.filter.curve)
    if not polygon or not rs.IsCurveClosed(polygon):
        print("Error: The selected object is not a closed polygon.")
        return None

    bbox = rs.BoundingBox(polygon)
    if not bbox:
        print("Error: Could not calculate the bounding box.")
        return None

    min_x = bbox[0][0]
    max_x = bbox[1][0]
    min_y = bbox[0][1]
    max_y = bbox[3][1]

    x_step = (max_x - min_x) / 2
    y_step = (max_y - min_y) / 2
    sections = [
        ((min_x, min_y), (min_x + x_step, min_y + y_step)),
        ((min_x + x_step, min_y), (max_x, min_y + y_step)),
        ((min_x, min_y + y_step), (min_x + x_step, max_y)),
        ((min_x + x_step, min_y + y_step), (max_x, max_y)),
    ]

    points_per_section = num_points // 4
    remainder_points = num_points % 4
    random_points = []

    for i, section in enumerate(sections):
        (sec_min, sec_max) = section
        sec_min_x, sec_min_y = sec_min
        sec_max_x, sec_max_y = sec_max

        points_to_generate = points_per_section + (1 if i < remainder_points else 0)

        for _ in range(points_to_generate):
            for attempt in range(200):
                x = random.uniform(sec_min_x, sec_max_x)
                y = random.uniform(sec_min_y, sec_max_y)
                z = 0
                point = (x, y, z)
                if rs.PointInPlanarClosedCurve(point, polygon) and is_far_enough(point, random_points, min_distance):
                    random_points.append(point)
                    break
            else:
                print("Failed to place a point in this section after 200 attempts.")

    created_points = []
    for point in random_points:
        created_points.append(rs.AddPoint(point))

    group_name = "GeneratedPointsGroup"
    rs.AddGroup(group_name)
    rs.AddObjectsToGroup(created_points, group_name)

    print("Generated {} random points inside the polygon and grouped them as '{}'.".format(len(created_points), group_name))
    return polygon, bbox, created_points

def connect_and_extend_lines(points, bbox):
    """
    Connects points starting with the bottom-leftmost point, creates lines, and extends both ends
    of each line to the bounding box.
    """
    bbox_curve = rs.AddPolyline(bbox + [bbox[0]])
    points_coords = [rs.PointCoordinates(point) for point in points]
    points_coords.sort(key=lambda p: (p[1], p[0]))  # Sort by bottom-left (y, then x)

    lines = []
    while len(points_coords) > 1:
        base_point = points_coords.pop(0)
        closest_point = None
        closest_distance = float('inf')

        for point in points_coords:
            distance = math.sqrt((base_point[0] - point[0])**2 + (base_point[1] - point[1])**2)
            if distance < closest_distance:
                closest_point = point
                closest_distance = distance

        if closest_point:
            line = rs.AddLine(base_point, closest_point)
            lines.append(line)
            points_coords.remove(closest_point)

    # Extend both ends of each line to the bounding box
    for line in lines:
        rs.ExtendCurve(line, 0, 0, [bbox_curve])  # Extend start
        rs.ExtendCurve(line, 0, 1, [bbox_curve])  # Extend end

    group_name = "ExtendedLinesGroup"
    rs.AddGroup(group_name)
    rs.AddObjectsToGroup(lines, group_name)

    print("Generated and extended {} lines and grouped them as '{}'.".format(len(lines), group_name))
    rs.DeleteObject(bbox_curve)
    return lines

def main():
    """
    Main function to run the script.
    """
    print("Running script...")

    polygon, bbox, points = fill_polygon_with_random_points_no_overlap(num_points, min_distance)
    if not points or not polygon:
        print("No points or polygon generated.")
        return

    extended_lines = connect_and_extend_lines(points, bbox)

if __name__ == "__main__":
    main()
