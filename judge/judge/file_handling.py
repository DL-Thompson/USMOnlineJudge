import os
from judge import app
import time


SUCCESS_MESSAGE = "Congratulations! (sp?) Your code passed our tests in ways that make us happy!"
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
    results = None
    file_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    while not results:
        if os.path.exists(file_path+error):
            file_path += error
            file = open(file_path, 'r')
            if not file:
                continue
            results = ["There was an error in your submission.\n"]
            lines = file.readlines()
            for line in lines:
                results.append(clean(line.decode('utf-8')))
        elif os.path.exists(file_path+success):
            file_path += success
            with open(file_path, 'r') as f:
                for line in f:
                    print line
            results = [SUCCESS_MESSAGE]
        elif os.path.exists(file_path+incorrect):
            file_path += incorrect
            results = [INCORRECT_MESSAGE]
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