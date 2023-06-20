import os
from flask import request, jsonify, Blueprint,send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from application.client.view import docs
from application.database.client import db
from application.database.problems import ImageUpload, OLX
from application.OLX.sh import OLXWithImageSchema

olx = Blueprint('olx_1', __name__, url_prefix="/api/v1/olx")


@olx.route('/create', methods=['POST'])
@jwt_required()  # Требуется авторизация
def create_olx_with_images():
    current_user_id = get_jwt_identity().get('id')
    title = request.form.get('title')
    description = request.form.get('description')
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


        olx = OLX(title=title, description=description, user_id=current_user_id)
        olx.image.extend(image_uploads)
        db.session.add(olx)
        db.session.commit()

        return jsonify(message='OLX объявление с изображениями создано успешно.')
    else:
        return jsonify(error='Ошибка: Некорректные файлы изображений.')



@olx.route('/list', methods=['GET'])
def get_all_olx():
    problems = OLX.query.all()
    problems_data = OLXWithImageSchema(many=True).dump(problems)

    return jsonify(problems_data)


@olx.route('/images/<fileName>', methods=['GET'])
def get_image(fileName):
    image_upload = ImageUpload.query.filter_by(fileName=fileName).first()
    if image_upload is None:
        return 'Файл не найден', 404
    from app import app
    image_path = os.path.join(app.root_path, '..', 'uploads', fileName)
    return send_file(image_path)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif',"PNG"}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

docs.register(create_olx_with_images, blueprint="olx_1", endpoint='create_olx_with_images')
docs.register(get_all_olx, blueprint="olx_1", endpoint='get_all_olx')