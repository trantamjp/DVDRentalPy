from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        SmallInteger, String, or_, text)
from sqlalchemy.orm import joinedload, lazyload, relationship

from app import db
from app.models.address import Address
from app.models.base_model import BaseModel
from app.models.city import City
from app.models.country import Country

search_like_escape = BaseModel.search_like_escape


class Customer(db.Model, BaseModel):
    __tablename__ = 'customer'

    customer_id = Column(Integer, primary_key=True, server_default=text(
        "nextval('customer_customer_id_seq'::regclass)"))
    store_id = Column(SmallInteger, nullable=False, index=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False, index=True)
    email = Column(String(50))
    address_id = Column(ForeignKey('address.address_id', ondelete='RESTRICT',
                                   onupdate='CASCADE'), nullable=False, index=True)
    activebool = Column(Boolean, nullable=False, server_default=text("true"))
    create_date = Column(Date, nullable=False,
                         server_default=text("('now'::text)::date"))
    last_update = Column(DateTime, server_default=text("now()"))
    active = Column(Integer)

    address = relationship('Address', backref='customers')

    def __repr__(self):
        return '<Customer {} {} {} -> address_id {}>'.format(self.customer_id, self.first_name, self.last_name, self.address_id)

    @classmethod
    def datatable_search(cls, args):

        start = args.get('start') or 0
        length = args.get('length') or 10
        orders = args.get('order') or []
        search = args.get('search') or {}
        columns = args.get('columns') or []

        records_total = Customer.query.count()

        rs_filtered = Customer.query

        for filter_name in ['first_name', 'last_name', 'activebool', 'address', 'postal_code', 'phone', 'city', 'country']:
            column = next(
                (col for col in columns if col.get('name') == filter_name), None)
            if column == None:
                continue

            search_value = column.get('search').get('value') or ''
            if search_value == '':
                continue

            if filter_name == 'first_name':
                rs_filtered = rs_filtered.filter(
                    Customer.first_name.ilike(search_like_escape(search_value)))
                continue

            if filter_name == 'last_name':
                rs_filtered = rs_filtered.filter(
                    Customer.last_name.ilike(search_like_escape(search_value)))
                continue

            if filter_name == 'activebool':
                rs_filtered = rs_filtered.filter(
                    Customer.activebool.is_(str(search_value) == '1'))
                continue

            if filter_name == 'address':
                search_value_like = search_like_escape(search_value)
                rs_filtered = rs_filtered.filter(
                    Customer.address.has(or_(
                        Address.address.ilike(search_value_like),
                        Address.address2.ilike(search_value_like)
                    ))
                )
                continue

            if filter_name == 'postal_code':
                rs_filtered = rs_filtered.filter(
                    Customer.address.has(
                        Address.postal_code.ilike(
                            search_like_escape(search_value))
                    )
                )
                continue

            if filter_name == 'phone':
                rs_filtered = rs_filtered.filter(
                    Customer.address.has(
                        Address.phone.ilike(search_like_escape(search_value))
                    )
                )
                continue

            if filter_name == 'city':
                subq = Address.query.filter(
                    Address.city.has(
                        City.city.ilike(search_like_escape(search_value))
                    )
                ).with_entities(Address.address_id).subquery()

                rs_filtered = rs_filtered.filter(
                    Customer.address_id.in_(subq)
                )
                continue

            if filter_name == 'country':
                subq = Address.query.join(City).join(Country).filter(
                    Country.country_id == search_value
                ).with_entities(Address.address_id).subquery()

                rs_filtered = rs_filtered.filter(
                    Customer.address_id.in_(subq)
                )
                continue

        records_filtered = rs_filtered.count()

        rs_filtered_ordered = rs_filtered.join(
            Address).join(City).join(Country)

        for order in orders:
            order_column = columns[order.get('column')].get('name')
            if order_column == 'address':
                cls_attr = Address.address
            elif order_column == 'city':
                cls_attr = City.city
            elif order_column == 'postal_code':
                cls_attr = Address.postal_code
            elif order_column == 'country':
                cls_attr = Country.country
            elif order_column == 'phone':
                cls_attr = Address.phone
            else:
                cls_attr = getattr(Customer, order_column)

            rs_filtered_ordered = rs_filtered_ordered.order_by(
                cls_attr.desc() if order.get('dir') == 'desc' else cls_attr.asc())

        customers = rs_filtered_ordered.options(joinedload(Customer.address).
                                                joinedload(Address.city).
                                                joinedload(City.country)) \
            .offset(start).limit(length).all()

        customer_list = {
            'records_total': records_total,
            'records_filtered': records_filtered,
            'customers': customers,
        }

        return customer_list
