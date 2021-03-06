# coding: UTF-8
from django import forms
# locals
from shop.models import Order


class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(label=u'Количество',
                                  widget=forms.TextInput(attrs={'size': '2', 'value': '1', 'maxlength': '5'}),
                                  error_messages={'invalid': u'Введите правильное количество.'}, min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies должны быть включены.")
        return self.cleaned_data


class SearchForm(forms.Form):
    search = forms.CharField(max_length=150, label='', required=False,
                             widget=forms.TextInput(attrs={'placeholder': 'Поиск',
                                                           'class': 'input-block-level search-query'}))

'''
class PropertiesFilter(forms.Form):
    """
    Форма фильтрации товаров по их свойствам.
    category_pk - id категории товаров, передается при вызове формы с views.py.
    У каждой категории могут быть свои свойства.
    Если не указано category_pk, то выводятся все свойства.
    """

    def __init__(self, category_pk=None, *args, **kwargs):
        self.category_pk = category_pk
        super(PropertiesFilter, self).__init__(*args, **kwargs)

        if not category_pk:
            properties = Properties.objects.all().order_by('propName')
        else:
            # сделать сортировку по алфавиту
            properties1 = Properties.objects.filter(category=None).order_by('propName')
            properties2 = Properties.objects.filter(category=category_pk).order_by('propName')
            properties = chain(properties1, properties2)

        for i, prop in enumerate(properties):
            properties_list = tuple(set(ItemProperties.objects.filter(prop=prop.pk)
                                        .values_list('propValue', 'propValue')))
            self.fields['items_%s' % i] = forms.MultipleChoiceField(
                required=False,
                widget=forms.CheckboxSelectMultiple,
                choices=properties_list,
                label=prop.propName
            )

    def clean(self):
        # т.к. все поля required=False, то нужно передавать только заполненные поля
        form_data = super(PropertiesFilter, self).clean()
        cleaned_data = {}
        for key, value in form_data.items():
            if len(value):
                cleaned_data[key] = value
        return cleaned_data
'''

class Checkout(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('status', 'date')

    def __init__(self, *args, **kwargs):
        super(Checkout, self).__init__(*args, **kwargs)

        for field in self.fields:
            field = self.fields.get(field)
            if field:
                field.widget.attrs.update({'placeholder': field.label})
