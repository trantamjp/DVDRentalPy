from sqlalchemy import Date, DateTime, Numeric


class BaseModel:

    def row2dict(self):
        d = {}
        for column in self.__table__.columns:
            val = getattr(self, column.name)
            d[column.name] = \
                val.isoformat() if (isinstance(column.type, Date) or isinstance(column.type, DateTime)) \
                else str(round(val, 2)) if (isinstance(column.type, Numeric)) \
                else val

        return d

    @staticmethod
    def search_like_escape(value):
        return '%' + value \
            .replace('\\', '\\\\') \
            .replace('_', '\\_') \
            .replace('%', '\\%') + '%'
