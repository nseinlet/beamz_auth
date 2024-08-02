import random
from django import template

register = template.Library()

@register.simple_tag
def random_background():
    picts = [
        'devin-rajaram-Ji_Lm0WbVYc-unsplash.jpg',
        'edgar-chaparro-HnFosyNwbPo-unsplash.jpg',
        'henk-van-der-steege-M-v1p5VMD90-unsplash.jpg',
        'henry-be-MWP9cxS4uCg-unsplash.jpg',
        'levi-frey-x19nNMWeo5A-unsplash.jpg',
        'malgorzata-frej-EQhpvZWdr5s-unsplash.jpg',
        'matt-briney-GQmkzcjry3A-unsplash.jpg',
        'ricardo-gomez-angel-j5gCOKZdm6I-unsplash.jpg',
    ]
    a, b = 0, len(picts)-1
    return '/static/img/' + picts[random.randint(a, b)]