from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from app import db
from app.models.base_model import BaseModel


class Address(db.Model, BaseModel):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True, server_default=text(
        "nextval('address_address_id_seq'::regclass)"))
    address = Column(String(50), nullable=False)
    address2 = Column(String(50))
    district = Column(String(20), nullable=False)
    city_id = Column(ForeignKey('city.city_id'), nullable=False, index=True)
    postal_code = Column(String(10))
    phone = Column(String(20), nullable=False)
    last_update = Column(DateTime, nullable=False,
                         server_default=text("now()"))

    city = relationship('City', backref='addresses')

    def __repr__(self):
        return '<Address {} {} {} -> city_id {}>'.format(self.address_id, self.address, self.address2, self.city_id)
