import os
from judge import app
import time

error = '-error'
success = '-success'


def save(text, filename):
    #saves the text from the code editor to a file in the upload directory
    directory = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file = open(directory, "w")
    file.write(text)
    file.close()

def get_results(ex_id, filename):
    results = None
    file_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    while not results:
        if os.path.exists(file_path+error):
            file_path += error
            file = open(file_path, 'r')
            if not file:
                continue
            results = file.readlines()
        elif os.path.exists(file_path+success):
            file_path += success
            file = open(file_path, 'r')
            if not file:
                continue
            results = file.readline()
    delete_file(file_path)
    if isinstance(results, "".__class__):
        return results
    elif type(results) is list:
        return '\n'.join(results)


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print "Error, can't delete: ", file_path

