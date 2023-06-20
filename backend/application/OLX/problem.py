import os
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from application.OLX.sh import ProblemSchema, ImageUploadSchema
from application.OLX.view import allowed_file
from application.client.view import docs
from application.database.client import db
from application.database.problems import ImageUpload, Problem

problem = Blueprint('problem_1', __name__, url_prefix="/api/v1/problem")


@problem.route('/create', methods=['POST'])
@jwt_required()
def create_problem_with_images():
    current_user_id = get_jwt_identity().get('id')
    title = request.form.get('title')
    description = request.form.get('description')
    iin = request.form.get("iin")

    images = request.files.getlist('images')

    if images:
        image_uploads = []
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                from app import app
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(file_path)

                image_upload = ImageUpload(fileName=filename, file=file_path)
                db.session.add(image_upload)
                image_uploads.append(image_upload)

        olx = Problem(title=title, description=description, user_id=current_user_id, iin=iin)
        olx.image.extend(image_uploads)
        db.session.add(olx)
        db.session.commit()

        return jsonify(message='Problem объявление с изображениями создано успешно.')
    else:
        return jsonify(error='Ошибка: Некорректные файлы изображений.')


@problem.route('/list', methods=['GET'])
def get_all_problems():
    problems = Problem.query.all()
    problems_data = ProblemSchema(many=True).dump(problems)
    return jsonify(problems_data)


@problem.route('/images', methods=['GET'])
def get_all_images():
    images = ImageUpload.query.all()
    images_data = ImageUploadSchema(many=True).dump(images)
    return jsonify(images_data)


docs.register(create_problem_with_images, blueprint="problem_1", endpoint='create_problem_with_images')
docs.register(get_all_problems, blueprint="problem_1", endpoint='get_all_problems')

