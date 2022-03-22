from django.db.models import Q

contracts_search_fields = 'project__name', 'company__name', 'name', 'amount_netto', 'vat', 'amount_brutto'
projects_search_fields = 'name', 'code', 'company__name', 'address', 'city', 'land'
bills_search_fields = 'contract__project__name', 'contract__company__name', 'contract__name', \
                      'name', 'amount_netto', 'vat', 'amount_brutto'
companies_search_fields = 'name', 'address', 'city', 'land', 'email', 'phone', 'ceo', 'vat_number'
payments_search_fields = 'contract__project__name', 'contract__company__name', 'contract__name', \
                         'name', 'amount_netto', 'vat', 'amount_brutto'


def filter_queryset(queryset, request, search_fields):
    search = request.GET.get('search')
    if search is not None:
        qs = Q()
        for query in [Q(**{f'{field}__icontains': search}) for field in search_fields]:
            qs = qs | query
        queryset = queryset.filter(qs)
    return queryset
