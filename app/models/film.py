from sqlalchemy import func, or_

from app import db


class Film(db.Model):
    __tablename__ = 'film_list'

    fid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.TEXT)
    category = db.Column(db.String(10))
    price = db.Column(db.Float)
    length = db.Column(db.Integer)
    rating = db.Column(db.String(50))
    actors = db.Column(db.TEXT)

    def __repr__(self):
        return '<Film {} {}}>'.format(self.title, self.category)

    def as_json(self):
        return {
            'fid': self.fid,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'length': self.length,
            'rating': self.rating,
            'actors': self.actors,
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

        films = rs_filtered_paging.all()

        film_list = {
            'records_total': records_total,
            'records_filtered': records_filtered,
            'film_list': films,
        }

        return film_list
