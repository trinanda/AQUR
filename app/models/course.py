from app import db


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    private_class_charge_per_minutes = db.Column(db.Float())
    regular_class_charge_per_minutes = db.Column(db.Float())
    min_private_class_duration = db.Column(db.Float())
    min_regular_class_duration = db.Column(db.Float())
    min_private_class_charge_per_meet = db.Column(db.Float())
    min_regular_class_charge_per_meet = db.Column(db.Float())
    image = db.Column(db.Unicode(128))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    def course_name(self):
        return '%s' % (self.name)

    def __str__(self):
        return self.name
