from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        info_dict = request.session.get('info')
        path = request.path_info
        # print(path)
        # print(info_dict)
        if path in ['/login', '/index', '/register', '/ProblemSet'] or info_dict is not None:
            return
        else:
            return redirect('/login')


