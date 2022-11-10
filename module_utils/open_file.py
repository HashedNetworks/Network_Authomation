""" Function to open a file """

def open_filename(filename):
    with open(filename, 'r') as filehandle:
        data = filehandle.read()
        print ("ORIGINAL FILE FORMAT: \n")
        print(data)
        return data
