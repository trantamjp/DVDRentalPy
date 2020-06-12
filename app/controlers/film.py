from app.models.film import Film as FilmDAO


class Film:
    @staticmethod
    def datatable_search(args):
        film_list = FilmDAO.datatable_search(args)
        return {
            'draw':  args.get('draw'),
            'recordsTotal': film_list['records_total'],
            'recordsFiltered': film_list['records_filtered'],
            'data': list(map(lambda film: film.as_json(), film_list['film_list'])),
        }
