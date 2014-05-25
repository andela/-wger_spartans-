# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

from django import template
from django.forms.widgets import CheckboxInput

from wger.utils.constants import PAGINATION_MAX_TOTAL_PAGES
from wger.utils.constants import PAGINATION_PAGES_AROUND_CURRENT

register = template.Library()


@register.filter(name='get_current_settings')
def get_current_settings(exercise, set_id):
    '''
    Does a filter on the sets

    We need to do this here because it's not possible to pass arguments to function in
    the template, and we are only interested on the settings that belong to the current
    set
    '''
    return exercise.setting_set.filter(set_id=set_id)


@register.inclusion_tag('tags/render_day.html')
def render_day(day):
    '''
    Renders a day as it will be displayed in the workout overview
    '''
    return {'day':     day.canonical_representation,
            'workout': day.training}


@register.inclusion_tag('tags/pagination.html')
def pagination(paginator, page):
    '''
    Renders the necessary links to paginating a long list
    '''

    # For very long lists (e.g. the English ingredient with more than 8000 items)
    # we muck around here to remove the pages not inmediately 'around' the current
    # one, otherwise we end up with a useless block with 300 pages.
    if paginator.num_pages > PAGINATION_MAX_TOTAL_PAGES:

        start_page = page.number - PAGINATION_PAGES_AROUND_CURRENT
        for i in range(page.number - PAGINATION_PAGES_AROUND_CURRENT, page.number + 1):
            if i > 0:
                start_page = i
                break

        end_page = page.number + PAGINATION_PAGES_AROUND_CURRENT
        for i in range(page.number, page.number + PAGINATION_PAGES_AROUND_CURRENT):
            if i > paginator.num_pages:
                end_page = i
                break

        page_range = range(start_page, end_page)
    else:
        page_range = paginator.page_range

    # Set the template variables
    return {'page':       page,
            'page_range': page_range}


@register.inclusion_tag('tags/render_weight_log.html')
def render_weight_log(log, div_uuid):
    '''
    Renders a weight log series
    '''

    return {'log': log,
            'div_uuid': div_uuid}


@register.inclusion_tag('tags/license-sidebar.html')
def license_sidebar(license, author=None):
    '''
    Renders the license notice for exercises
    '''

    return {'license': license,
            'author': author}


@register.inclusion_tag('tags/language_select.html', takes_context=True)
def language_select(context, language):
    '''
    Renders a link to change the current language.
    '''

    return {'language_name': language[1],
            'path': 'images/icons/flag-{0}.svg'.format(language[0]),
            'i18n_path': context['i18n_path'][language[0]]}


@register.filter
def get_item(dictionary, key):
    '''
    Allows to access a specific key in a dictionary in a template
    '''
    return dictionary.get(key)


#
# Form utils
#
@register.filter(name='form_field_add_css')
def form_field_add_css(field, css):
    '''
    Adds a CSS class to a form field. This is needed among other places for
    bootstrap 3, which needs a 'form-control' class in the field itself
    '''
    return field.as_widget(attrs={"class": css})


@register.filter(name='is_checkbox')
def is_checkbox(field):
    '''
    Tests if a field element is a checkbox, as it needs to be handled slightly different

    :param field: a form field
    :return: boolen
    '''
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__


@register.inclusion_tag('tags/render_form_element.html')
def render_form_field(field):
    '''
    Renders a form field with all necessary labels, help texts and labels
    within 'form-group'.

    See bootstrap documentation for details: http://getbootstrap.com/css/#forms
    '''

    return {'field': field}


@register.inclusion_tag('tags/render_form_submit.html')
def render_form_submit(save_text='Save', button_class='default'):
    """
    Comfort function that renders a submit button with all necessary HTML
    and CSS

    :param save_text: the text to use on the submit button
    :param button_class: CSS class to apply to the button, default 'default'
    """
    if button_class in ('default',
                        'primary',
                        'success',
                        'info',
                        'warning',
                        'danger',
                        'link'):
        button_class = button_class
    else:
        button_class = 'default'

    return {'save_text': save_text,
            'button_class': button_class}


@register.inclusion_tag('tags/render_form_errors.html')
def render_form_errors(form):
    """
    Renders the non-field errors of a form with all necessary HTML and CSS
    (non-field errors refer to errors that can't be associated to any single
    field)

    :param form: the form object
    """
    return {'form': form}


@register.inclusion_tag('tags/render_form_fields.html')
def render_form_fields(form, submit_text='Save', show_save=True):
    '''
    Comfort function that renders all fields in a form, as well as the submit
    button

    Internally it simply calls the other table_form_* functions and will render
    the fields in the order they were defined. If you want to change this, you
    need to call table_form_field for each field yourself. This function will
    also render a hidden field with a CSRF token, so be sure to pass it to the
    template.

    It is still necessary to enclose its output in <form> tags!

    :param form: the form to be rendered
    :param save_text: the text to use on the submit button
    '''

    return {'form': form,
            'show_save': show_save,
            'submit_text': submit_text}