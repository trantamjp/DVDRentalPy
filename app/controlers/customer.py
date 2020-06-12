from app.models.customer import Customer as CustomerDAO


class Customer:
    @staticmethod
    def datatable_search(args):
        customer_list = CustomerDAO.datatable_search(args)
        return {
            'draw':  args.get('draw'),
            'recordsTotal': customer_list['records_total'],
            'recordsFiltered': customer_list['records_filtered'],
            'data': list(map(lambda customer: customer.as_json(), customer_list['customer_list'])),
        }
