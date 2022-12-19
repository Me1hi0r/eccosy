from datetime import datetime

from django.forms import ModelForm, DateTimeField, ModelChoiceField, IntegerField, widgets, Form
from .models import Order, Product

DATETIME_FORMAT = "%Y-%m-%dT%H:%M"


class OrderCreationForm(ModelForm):
    date_finish = DateTimeField(
        label='Finish order',
        widget=widgets.DateTimeInput(
            attrs={"type": "datetime-local", "value": lambda: datetime.now().strftime(DATETIME_FORMAT)}
        ),
        localize=True,
        required=False,
    )
    size = IntegerField()

    class Meta:
        model = Order
        fields = ('date_finish', 'size', 'comment')


class AddSizeForm(Form):
    size = IntegerField()
