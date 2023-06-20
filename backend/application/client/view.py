import random
import string
from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify
from flask_apispec import FlaskApiSpec
from marshmallow import ValidationError
import io
import csv
from flask import send_file, make_response
from application.client.sh import UserSchema
from application.database.client import User

auth = Blueprint('auth', __name__, url_prefix="/api/v1/auth")
docs = FlaskApiSpec()


@auth.route('/login', methods=["POST"])
def login():
    try:
        user_data = UserSchema(only=('number', 'password', 'role_user')).load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    number = user_data.get('number')
    password = user_data.get('password')
    role_user = user_data.get('role_user')

    if number and password and role_user:
        user = User.query.filter_by(number=number, role_user=role_user).first()
        if user and user.password_check_hash(password):
            access_token = user.create_token(identity=user.id, id=user.id)
            return jsonify({"access_token": access_token, "user": user.id, "role_user": user.role_user}), 200
    return jsonify(message="Invalid number, password, or role"), 401


@auth.route("/register", methods=["POST"])
def register():
    try:
        user_data = UserSchema(only=('number', 'password', 'role_user', 'full_name')).load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    pwd = User.password_hash(password=user_data['password'])

    user = User(
        number=user_data['number'],
        role_user=user_data.get('role_user', None),
        full_name=user_data.get('full_name', None),
        password=pwd
    )
    user.create_user(user)
    result = UserSchema().dump(user)
    return jsonify(result), 201


@auth.route("/register/users", methods=['POST'])
@jwt_required()
def create_default_user():
    try:
        user_data = UserSchema(only=('apartment',)).load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Генерация случайного номера
    number = random.randint(1000, 9999)

    # Генерация случайного полного имени
    full_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))

    # Генерация случайного пароля
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    pwd = User.password_hash(password)

    user = User(
        number=number,
        full_name=full_name,
        password=pwd,
        apartment=user_data['apartment']
    )
    user.create_user(user)
    result = UserSchema().dump(user)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Number', 'Full Name', 'Password', 'Apartment'])
    writer.writerow([number, full_name, password, user_data['apartment']])

    # Создание объекта ответа
    response = make_response(output.getvalue())

    # Настройка заголовков и скачивание файла
    response.headers.set('Content-Disposition', 'attachment', filename='generated_data.csv')
    response.headers.set('Content-Type', 'text/csv')

    return response


@auth.route("/job", methods=['GET'])
def user_job():
    job = User.query.filter_by(role_user="Работник").all()
    job_data = UserSchema(many=True).dump(job)
    return jsonify(job_data), 200

   


docs.register(login, blueprint="auth", endpoint='login')
docs.register(register, blueprint="auth", endpoint='register')
docs.register(user_job, blueprint="auth", endpoint='user_job')



