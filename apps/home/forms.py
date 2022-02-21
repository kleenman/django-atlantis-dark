from django.forms import ModelForm, NumberInput, Select
from .models import Bbr, Drink, Mark


class MarkForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(MarkForm, self).__init__(*args, **kwargs)
    #     self.fields['drink'].choices = [(n, '{name} ---- {price:,.2f}€'
    #                                      .format(name=n.name, price=n.price)
    #
    #                                      .replace('.', ',')) for n in Drink.objects.all()]
    class Meta:
        model = Mark
        fields = ['drink', 'units']
        widgets = {
            'units': NumberInput()
        }
        labels = {
            'drink': 'Getränk',
            'units': 'Menge'
        }


