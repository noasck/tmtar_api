from flask import send_from_directory
from flask_restx import Namespace, Resource, abort
from flask_accepts import responds
from flask.wrappers import Response # noqa
from typing import List

from .schema import FileSchema
from .service import FileService, AliasGenerator
from .model import File
from ..project.builders.access_control import access_restriction
import werkzeug
from flask_restx import reqparse
from flask_cors import cross_origin

import os
from ..project.injector import Injector
from werkzeug.utils import secure_filename

app = Injector().app

file_upload = reqparse.RequestParser()
file_upload.add_argument('file',
                         type=werkzeug.datastructures.FileStorage,
                         location='files',
                         required=True,
                         help='Source file')

api = Namespace('files', description='Ns contains media control routes', decorators=[cross_origin()])


@api.route('/')
class FileResource(Resource):
    """Files"""

    @responds(schema=FileSchema(many=True), api=api)
    @access_restriction(root_required=True, api=api)
    def get(self) -> List[File]:
        """Get all files list"""
        return FileService.get_all()

    @responds(schema=FileSchema, api=api)
    @api.expect(file_upload)
    @access_restriction(api=api)
    def post(self):
        """Post new File to server media storage"""
        args = file_upload.parse_args()
        if args['file']:
            filename, file_extension = os.path.splitext(args['file'].filename)
            alias = AliasGenerator.random_string_generator()+file_extension
            destination = os.path.join(
                app.config["MEDIA_FOLDER"],
                alias
            )
            if not os.path.exists(app.config["MEDIA_FOLDER"]):
                os.makedirs(app.config["MEDIA_FOLDER"])
            args['file'].save(destination)
            return FileService.create(alias)
        else:
            abort(404, message='File not sent')


@api.route('/<path:filename>') # noqa
class FileNameResource(Resource):

    @api.response(200, "Returns file to download from storage media")
    def get(self, filename):
        """Get file from the storage"""
        file = secure_filename(filename)
        return send_from_directory(app.config["MEDIA_FOLDER"], file)

    @access_restriction(root_required=True, api=api)
    def delete(self, filename):
        """Delete File from storage"""
        if FileService.delete_by_filename(secure_filename(filename)):
            os.remove(os.path.join(app.config["MEDIA_FOLDER"], filename))
