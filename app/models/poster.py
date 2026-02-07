from app.extensions.extensions import db
from datetime import datetime


class Poster(db.Model):
    __tablename__ = "posters"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", name="fk_posters_user_id"), nullable=False
    )
    user = db.relationship("User", back_populates="posters")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
