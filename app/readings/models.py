from app import db


class Reading(db.Model):
    __tablename__ = "readings"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    timestamp = db.Column(db.TIMESTAMP)

    def __init__(self, value, timestamp):
        self.value = value
        self.timestamp = timestamp

    def serialize(self):
        return {
            "id": self.id,
            "value": self.value,
            "timestamp": self.timestamp.isoformat()
        }
