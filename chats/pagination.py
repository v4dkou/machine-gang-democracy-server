from hakathon.pagination import MaxIdPagination

class DateCreatedPagination(MaxIdPagination):
    ordering = '-date_created'
