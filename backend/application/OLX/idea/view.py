import os
from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from application.OLX.idea.sh import IdeaSchema
from application.OLX.view import allowed_file
from application.client.view import docs
from application.database.client import db
from application.database.idea import Idea
from application.database.problems import ImageUpload

idea = Blueprint('idea',__name__,  url_prefix="/api/v1/idea")


@idea.route('/create', methods=['POST'])
@jwt_required()
def create_idea_with_images():
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

        idea = Idea(title=title, description=description, user_id=current_user_id,)
        idea.image.extend(image_uploads)
        db.session.add(idea)
        db.session.commit()

        return jsonify(message='IDea объявление с изображениями создано успешно.')
    else:
        return jsonify(error='Ошибка: Некорректные файлы изображений.')


@idea.route('/list', methods=['GET'])
def get_all_idea():
    idea = Idea.query.all()
    idea_data = IdeaSchema(many=True).dump(idea)

    return jsonify(idea_data)


@idea.route('/image/<string:Filename>', methods=['GET'])
def get_image(Filename):
    image_upload = ImageUpload.query.get(Filename)

    if image_upload:
        directory = 'uploads'  # Путь к директории с изображениями
        return send_from_directory(directory, image_upload.fileName)
    else:
        return jsonify(error='Изображение не найдено.')


docs.register(create_idea_with_images, blueprint="idea", endpoint='create_idea_with_images')
docs.register(get_all_idea, blueprint="idea", endpoint='get_all_idea')