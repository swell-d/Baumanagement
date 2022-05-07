from django.forms import ModelForm

from comments.models import Comment
from main.models import get_base_models


class CommentFormClass(ModelForm):
    class Meta:
        model = Comment
        fields = Comment.form_fields


def add_comment_to_object(request, new_object):
    path = request.POST.get('newCommentNextURL')
    if not path:
        return
    object_name, id = path.strip('/').split('/')
    id = id[:id.find('?')] if '?' in id else id
    base_models = get_base_models()
    obj = base_models[object_name].objects.get(id=int(id))
    obj.comment_ids.append(new_object.id)
    obj.save()
