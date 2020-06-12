from sqlalchemy import func, or_

from app import db


class Customer(db.Model):
    __tablename__ = 'customer_list'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(50))
    zip_code = db.Column('zip code', db.String(10))
    phone = db.Column(db.String(20))
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    notes = db.Column(db.String(20))
    sid = db.Column(db.Integer)

    def __repr__(self):
        return '<Customer {} {} {}>'.format(self.name, self.address, self.zip_code)

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'zip_code': self.zip_code,
            'phone': self.phone,
            'city': self.city,
            'country': self.country,
            'notes': self.notes,
            'sid': self.sid,
        }

    @classmethod
    def datatable_search(cls, args):
        start = args.get('start') or 0
        length = args.get('length') or 10
        orders = args.get('order') or []
        search = args.get('search') or {}
        columns = args.get('columns') or []

        rs = cls.query
        records_total = rs.count()

        rs_filtered = rs
        filters = []
        search_value = search.get('value')
        for column in columns:
            if not column.get('searchable'):
                continue
            try:
                column_search_value = column.get(
                    'search').get('value') or search_value
                if column_search_value != '':
                    column_search_value = '%' + column_search_value.lower() + '%'
                    cls_attr = getattr(cls, column.get('data'))
                    filters.append(func.lower(
                        cls_attr).like(column_search_value))
            except:
                continue

        if len(filters):
            rs_filtered = rs_filtered.filter(or_(*filters))

        records_filtered = rs_filtered.count()

        rs_filtered_paging = rs_filtered
        for order in orders:
            try:
                order_column = columns[order.get('column')].get('data')
                cls_attr = getattr(cls, order_column)

                order_dir = order.get('dir')
                if order_dir == 'desc':
                    order_dir = cls_attr.desc()
                else:
                    order_dir = cls_attr.asc()
            except:
                continue

            rs_filtered_paging = rs_filtered_paging.order_by(order_dir)

        rs_filtered_paging = rs_filtered_paging.offset(start).limit(length)

        customers = rs_filtered_paging.all()

        customer_list = {
            'records_total': records_total,
            'records_filtered': records_filtered,
            'customer_list': customers,
        }

        return customer_list
