import os
from judge import app
from database import production_env
import prod_cfg
import dev_cfg
import time

if production_env:
    RESULTS_FOLDER = prod_cfg.results_folder
else:
    RESULTS_FOLDER = dev_cfg.results_folder


app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
error = '-error'
success = '-success'


def get_results(ex_id, filename):
    results = None
    file_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    print 'searching for either: ' + file_path+error + ' or ' + file_path+success
    while not results:
        if os.path.exists(file_path+error):
            file_path = file_path+error
            print 'is error file'
            file = open(file_path, 'r')
            if not file:
                continue
            results = file.readlines()
        elif os.path.exists(file_path+success):
            file_path = file_path+success
            print 'is success file'
            file = open(file_path, 'r')
            if not file:
                continue
            results = file.readline()
        else:
            print 'cant find'

    delete_file(file_path)
    return results


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print "Error, can't delete: ", file_path