#!/usr/bin/env python

from wsgiref import simple_server
from flask import Flask, request, render_template,abort,send_file
from flask import Response
import os
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction
import json

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/main", methods=["GET"])
@cross_origin()

def main():
    return render_template("main.html")

@app.route("/data", defaults={"req_path": "Prediction_Batch_files"})
@app.route("/data/<path:req_path>")

@cross_origin()
def get_data(req_path):
    try:
        os.makedirs("data", exist_ok=True)
        print(f"req_path: {req_path}")
        abs_path = os.path.join(req_path)
        print(abs_path)
        if not os.path.exists(abs_path):
            abort(404)
        if os.path.isfile(abs_path):
            return send_file(abs_path)
        files = {os.path.join(abs_path, file) : file for file in os.listdir(abs_path)}
        result = {
            "files": files,
            "parent_folder": os.path.dirname(abs_path),
            "parent_label": abs_path
        }
        return render_template("files.html", result=result)
    except Exception as e:
        error = "Error occured while getting the data"
        error = {"error": error}
        return render_template("404.html", error=error)


@app.route("/saved_models", defaults={"req_path": "models"})
@app.route("/saved_models/<path:req_path>")

@cross_origin()
def saved_models(req_path):
    try:
        os.makedirs("saved_models", exist_ok=True)
        print(f"req_path: {req_path}")
        abs_path = os.path.join(req_path)
        print(abs_path)
        if not os.path.exists(abs_path):
            abort(404)
        if os.path.isfile(abs_path):
            return send_file(abs_path)
        files = {os.path.join(abs_path, file)                 : file for file in os.listdir(abs_path)}
        result = {
            "files": files,
            "parent_folder": os.path.dirname(abs_path),
            "parent_label": abs_path
        }
        return render_template("saved_models_files.html", result=result)
    except Exception as e:
        error = "Error occured while getting the saved models 🤔🤔"
        error = {"error": error}
        return render_template("404.html", error=error)
    
@app.route("/upload", methods=["POST", "GET"])
@cross_origin()

def upload():
    return render_template("db.html")
    
@app.route("/logs", defaults={"req_path": "Training_Logs"})
@app.route("/logs/<path:req_path>")

@cross_origin()
def get_logs(req_path):
    try:
        os.makedirs("logs", exist_ok=True)
        print(f"req_path: {req_path}")
        abs_path = os.path.join(req_path)
        print(abs_path)
        if not os.path.exists(abs_path):
            abort(404)
        if os.path.isfile(abs_path):
            return send_file(abs_path)
        files = {os.path.join(abs_path, file)                 : file for file in os.listdir(abs_path)}
        result = {
            "files": files,
            "parent_folder": os.path.dirname(abs_path),
            "parent_label": abs_path
        }
        return render_template("log_files.html", result=result)
    except Exception as e:
        error = "Error occured while getting the log files 🤔🤔"
        error = {"error": error}
        return render_template("404.html", error=error)

@app.route("/stream/train",methods=["GET","POST"])
def retrain_model():
    return render_template("train1.html")



# def stream():
#     try:
#         def generate():
#             with open(log_file_path, "r") as f:
#                 while True:
#                     yield f.read()
#                     sleep(0.1)
#         return app.response_class(generate(), mimetype="text/plain")
#     except Exception as e:
#         print(e)

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']

            pred_val = pred_validation(path)  # object initialization

            pred_val.prediction_validation()  # calling the prediction_validation function

            pred = prediction(path)  # object initialization

            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at !!!" + str(path) + 'and few of the predictions are ' + str(
                json.loads(json_predictions)))
        elif request.form is not None:
            path = request.form['filepath']

            pred_val = pred_validation(path)  # object initialization

            pred_val.prediction_validation()  # calling the prediction_validation function

            pred = prediction(path)  # object initialization

            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at !!!" + str(path) + 'and few of the predictions are ' + str(
                json.loads(json_predictions)))
        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)


@app.route("/train", methods=['GET', 'POST'])
@cross_origin()
def trainRouteClient():
    try:
        # if request.json['folderPath'] is not None:
        folder_path = "Training_Batch_Files"
        # path = request.json['folderPath']
        if folder_path is not None:
            path = folder_path

            train_valObj = train_validation(path)  # object initialization

            train_valObj.train_validation()  # calling the training_validation function

            trainModelObj = trainModel()  # object initialization
            trainModelObj.trainingModel()  # training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)
    return Response("Training successful!!")


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    # port = 5000
    app.run(host='127.0.0.1',port=port, debug=False)