from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from ex_user.forms import ExUserForm, UserForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.edit import ProcessFormView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login


class ExUser(object):
    @staticmethod
    @login_required
    def profile(request, *args, **kwargs):
        context = kwargs['extra_context']
        return render_to_response(
            'ex_user/profile.html',
            context,
            context_instance=RequestContext(request)
        )


class ExUserRegistrationFormView(FormView, TemplateView):
    template_name = 'ex_user/registration.html'
    success_url = '/profile/'
    form_class = UserForm
    ex_user_form = ExUserForm
    prefix = 'form_user'

    def forms_valid(self, request, **kwargs):
        user = authenticate(username=kwargs['username'], password=kwargs['password'])

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(self.get_success_url())
            raise Exception('Account disabled')
        raise Exception('invalid login')

    def forms_invalid(self, form_user, form_ex_user):
        return self.render_to_response(self.get_context_data(form_user=form_user, form_ex_user=form_ex_user))

    def post(self, request, *args, **kwargs):
        user_form = self.get_form()
        form_ex_user = ExUserForm(self.request.POST, self.request.FILES, prefix='form_ex_user')

        if user_form.is_valid() and form_ex_user.is_valid():
            user = user_form.save()
            form_ex_user = ExUserForm(self.request.POST, self.request.FILES, instance=user, prefix='form_ex_user')
            form_ex_user.is_valid()
            form_ex_user.cleaned_data['user'] = user.id
            form_ex_user.save()
            return self.forms_valid(request, username=user.username, password=user.password)
        return self.forms_invalid(user_form, form_ex_user)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('ex_user:profile'))

        return super(ExUserRegistrationFormView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ExUserRegistrationFormView, self).get_context_data(**kwargs)
        context.update(self.kwargs['extra_context'])
        context['form_user'] = self.get_form()
        context['form_ex_user'] = ExUserForm(prefix='form_ex_user')

        if 'form_ex_user' in kwargs:
            context['form_ex_user'] = kwargs['form_ex_user']
        return context

    def get_success_url(self):
        return self.success_url