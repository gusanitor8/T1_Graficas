import re

def read(filename):    
    string = ""

    with open(filename, 'r') as f:
        string = str(f.read())

    return toSplit(string)
    
def toSplit(input_string):
    pattern = r"\(\d+,\s*\d+\)"  # Regular expression to match tuples
    tuples_list = re.findall(pattern, input_string)
    return get_array(tuples_list)

def get_array(array):
    pointsArray = []
    for element in array:
        element = element.strip("()")
        points = element.split(",")
        points[1] = int(points[1].strip())
        points[0] = int(points[0].strip())
        pointsArray.append(points)
    return pointsArray
