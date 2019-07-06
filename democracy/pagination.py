from hakathon.pagination import MaxIdPagination

class DateUpdatedPagination(MaxIdPagination):
    ordering = '-date_updated'
