from ex_user.forms import ExUserForm, UserForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login


class ExUser(TemplateView):
    template_name = 'ex_user/profile.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/login/?next=%s' % request.path)
        return super(ExUser, self).get(request, *args, **kwargs)


class ExUserRegistrationFormView(FormView):
    template_name = 'ex_user/registration.html'
    success_url = '/profile/'
    form_class = UserForm
    ex_user_form = ExUserForm

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
        form_ex_user = self.ex_user_form(self.request.POST, self.request.FILES)

        if user_form.is_valid() and form_ex_user.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            ex_user = form_ex_user.save(commit=False)
            ex_user.user = user
            ex_user.save()
            return self.forms_valid(request, username=self.request.POST.get('username'),
                                    password=self.request.POST.get('password'))
        return self.forms_invalid(user_form, form_ex_user)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('ex_user:profile'))

        return super(ExUserRegistrationFormView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = dict()
        context['form_user'] = self.get_form()
        context['form_ex_user'] = self.ex_user_form()
        context.update(super(ExUserRegistrationFormView, self).get_context_data(**kwargs))
        return context

    def get_success_url(self):
        return self.success_url
