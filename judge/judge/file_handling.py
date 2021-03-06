import os
from judge import app
import time


SUCCESS_MESSAGE = "Congratulations! Your code passed our tests in ways that make us happy!"
INCORRECT_MESSAGE = "We're sorry, your princess is in another realm of time and space's castle. In other words, nope."

error = '-error'
success = '-success'
incorrect = '-incorrect'


def save(text, filename):
    #saves the text from the code editor to a file in the upload directory
    directory = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file = open(directory, "w")
    file.write(text)
    file.close()


def get_results(filename):
    results = {}
    file_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    while not results:
        if os.path.exists(file_path+error):
            file_path += error
            file = open(file_path, 'r')
            if not file:
                continue
            results['message'] = "There was an error in your submission.\n"
            lines = file.readlines()
            errors = []
            for line in lines:
                errors.append(clean(line.decode('utf-8')))
            results['errors'] = errors
        elif os.path.exists(file_path+success):
            file_path += success
            with open(file_path, 'r') as f:
                m = None
                t = None
                for line in f:
                    if "Time:" in line:
                        for st in line.split():
                            try:
                                t = float(st)
                            except ValueError:
                                pass
                    if "Memory:" in line:
                        for st in line.split():
                            try:
                                m = float(st)
                            except ValueError:
                                pass
                if not t:
                    t = 0
                if not m:
                    m = 0
            results['message'] = SUCCESS_MESSAGE
            results['time'] = t
            results['memory'] = m
        elif os.path.exists(file_path+incorrect):
            file_path += incorrect
            results['message'] = INCORRECT_MESSAGE
    delete_file(file_path)
    return results


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print "Error, can't delete: ", file_path


def clean(error_line):
    # cleans out the file path on the server from displaying
    cleaned = ""
    split = error_line.split(':')
    firstSplit = True
    for s in split:
        if firstSplit:
            firstSplit = False
            continue
        cleaned += s + ":"

    return cleaned