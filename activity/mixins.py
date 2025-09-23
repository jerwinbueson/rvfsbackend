from django.utils import timezone
from .models import UserLog  # adjust if your UserLog is elsewhere

class UserLogMixin:
    """
    Add to any CBV (CreateView, UpdateView, DeleteView) to log user actions.
    Set `log_action` automatically based on CBV type.
    """
    log_create_action = 'CREATE'
    log_update_action = 'UPDATE'
    log_delete_action = 'DELETE'

    def log_user_action(self, obj, action, description=None):
        """Create a UserLog row for the current user and object."""
        UserLog.objects.create(
            user=getattr(self.request, 'user', None),
            action=action,
            model_name=obj.__class__.__name__,
            object_id=obj.pk,
            description=description or f"{action} {obj}",
            timestamp=timezone.now()
        )

    # hook into CreateView/UpdateView form_valid
    def form_valid(self, form):
        response = super().form_valid(form)
        action = self.log_create_action if self.request.method == 'POST' and not self.object.pk else self.log_update_action
        # In CreateView, self.object is just created; in UpdateView it's updated
        self.log_user_action(self.object, action)
        return response

    # hook into DeleteView delete
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        self.log_user_action(obj, self.log_delete_action)
        return super().delete(request, *args, **kwargs)
