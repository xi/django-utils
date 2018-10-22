from django.forms.widgets import TextInput


class DatalistWidget(TextInput):
    template_name = 'utils/widgets/datalist.html'

    def __init__(self, *args, datalist=[], **kwargs):
        self.datalist = datalist
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        attrs = context['widgets']['attrs']
        attrs['list'] = attrs['id'] + '_list'
        context['datalist'] = self.datalist
        return context
