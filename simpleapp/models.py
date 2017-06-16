# coding=utf-8
from __future__ import unicode_literals

import xlsxwriter
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from diplomka import settings


def file_upload_to(instance, filename):
    return "%s" % filename


class Faculty(models.Model):
    name = models.CharField(max_length=100, verbose_name='Отделение')
    lessons = models.ManyToManyField('Lesson')
    quota = models.IntegerField(default=0)
    filled_quota = models.IntegerField(default=0)
    manager = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.name


class Tour(models.Model):
    name = models.CharField(max_length=100)
    initial = models.DateTimeField(null=True, blank=True)
    final = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Protocol(models.Model):
    tour = models.ForeignKey(Tour)
    protocol = models.FileField(upload_to=file_upload_to)
    date = models.DateTimeField(auto_now=True)


class Otchet(models.Model):
    tour = models.ForeignKey(Tour, null=True)
    department = models.ForeignKey(Faculty, null=True)
    otchet = models.FileField(upload_to=file_upload_to, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        faculty = self.department
        tour = self.tour
        alumnis = Alumni.objects.filter(faculty=faculty, tour=tour)
        shaar = alumnis.filter(place=u'Шаар').exclude(olimpiadnik=True)
        borbor = alumnis.filter(place=u'Борбор').exclude(olimpiadnik=True)
        aiyl = alumnis.filter(place=u'Айыл').exclude(olimpiadnik=True)
        too = alumnis.filter(place=u'Тоо').exclude(olimpiadnik=True)
        olimpiadniki = alumnis.filter(olimpiadnik=True)
        name = settings.BASE_DIR + u'/static_in_env/media_root/otchet_%s_%s.xlsx' % (tour.name, faculty.name)
        workbook = xlsxwriter.Workbook(name)
        worksheet = workbook.add_worksheet('Result')
        worksheet.set_column('A:A', 1.5)
        worksheet.set_column('B:Z', 5)
        format = workbook.add_format({'bg_color': 'red',
                                      'align': 'center',
                                      'valign': 'vcenter',
                                      'font_size': 7,
                                      'border': 1})
        worksheet.set_default_row(11)
        cell_format = workbook.add_format({'align': 'center',
                                           'valign': 'vcenter',
                                           'font_size': 7,
                                           'border': 1})
        cell_format_name = workbook.add_format({'align': 'center',
                                                'valign': 'vcenter',
                                                'font_size': 7,
                                                'border': 1})
        worksheet.merge_range('A1:K1', u"%s багыты боюнча" % faculty.name, cell_format)
        worksheet.merge_range('A2:K2', u"%sда катышкандардын тизмеси" % tour.name, cell_format)
        worksheet.merge_range('A3:K3', u"Кабыл алуу планы: %s" % faculty.filled_quota, cell_format)
        worksheet.merge_range('A5:A6', 'N', cell_format)
        worksheet.merge_range('B5:E5', u'Шаар', format)
        format_blue = workbook.add_format({'bg_color': 'blue',
                                           'align': 'center',
                                           'valign': 'vcenter',
                                           'font_size': 7,
                                           'border': 1})
        worksheet.merge_range('F5:I5', u'Кичи шаар жана обл. борборлор', format_blue)
        format_yellow = workbook.add_format({'bg_color': 'yellow',
                                             'align': 'center',
                                             'valign': 'vcenter',
                                             'font_size': 7,
                                             'border': 1})
        worksheet.merge_range('J5:M5', u'Айыл жергеси', format_yellow)
        format_purple = workbook.add_format({'bg_color': 'purple',
                                             'align': 'center',
                                             'valign': 'vcenter',
                                             'font_size': 7,
                                             'border': 1})
        worksheet.merge_range('N5:Q5', u'Бийик тоолу аймак', format_purple)
        format_white = workbook.add_format({'align': 'center',
                                            'valign': 'vcenter',
                                            'font_size': 7,
                                            'border': 1})
        worksheet.merge_range('R5:U5', u'Олимпиада жеңүүчүлөрү', format_white)
        worksheet.write('B6', u'Иден', cell_format_name)
        worksheet.write('C6', u'Негизги', cell_format_name)
        worksheet.write('D6', u'Кошумча', cell_format_name)
        worksheet.write('E6', u'Суммасы', cell_format_name)
        worksheet.write('F6', u'Иден', cell_format_name)
        worksheet.write('G6', u'Негизги', cell_format_name)
        worksheet.write('H6', u'Кошумча', cell_format_name)
        worksheet.write('I6', u'Суммасы', cell_format_name)
        worksheet.write('J6', u'Иден', cell_format_name)
        worksheet.write('K6', u'Негизги', cell_format_name)
        worksheet.write('L6', u'Кошумча', cell_format_name)
        worksheet.write('M6', u'Суммасы', cell_format_name)
        worksheet.write('N6', u'Иден', cell_format_name)
        worksheet.write('O6', u'Негизги', cell_format_name)
        worksheet.write('P6', u'Кошумча', cell_format_name)
        worksheet.write('Q6', u'Суммасы', cell_format_name)
        worksheet.write('R6', u'Иден', cell_format_name)
        worksheet.write('S6', u'Негизги', cell_format_name)
        worksheet.write('T6', u'Кошумча', cell_format_name)
        worksheet.write('U6', u'Суммасы', cell_format_name)
        worksheet.set_row(5, 30)
        l = [shaar.count(), aiyl.count(), too.count(), borbor.count(), olimpiadniki.count()]
        m = max(l)
        for i in 'ABCDEFGHIJKLMNOPQRSTU':
            for j in range(7, m + 7):
                worksheet.write('%s%s' % (i, j), None, cell_format_name)
        counter = 6
        for i in shaar:
            counter += 1
            worksheet.write('B%s' % str(counter), i.ortId, cell_format_name)
            worksheet.write('C%s' % str(counter), i.main, cell_format_name)
            worksheet.write('D%s' % str(counter), i.extra_num, cell_format_name)
            worksheet.write('E%s' % str(counter), i.summa, cell_format_name)
            worksheet.write('A%s' % str(counter), counter - 6, cell_format_name)
        counter = 6
        for i in borbor:
            counter += 1
            worksheet.write('F%s' % str(counter), i.ortId, cell_format_name)
            worksheet.write('G%s' % str(counter), i.main, cell_format_name)
            worksheet.write('H%s' % str(counter), i.extra_num, cell_format_name)
            worksheet.write('I%s' % str(counter), i.summa, cell_format_name)
            worksheet.write('A%s' % str(counter), counter - 6, cell_format_name)
        counter = 6
        for i in aiyl:
            counter += 1
            worksheet.write('J%s' % str(counter), i.ortId, cell_format_name)
            worksheet.write('K%s' % str(counter), i.main, cell_format_name)
            worksheet.write('L%s' % str(counter), i.extra_num, cell_format_name)
            worksheet.write('M%s' % str(counter), i.summa, cell_format_name)
            worksheet.write('A%s' % str(counter), counter - 6, cell_format_name)
        counter = 6
        for i in too:
            counter += 1
            worksheet.write('N%s' % str(counter), i.ortId, cell_format_name)
            worksheet.write('O%s' % str(counter), i.main, cell_format_name)
            worksheet.write('P%s' % str(counter), i.extra_num, cell_format_name)
            worksheet.write('Q%s' % str(counter), i.summa, cell_format_name)
            worksheet.write('A%s' % str(counter), counter - 6, cell_format_name)
        counter = 6
        for i in olimpiadniki:
            counter += 1
            worksheet.write('R%s' % str(counter), i.ortId, cell_format_name)
            worksheet.write('S%s' % str(counter), i.main, cell_format_name)
            worksheet.write('T%s' % str(counter), i.extra_num, cell_format_name)
            worksheet.write('U%s' % str(counter), i.summa, cell_format_name)
            worksheet.write('A%s' % str(counter), counter - 6, cell_format_name)
        m += 6
        worksheet.write('B%s' % (m + 3), u'Всего', cell_format_name)
        worksheet.write('C%s' % (m + 3), alumnis.count(), cell_format_name)
        worksheet.write('D%s' % (m + 5), u'Квота', cell_format_name)
        worksheet.merge_range('B%s:C%s' % (m + 5, m + 5), u'Шаар', cell_format_name)
        worksheet.write('G%s' % (m + 5), u'Квота', cell_format_name)
        worksheet.merge_range('E%s:F%s' % (m + 5, m + 5), u'Кичи шаар ж/а обл.', cell_format_name)
        worksheet.write('J%s' % (m + 5), u'Квота', cell_format_name)
        worksheet.merge_range('H%s:I%s' % (m + 5, m + 5), u'Айыл жергеси', cell_format_name)
        worksheet.write('M%s' % (m + 5), u'Квота', cell_format_name)
        worksheet.merge_range('K%s:L%s' % (m + 5, m + 5), u'Бийик тоолу айм.', cell_format_name)
        worksheet.write('P%s' % (m + 5), u'Квота', cell_format_name)
        worksheet.merge_range('N%s:O%s' % (m + 5, m + 5), u'Олимпиада жең.', cell_format_name)
        if alumnis.count() != 0:
            x = (faculty.filled_quota - olimpiadniki.count()) / (alumnis.count() - olimpiadniki.count())
            n = shaar.count() * x
            k = borbor.count() * x
            o = aiyl.count() * x
            p = too.count() * x
        else:
            n = 0
            k = 0
            o = 0
            p = 0
        worksheet.write('D%s' % (m + 6), n, cell_format_name)
        worksheet.merge_range('B%s:C%s' % (m + 6, m + 6), shaar.count(), cell_format_name)
        worksheet.write('G%s' % (m + 6), k, cell_format_name)
        worksheet.merge_range('E%s:F%s' % (m + 6, m + 6), borbor.count(), cell_format_name)
        worksheet.write('J%s' % (m + 6), o, cell_format_name)
        worksheet.merge_range('H%s:I%s' % (m + 6, m + 6), aiyl.count(), cell_format_name)
        worksheet.write('M%s' % (m + 6), p, cell_format_name)
        worksheet.merge_range('K%s:L%s' % (m + 6, m + 6), too.count(), cell_format_name)
        worksheet.write('P%s' % (m + 6), 0, cell_format_name)
        worksheet.merge_range('N%s:O%s' % (m + 6, m + 6), 0, cell_format_name)
        barcode_worksheet = workbook.add_worksheet('Barcode')
        barcode_worksheet.set_column('A:A', 1.5)
        barcode_worksheet.set_column('B:B', 28)
        barcode_worksheet.set_column('C:C', 20)
        barcode_worksheet.set_column('D:D', 18)
        barcode_worksheet.set_column('E:E', 5)
        barcode_worksheet.set_column('F:F', 14)
        barcode_worksheet.set_column('G:G', 12)
        barcode_format = workbook.add_format({'align': 'center',
                                              'valign': 'vcenter',
                                              'font_size': 10,
                                              'border': 1})
        g = ord('G')
        for i in faculty.lessons.all():
            g += 1
            barcode_worksheet.write('%s1' % chr(g), i.name, barcode_format)
        barcode_worksheet.write('A1', u'№', barcode_format)
        barcode_worksheet.write('B1', u'поле для ввода со сканера ШК', barcode_format)
        barcode_worksheet.write('C1', u'регистрационный номер', barcode_format)
        barcode_worksheet.write('D1', u'цвет сертификата', barcode_format)
        barcode_worksheet.write('E1', u'тур', barcode_format)
        barcode_worksheet.write('F1', u'красный аттестат', barcode_format)
        barcode_worksheet.write('G1', u'телефон', barcode_format)
        count = 1
        for i in alumnis.all():
            count += 1
            barcode_worksheet.write('B%s' % count, i.barcode, barcode_format)
            barcode_worksheet.write('A%s' % count, count - 1, barcode_format)
            barcode_worksheet.write('C%s' % count, i.ortId, barcode_format)
            if i.place == u'Шаар':
                barcode_worksheet.write('D%s' % count, u'К', format)
            if i.place == u'Борбор':
                barcode_worksheet.write('D%s' % count, u'С', format_blue)
            if i.place == u'Айыл':
                barcode_worksheet.write('D%s' % count, u'Ж', format_yellow)
            else:
                barcode_worksheet.write('D%s' % count, u'Ф', format_purple)
            barcode_worksheet.write('E%s' % count, i.tour.name, barcode_format)
            if i.atestat:
                barcode_worksheet.write('F%s' % count, '*', barcode_format)
            else:
                barcode_worksheet.write('F%s' % count, ' ', barcode_format)
            barcode_worksheet.write('G%s' % count, i.phone, barcode_format)
            g = ord('G')
            for j in faculty.lessons.all():
                g += 1
                barcode_worksheet.write('%s%s' % (chr(g), count), AlumniLesson.objects.get(lesson=j, alumni=i).grade,
                                        barcode_format)

        journal_worksheet = workbook.add_worksheet('Journal')
        journal_worksheet.set_column('A:A', 1.5)
        journal_worksheet.set_column('B:G', 10)
        journal_format = workbook.add_format({'align': 'center',
                                              'valign': 'vcenter',
                                              'font_size': 8,
                                              'border': 1})
        journal_worksheet.write('A1', u'№', journal_format)
        journal_worksheet.write('B1', u'Идент.', journal_format)
        journal_worksheet.write('C1', u'Основной', journal_format)
        journal_worksheet.write('D1', u'Доп', journal_format)
        journal_worksheet.write('E1', u'Сумма', journal_format)
        journal_worksheet.write('F1', u'Категория', journal_format)
        journal_worksheet.write('G1', u'Атестат', journal_format)
        journal_worksheet.set_default_row(11)
        c = 0
        for i in alumnis.all():
            c += 1
            journal_worksheet.write('A%s' % (c + 1), c, journal_format)
            journal_worksheet.write('B%s' % (c + 1), i.ortId, journal_format)
            journal_worksheet.write('C%s' % (c + 1), i.main, journal_format)
            journal_worksheet.write('D%s' % (c + 1), i.extra_num, journal_format)
            journal_worksheet.write('E%s' % (c + 1), i.summa, journal_format)
            if i.place == u'Шаар':
                journal_worksheet.write('F%s' % (c + 1), u'К', format)
            if i.place == u'Борбор':
                journal_worksheet.write('F%s' % (c + 1), u'С', format_blue)
            if i.place == u'Айыл':
                journal_worksheet.write('F%s' % (c + 1), u'Ж', format_yellow)
            else:
                journal_worksheet.write('F%s' % (c + 1), u'Ф', format_purple)
            if i.atestat:
                journal_worksheet.write('G%s' % (c + 1), '*', journal_format)
            else:
                journal_worksheet.write('G%s' % (c + 1), ' ', journal_format)
            workbook.close()
        self.otchet = '/media/otchet_%s_%s.xlsx' % (tour.name, faculty.name)
        super(Otchet, self).save()


class Lesson(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Alumni(models.Model):
    class Meta:
        ordering = ['summa']

    choices = (
        ('Шаар', 'Шаар'),
        ('Борбор', 'Борбор'),
        ('Айыл', 'Айыл'),
        ('Тоо', 'Тоо'),
    )
    barcode = models.CharField(max_length=100, null=True)
    ortId = models.CharField(max_length=100)
    tour = models.ForeignKey(Tour, null=True)
    faculty = models.ForeignKey(Faculty, null=True)
    place = models.CharField(max_length=100, null=True, choices=choices)
    extra_num = models.IntegerField(default=0)
    main = models.IntegerField(default=0)
    atestat = models.BooleanField(default=False)
    lgotnik = models.BooleanField(default=False)
    olimpiadnik = models.BooleanField(default=False)
    passed = models.BooleanField(default=False)
    summa = models.IntegerField(default=0)
    phone = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.barcode

    def get_main(self):
        less = Lesson.objects.get(name='Основной')
        alumnilesson = AlumniLesson.objects.get(lesson=less, alumni=self)
        return alumnilesson.grade


class AlumniLesson(models.Model):
    alumni = models.ForeignKey(Alumni, null=True)
    lesson = models.ForeignKey(Lesson, null=True)
    grade = models.IntegerField(default=0)

    def __unicode__(self):
        return self.lesson.name
