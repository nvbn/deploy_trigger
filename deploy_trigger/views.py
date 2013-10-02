from django.views.generic import TemplateView


class IndexPageView(TemplateView):
    """Index page view"""

    def get_template_names(self) -> str:
        """Get template name"""
        if self.request.user.is_authenticated():
            return 'index.html'
        else:
            return 'welcome.html'
