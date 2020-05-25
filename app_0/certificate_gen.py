from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone

from xhtml2pdf import pisa


def render_to_pdf(instance, template_src):
    template = get_template(template_src)
    context_dict = {'type': instance.type, 'content': get_content(instance.type)}
    if instance.type == 'Income':
        context_dict['content'] = context_dict['content'].format(timezone.now().year,
                                                                 instance.requested_by.name.upper(),
                                                                 instance.annual_income)
    if instance.type == 'Caste':
        context_dict['content'] = context_dict['content'].format(instance.requested_by.name.upper(),
                                                                 instance.father.upper(),
                                                                 instance.address, instance.cast)
    if instance.type == 'Nativity':
        context_dict['content'] = context_dict['content'].format(instance.requested_by.name.upper(),
                                                                 instance.father.upper(),
                                                                 instance.address)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None


def get_content(key):
    data = {
        'Income': 'This is to certify that the annual income from all sources including share of joint family for the financial year of {} of Mr. / Ms. / Mrs.{}in Rs. {}',
        'Caste': 'This is to certify that Shri/ Smt./ Kumari {} son/daughter of {} of {} in the State/Union Territory Kerala belongs to the {} Community which is recognized by Government of India',
        'Nativity': 'This is to certify that Mr/Mrs {} S/o / D/o {} is resident of Kerala of address {} is the state of Kerala is subjected to Indian Union.',
    }
    return data[key]
