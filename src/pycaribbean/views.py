# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView


class AngularAppView(TemplateView):
    """
    Serve the base angular app template.
    """
    template_name = 'base.html'
