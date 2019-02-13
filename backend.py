from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
import json  # To write history to a json file
from pathlib import Path  # To check if the json file exists
import os  # To delete the json history file from the server
import datetime  # To rename the json file if corrupted and include the date in the name

app = Flask(__name__)

# --- Routes ---
# redirect to endpoint /counter for any other routes than counter and history
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('actionOnCounter'))

@app.route('/counter')
def actionOnCounter():
    inputValue = request.args.get('value')  # get the input value
    actionToDoOnCounter = request.args.get('action-select-box')  # get the selected action in option menu

    # if json file exists, values already exists, so counter value need to be loaded
    if (isJsonHistoryFileExists()):
        counterValue = getLastValueInJsonHistoryFile()

        if (inputValue and actionToDoOnCounter):
            return treatActionOnCounter(counterValue, float(inputValue), actionToDoOnCounter)

        return renderCounterTemplate(counterValue)

    elif (inputValue and actionToDoOnCounter):  # first time with inputs
        counterValue = 0
        
        createJsonHistoryFile()
        return treatActionOnCounter(counterValue, float(inputValue), actionToDoOnCounter)

    return renderCounterTemplate(0)  # first time without inputs

@app.route('/history')
def history():
    if (isJsonHistoryFileExists()):
        with open('history.json') as jsonHistoryFile:
            contentJsonFile = json.load(jsonHistoryFile)
        return render_template('history.html', value=contentJsonFile['history']) 

    return render_template('history.html')

@app.route('/deletehistory')
def deleteHistory():
    # delete the file then redirect to history
    deleteJsonHistoryFile()
    return redirect(url_for('history'))
    
#
# --- Functions ---
#
def treatActionOnCounter(p_counterValue, p_inputValue, p_actionToDoOnCounter):
    try:
        if (p_actionToDoOnCounter == 'addition'):
            p_counterValue = p_counterValue + p_inputValue

        if (p_actionToDoOnCounter == 'soustraction'):
            p_counterValue = p_counterValue - p_inputValue

        if (p_actionToDoOnCounter == 'multiplication'):
            p_counterValue = p_counterValue * p_inputValue

        if (p_actionToDoOnCounter == 'division'):
            p_counterValue = p_counterValue / p_inputValue
    except: 
        p_counterValue = 0

    writeDataToJsonHistoryFile(roundCounterValue(p_counterValue), p_actionToDoOnCounter)
    return renderCounterTemplate(p_counterValue)

# Create the json history file with his structure
def createJsonHistoryFile():
    with open('history.json', 'w') as jsonHistoryFile:
        jsonHistoryFile.write("{\"history\": []}")
        jsonHistoryFile.close()

# Update json history file after a new action
def writeDataToJsonHistoryFile(p_counterValue, p_actionOnCounter):
    with open('history.json') as jsonHistoryFile:
        contentJsonFile = json.load(jsonHistoryFile)

    contentJsonFile["history"].append({"counterValue": p_counterValue, "actionOnCounter": p_actionOnCounter})

    with open('history.json', 'w') as newJsonHistoryFile:
        newJsonHistoryFile.write(json.dumps(contentJsonFile))
        newJsonHistoryFile.close()

# Return true if the json history file already exists and have the right structure
def isJsonHistoryFileExists():
    myJsonFile = Path('history.json')
    
    if myJsonFile.is_file():
        with open('history.json') as jsonHistoryFile:
            contentJsonFile = json.load(jsonHistoryFile)
        try:
            # Check if the structure of the json is not corrupted
            if('history' in contentJsonFile):
                for jsonLine in contentJsonFile['history']:
                    if (not 'counterValue' in jsonLine or not 'actionOnCounter' in jsonLine):
                        renameJsonHistoryFile()
                        return False
            else:
                renameJsonHistoryFile()
                return False
        except:
            # Rename file if corrupted
            renameJsonHistoryFile()
            return False
        
        return True

    return False

# Return the last value stored in the json file
def getLastValueInJsonHistoryFile():
    with open('history.json') as jsonHistoryFile:
        contentJsonFile = json.load(jsonHistoryFile)
    # try-catch to return 0 if the file exists but there is nothing in it
    try:
        # return the last value stored in the file as a float
        return float(contentJsonFile['history'][len(contentJsonFile['history'])-1]['counterValue'])
    except:
        return 0

# Rename the json history file (in case the file is corrupted, better to rename than delete it)
def renameJsonHistoryFile():
    now = datetime.datetime.now()
    os.rename('history.json', 'history_corrupted_{}.json'.format(now.strftime("%Y-%m-%d_%H-%M")))

# To delete the json history file
def deleteJsonHistoryFile():
    if (isJsonHistoryFileExists()):
        os.remove('history.json')

# Round the counter value for better user experience
def roundCounterValue(p_counterValue):
    if (p_counterValue != 0): # 0 removed later so don't execute if it's 0
        counterValue = round(p_counterValue, 3)  # round to 3 digits
        return str(counterValue).rstrip('0').rstrip('.')  # if number ends with '.0' its removed
    
    return 0

# More readable render function
def renderCounterTemplate(p_counterValue):
    return render_template('index.html', value=roundCounterValue(p_counterValue))
