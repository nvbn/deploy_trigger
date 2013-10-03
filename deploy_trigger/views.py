from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import logout
from braces.views import LoginRequiredMixin


class IndexPageView(TemplateView):
    """Index page view"""

    def get_template_names(self) -> str:
        """Get template name"""
        if self.request.user.is_authenticated():
            return 'index.html'
        else:
            return 'welcome.html'


class LogoutView(LoginRequiredMixin, RedirectView):
    """Logout view"""
    url = reverse_lazy('home')
    permanent = False

    def get(self, request, *args, **kwargs):
        """Logout on get"""
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
