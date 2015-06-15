from django.shortcuts import render
from django.forms import ModelForm, HiddenInput
from comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect



    # @staticmethod
    # @csrf_protect
    # @require_POST
    # def comment_save(request):
    #     form = CommentForm(request.POST)
    #
    #     if form.is_valid():
    #         form.save()
    #         c_type = form.cleaned_data['content_type']
    #         obj = c_type.get_object_for_this_type(pk=form.cleaned_data['object_id'])
    #         return redirect(obj)
    #
    #     return render(request, 'materials/item_detail.html', {'form_comment': form})
