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
import importlib

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

output_model = api.parser()
output_model.add_argument('request_id', type=str, location='args')
output_model.add_argument('method', type=str, location='args')
output_model.add_argument('analytic_name', type=str, location='args')

preprocess_model = api.model("preprocess_request", {
                 'request_id' : fields.String,
                 'method' : fields.String
                })

analytic_model = api.model("analytic_request", {
                 'analytic_name' : fields.String,
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
            path = server_path + "/" + args.get("request_id") + "/" + "preprocess"
            file = os.listdir(path)

            df = pandas.read_csv(path+"/"+file[0])
            if df.shape[0] > 1000:
                df_slice = df[:1000]
            else:
                df_slice = df
            return {"data": df_slice.to_dict(orient='list'), "status": "Success"}, 200
        except Exception as e:
            return {"data": "Failed to read data, ERROR::" + str(e), "status": "Failed"}


@api.route('/api/v1/analytic')
class train_analytic(Resource):
    @api.expect(analytic_model)
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('analytic_name', type=str, location="json", required=True)
            parser.add_argument('method', type=str, location="json", required=True)
            parser.add_argument('request_id', type=str, location="json", required=True)
            args = parser.parse_args()
            path = server_path + "/" + args.get("request_id") + "/" + "preprocess"
            file = os.listdir(path)
            df = pandas.read_csv(path + "/" + file[0])
            module_name = "analytics."+ args.get('analytic_name')
            module = importlib.import_module(module_name)
            analytic_class = getattr(module, args.get("analytic_name"))
            if args.get("method") == "train":
                result = analytic_class.train(df)
                if result["status"] == "success":

                    path = server_path + "/" + args.get("request_id") + "/" + args.get("analytic_name")
                    if os.path.exists(path):
                        pass
                    else:
                        os.mkdir(path)
                    file_name = os.path.join(path, "model.json")
                    fp = open(file_name, "w")
                    json.dump(result, fp)
                    fp.close()
                return result

            elif args.get("method") == "score":
                path = server_path + "/" + args.get("request_id") + "/" + args.get("analytic_name")
                model_file = os.path.join(path, "model.json")
                fp = open(model_file, "r")
                dct_model = json.load(fp)
                fp.close()
                result, df_out, error = analytic_class.score(df, dct_model["coeff"])
                if result == "success":

                    if os.path.exists(path):
                        pass
                    else:
                        os.mkdir(path)
                    file_name = os.path.join(path, "output.csv")
                    df_out.to_csv(file_name, index=False)
                    return {"status":"success"}
                else:
                    return {"status": "failed", "error": error}
        except Exception as e:
            return {"status": "failed", "error": str(e)}



@api.route('/api/v1/listanalytics')
class list_analytic(Resource):
    def get(self):
        path = os.path.join(server_path, "analytics.json")
        fp = open(path, "r")
        analytics = json.load(fp)
        fp.close()
        return analytics

@api.route('/api/v1/output')
class get_result(Resource):
    @api.expect(output_model)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('analytic_name', type=str, location="args", required=True)
            parser.add_argument('method', type=str, location="args", required=True)
            parser.add_argument('request_id', type=str, location="args", required=True)
            args = parser.parse_args()
            path = server_path + "/" + args.get("request_id") + "/" + args.get("analytic_name")
            if args.get("method") == "train":
                file_name = "model.json"
            else:
                file_name = "output.csv"

            file_name = os.path.join(path, file_name)
            if os.path.exists(file_name):
                if args.get("method") == "train":
                    fp = open(file_name, "r")
                    data = json.load(fp)
                    fp.close()
                    return data
                else:
                    fp = open(file_name, "r")
                    df = pandas.read_csv(file_name)
                    return {"data": df.to_dict(orient='list')}
        except Exception as e:
            return {"error": str(e)}


if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, port=5000)
