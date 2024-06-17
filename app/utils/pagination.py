from app import models


class Pagination(object):
    def __init__(self, request, per_page=5, page_index_range=1, private=True, table_name=""):
        data = {}

        self.request = request
        # print(request.session['info'])
        if 'info' in request.session:
            self.user_id = request.session['info']['id']
        if private is True:
            data['user_id'] = self.user_id

        self.search_value = request.GET.get('q', "")
        if self.search_value != "":
            data['title__contains'] = self.search_value
            # data['index__contains'] = self.search_value
        # print(data)
        # self.queryset = models.FavoriteProblem.objects.filter(**data)
        # print(table_name)
        self.queryset = getattr(models, table_name).objects.filter(**data)
        # print(self.queryset)

        self.page = int(request.GET.get('page', '1'))
        self.per_page = int(per_page)
        self.page_index_range = int(page_index_range)

        self.start = (self.page - 1) * self.per_page
        self.end = self.page * self.per_page
        self.page_queryset = self.queryset[self.start:self.end]

        self.total_count = self.queryset.count()
        self.page_index_count = self.total_count // self.per_page + 1


    def page_index_string(self):
        str_list = ""
        page_index_start = max(1, self.page - self.page_index_range)
        page_index_end = min(self.page_index_count, self.page + self.page_index_range)
        # print(self.page, self.page_index_count, page_index_start, page_index_end)
        if self.page > 1:
            str_list += f'<li class="page-item"><a class="page-link" href="?page={self.page-1}">Previous</a></li>'
        else:
            str_list += f'<li class="page-item"><a class="page-link disabled" href="#">Previous</a></li>'
        for i in range(page_index_start, page_index_end + 1):
            if i == self.page:
                str_list += f'<li class="page-item active"><a class="page-link" href="?page={i}">{i}</a></li>'
            else:
                str_list += f'<li class="page-item"><a class="page-link" href="?page={i}">{i}</a></li>'
        if self.page < self.page_index_count:
            str_list += f'<li class="page-item"><a class="page-link" href="?page={self.page+1}">Next</a></li>'
        else:
            str_list += f'<li class="page-item"><a class="page-link disabled" href="#">Next</a></li>'

        return str_list

    def page_range(self):
        data = {}
        if self.search_value is not "":
            data['title'] = self.search_value

        start = max(0, (self.page - 1) * self.per_page)
        end = min(self.queryset.count(), start + self.per_page)
        queryset = self.queryset[start:end]
        return queryset
