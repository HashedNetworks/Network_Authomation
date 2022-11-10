""" Function to open a file """

def open_filename(filename):
    """ Function to open a file and loaded it into a variable

    Args:
        filename (str): filename with input data that will be converted to Python object

    Returns:
        dict: input data to convert
    """
    with open(filename, 'r') as filehandle:
        data = filehandle.read()
        print ("ORIGINAL FILE FORMAT: \n")
        print(data)
        return data
