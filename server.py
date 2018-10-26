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






'''
asset_model = api.model('asset_response', {
                'asset_id': fields.String,
                'description': fields.String,
                })

status_model = api.model('log_response', {
        'log': fields.String,
        })

asset_status = api.model('assetcreate_response', {
                'asset_id': fields.String,
                'status': fields.String,
        })

asset_create = api.model('asset_create_request', {
                'asset_name': fields.String,
                'asset_description': fields.String,
        })


@api.route("/api/device/asset")
class GetAsset(Resource):
    @requires_auth
    @api.marshal_with(asset_model)
    def get(self):
        try:
            asset_path = os.path.join(os.path.expanduser("~"), "asset.json")
            with open(asset_path, "r") as f:
                asset_dct = json.load(f)
                asset_id = asset_dct['asset_id']
            f.close()

        except Exception as e:
            asset_id = None

        if asset_id is None:
            asset_id = "Not defined"
            desc = "asset is not defined in system"
        else:
            desc = "asset id is available"
        return {"asset_id": asset_id, "description": desc}, 200


@api.route("/api/device/status")
class GetDeviceStatus(Resource):
    @requires_auth
    @api.marshal_with(status_model)
    def get(self):
        try:
            path = os.path.join(os.path.expanduser("~"), "device.log")
            with open(path, "r") as fp:
                lines = fp.readlines()
            fp.close()
            if len(lines) < 50:
                return {"log": json.dumps(lines)}
            else:
                return {"log": json.dumps(lines[-50:])}
        except Exception as e:
            return {"log": "Error::{}".format(str(e))}

@api.route("/api/device/createasset")
class CreateAsset(Resource):
    @requires_auth
    @api.expect(asset_create)
    @api.marshal_with(asset_status)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('asset_name', type=str, help='Name of the asset', required=True)
        parser.add_argument('asset_description', type=str, help='Description of asset', required=True)
        args = parser.parse_args()
        am = AssetManager()
        result = am.create_device_asset(args.get('asset_name'), args.get('asset_description'))
        return {"asset_id": result['asset_id'], "status": result['status']}

channel_status = api.model('channelcreate_response', {
                'Channel': fields.String,
                'status': fields.String,
        })


channel_create = api.model('channelcreate_request', {
                 'asset_id': fields.String,
                 'channel_key': fields.String,
                 'label': fields.String,
                 'unitFamily': fields.String,
                 'unit': fields.String,
                 'interval': fields.String,
                 'description': fields.String,
})

@api.route("/api/device/createchannel")
class Createchannel(Resource):
    @requires_auth
    @api.expect(channel_create)
    @api.marshal_with(channel_status)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('asset_id', type=str, help='ID of the asset', required=True)
        parser.add_argument('channel_key', type=str, help='Channel name', required=True)
        parser.add_argument('label', type=str, help='Channel label', required=True)
        parser.add_argument('unitFamily', type=str, help='Channel unit family', required=True)
        parser.add_argument('unit', type=str, help='Channel unit', required=True)
        parser.add_argument('interval', type=str, help='Channel interval', required=True)
        parser.add_argument('description', type=str, help='Channel description', required=True)
        args = parser.parse_args()
        channel_attrs = {
            "key": args.get("channel_key"),
            'label': args.get("label"),
            'unitFamily': args.get("unitFamily"),
            'unit': args.get("unit"),
            'interval': args.get("interval"),
            'description': args.get("description")
        }
        am = AssetManager()
        result = am.add_channel(args.get("asset_id"), channel_attrs)
        return result
'''
if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, port=5000)
