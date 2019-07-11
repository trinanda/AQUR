from app import db


class course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    schedule = db.Column(db.DateTime())
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teacher.id'))
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'))

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
