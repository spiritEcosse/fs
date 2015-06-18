from django.shortcuts import render_to_response
from django.template import RequestContext


class Account(object):
    @staticmethod
    def profile(request, *args, **kwargs):
        context = kwargs['extra_context']
        
        return render_to_response(
            'ex_user/profile.html',
            context,
            context_instance=RequestContext(request))