from flask import Flask, request
from flask_restplus import Resource, Api, fields, reqparse
import os
import pandas
import json
from werkzeug.contrib.fixers import ProxyFix
from waitress import serve
from werkzeug.datastructures import FileStorage
import parser
import uuid
from preprocess.pre_process import clean_data


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app)
#server_path = r"C:\Users\Harish\PycharmProjects\cceproject\data\raw_data"


if os.path.exists(os.path.join(os.path.expanduser("~"), "serverdata")):
    server_path = os.path.join(os.path.expanduser("~"), "serverdata")
else:
    server_path = os.path.join(os.path.expanduser("~"), "serverdata")
    os.makedirs(server_path)


file_upload_model = api.parser()
file_upload_model.add_argument('file', type=FileStorage, location='files', required=True)

file_visualize_model = api.parser()
file_visualize_model.add_argument('request_id', type=str, location='args')

preprocess_model = api.model("preprocess_request", {
                 'request_id' : fields.String,
                 'method' : fields.String
                })

@api.route('/api/v1/fileupload')
class upload_file(Resource):

    @api.expect(file_upload_model)
    def post(self):
        try:
            requestid = uuid.uuid4().hex
            parser = reqparse.RequestParser()
            parser.add_argument('file', type=FileStorage, location='files', required=True)
            args = parser.parse_args()
            # checking if the file is present or not.
            #if 'file' not in request.files:
            #    return "No file found"
            file = args.get('file')
            #server_path = r"C:\Users\Harish\PycharmProjects\cceproject\data\raw_data"
            #file = request.files['file']

            path = os.path.join(os.path.join(server_path, requestid + "\\" + "rawdata"))
            if os.path.exists(path):
                pass
            else:
                os.makedirs(path)

            abs_path = path + "\\" + file.filename
            file.save(abs_path)
            return {"requestid": requestid, "upload_status": "success", "location": abs_path}, 200
        except Exception as e:
            requestid = None
            return {"requestid": requestid, "upload_status": "failed::" + str(e) , "location": ""}


@api.route('/api/v1/preprocess')
class preprocess(Resource):
    @api.expect(preprocess_model)
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('request_id', type=str, location="json", required=True)
            parser.add_argument('method', type=str, location="json", required=True)
            args = parser.parse_args()
            path = server_path + "/" + args.get("request_id") + "/" + "rawdata"
            file = os.listdir(path)[0]

            df_clean = clean_data(path + "/" + file, args.get("method"))
            clean_path = server_path + "/" + args.get("request_id") + "/" + "preprocess"
            if os.path.exists(clean_path):
                pass
            else:
                os.mkdir(clean_path)
            clean_path = clean_path + "/" + file
            df_clean.to_csv(clean_path, index=False)
            return {"status": "Success", "Description": "Data cleaned"}, 200
        except Exception as e:
            return {"status": "Failed", "Description": "ERROR::" + str(e)}






@api.route('/api/v1/visualize/rawdata')
class visualize_rawdata(Resource):
    @api.expect(file_visualize_model)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('request_id', type=str, location='args')
            args = parser.parse_args()
            path = server_path + "/" + args.get("request_id") + "/" + "rawdata"
            file = os.listdir(path)

            df = pandas.read_csv(path+"/"+file[0])
            if df.shape[0] > 1000:
                df_slice = df[:1000]
            else:
                df_slice = df
            return {"data" : df_slice.to_dict(orient='list'), "status": "Success"}, 200
        except Exception as e:
            return {"data" : "Failed to read data, ERROR::" + str(e), "status": "Failed"}

@api.route('/api/v1/visualize/cleandata')
class visualize_rawdata(Resource):
    @api.expect(file_visualize_model)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('request_id', type=str)
            args = parser.parse_args()
            path = server_path + "/" + args.get("request_id") + "/" + "cleandata"
            file = os.listdir(path)

            df = pandas.read_csv(path+"/"+file[0])
            if df.shape[0] > 1000:
                df_slice = df[:1000]
            else:
                df_slice = df
            return {"data": df_slice.to_dict(orient='list'), "status": "Success"}, 200
        except Exception as e:
            return {"data": "Failed to read data, ERROR::" + str(e), "status": "Failed"}






if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, port=5000)
