from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from application.database.client import User, db, Role
from application.database.problems import Problem, Performance, ImageUpload, OLX

admin = Admin(url='/api/admin')


class UserAdmin(ModelView):
    column_hide_backrefs = False
    column_list = ["email", "roles"]


admin.add_view(UserAdmin(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Problem, db.session))
admin.add_view(ModelView(Performance, db.session))
admin.add_view(ModelView(ImageUpload, db.session))
admin.add_view(ModelView(OLX, db.session))