from app import db

taught_courses = db.Table(
    'taught_courses',
    db.Column('teacher_id', db.Integer(), db.ForeignKey('teacher.id')),
    db.Column('course_id', db.Integer(), db.ForeignKey('course.id')),
)


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    image = db.Column(db.Unicode(128))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    def course_name(self):
        return '%s' % (self.name)

    def __str__(self):
        return self.name
