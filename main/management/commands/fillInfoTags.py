from django.core.management import BaseCommand
from django.db import IntegrityError

from main.models import ProductInfoTags

tags = [
    ProductInfoTags(title="Последний штрих"),
    ProductInfoTags(title="Куполообразный верх"),
    ProductInfoTags(title="С отворотом"),
    ProductInfoTags(title="С ушами"),
    ProductInfoTags(title="Так и просятся в корзину покупок"),
    ProductInfoTags(title="Дизайн Space Jam"),
    ProductInfoTags(title="Высокий дизайн"),
    ProductInfoTags(title="Вспомогательные петли для легкого надевания"),
    ProductInfoTags(title="На шнуровке"),
    ProductInfoTags(title="Язычок и задник с мягкими вставками"),
    ProductInfoTags(title="Прочная резиновая подошва снаружи"),
    ProductInfoTags(title="Рифленая подошва"),
    ProductInfoTags(title="Из подборки экологичной моды"),
    ProductInfoTags(title="В полоску"),
    ProductInfoTags(title="Эластичный пояс с логотипом бренда"),
    ProductInfoTags(title="Боковые карманы"),
    ProductInfoTags(title="Прямой крой"),
    ProductInfoTags(title="Эксклюзивно для ASOS 4505"),
    ProductInfoTags(title="Широкий воротник"),
    ProductInfoTags(title="Застежка на кнопки"),
    ProductInfoTags(title="Вышивка логотипа на груди"),
    ProductInfoTags(title="Укороченная длина"),
    ProductInfoTags(title="Классическая крой"),
]


class Command(BaseCommand):
    help = f"Fills the database with the following products info tags: {tags}"

    def handle(self, *args, **options):
        for tag in tags:
            try:
                tag.save()
            except IntegrityError:
                pass

        self.stdout.write(self.style.SUCCESS("Successfully filled product info tags"))
