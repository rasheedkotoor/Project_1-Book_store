import base64
import pytz
import xlwt
from django.db.models import Count
from django.utils import timezone as tz
from django.shortcuts import render, redirect
from django.http import JsonResponse, QueryDict, HttpResponse
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from .models import *
from user.models import Profile


# Create your views here.


def home(request):
    total = 0
    monthly_total = 0
    daily_total = 0
    order_count = 0
    book_count = 0
    user_count = 0
    paypal_total = 0
    paypal_count = 0
    razor_pay_total = 0
    razor_pay_count = 0
    c_o_d_total = 0
    c_o_d_count = 0
    all_order = Order.objects.all()
    today = datetime.date.today()
    for allo in all_order:
        order_count += 1
        price = allo.price
        total += price
    monthly_order = Order.objects.filter(start_date__year=today.year,
                                         start_date__month=today.month)
    for allo in monthly_order:
        price = allo.price
        monthly_total += price
    daily_order = Order.objects.filter(start_date__year=today.year,
                                       start_date__month=today.month,
                                       start_date__day=today.day)
    for allo in daily_order:
        price = allo.price
        daily_total += price
    all_order = Order.objects.filter(pay_method='pay_pal')
    for allo in all_order:
        paypal_count += 1
        price = allo.price
        paypal_total += price
    all_order = Order.objects.filter(pay_method='razor_pay')
    for allo in all_order:
        razor_pay_count += 1
        price = allo.price
        razor_pay_total += price
    all_order = Order.objects.filter(pay_method='c_o_d')
    for allo in all_order:
        c_o_d_count += 1
        price = allo.price
        c_o_d_total += price
    all_book = Books.objects.all()
    for allb in all_book:
        book_count += 1
    all_user = User.objects.all()
    for allb in all_user:
        user_count += 1

    # last ten data collector
    last_ten_data = []
    last_ten_label = []
    c = 0
    for p in range(10):
        d = today - datetime.timedelta(days=c)
        c += 1
        one_day = Order.objects.filter(start_date=d)
        print(one_day, 'adsfasdfsadf')
        price = 0
        for one in one_day:
            price += one.price
        last_ten_data.append(price)
        last_ten_label.append(d)

    context = {'total': total, 'monthly_total': monthly_total, 'daily_total': daily_total,
               'user_count': user_count, 'order_count': order_count, 'paypal_total': paypal_total,
               'paypal_count': paypal_count, 'razor_pay_total': razor_pay_total,
               'razor_pay_count': razor_pay_count, 'c_o_d_total': c_o_d_total,
               'c_o_d_count': c_o_d_count, 'book_count': book_count,
               'data_order': last_ten_data, 'label_date': last_ten_label}
    return render(request, 'admin/overview.html', context)


def login(request):
    if request.session.has_key("key"):
        return redirect(home)
    if request.method == 'POST':
        u_name2 = request.POST['u_name1']
        p_word2 = request.POST['p_word1']
        if u_name2 == 'admin' and p_word2 == '123':
            request.session["key"] = 'sessionkey'
            # print(request)
            return JsonResponse('true', safe=False)
        else:
            return JsonResponse('false', safe=False)
    else:
        return render(request, 'admin/login.html')


def logout(request):
    request.session.flush()
    return redirect('login')


def userlist(request):
    users = Profile.objects.all()
    return render(request, 'admin/userlist.html', {'users': users})


def block_user(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
        user.save()
        messages.info(request, 'user is blocked')
    else:
        user.is_active = True
        user.save()
        messages.info(request, 'user is unblocked')
    return redirect(userlist)


def category(request):
    if request.method == 'POST':
        b_cat = request.POST['b_cat']
        if Category.objects.filter(category=b_cat).exists():
            messages.info(request, 'Category is already exists')
            return redirect(category)
        else:
            Category.objects.create(category=b_cat)
            return redirect(category)
    else:
        cats = Category.objects.all()
        context = {'cats': cats}
        return render(request, 'admin/category.html', context)


def add_offer(request):
    offer_value = request.POST['offer']
    cat = request.POST['cat']
    cat_off = Category.objects.get(category=cat)
    cat_off.offer = offer_value
    cat_off.save()
    books = Books.objects.filter(category=cat_off)
    for book in books:
        book.offer = offer_value
    book.save()
    return JsonResponse('true', safe=False)


def del_cat(request, pk):
    if request.session.has_key("key"):
        cat = Category.objects.get(pk=pk)
        cat.delete()
        return redirect(category)
    else:
        return redirect(login)


def booklist(request):
    books = Books.objects.all()
    cats = Category.objects.all()
    return render(request, 'admin/books.html', {'books': books, 'cats': cats})


def add_book(request):
    cats = Category.objects.all()
    if request.method == 'POST':
        name = request.POST['book_n']
        author = request.POST['author_n']
        publisher = request.POST['publish']
        year = request.POST['year']
        edition = request.POST['edition']
        page_no = request.POST['page_no']
        cate = request.POST['category']
        # label = request.POST['label']
        price = request.POST['price']
        offer = request.POST['offer']
        description = request.POST['description']
        image1 = request.POST['book_image1']
        image2 = request.POST['book_image2']

        format, imgstr1 = image1.split(';base64,')
        ext = format.split('/')[-1]
        img1 = ContentFile(base64.b64decode(imgstr1), name=name + '.' + ext)
        format, imgstr2 = image2.split(';base64,')
        img2 = ContentFile(base64.b64decode(imgstr2), name=name + '.' + ext)

        if Books.objects.filter(name=name).exists():
            messages.info(request, 'Book is already exists')
            return redirect(add_book)
        else:
            cat1 = Category.objects.get(category=cate)
            aut1, created = Author.objects.get_or_create(name=author)
            Books.objects.create(name=name, author=aut1,
                                 publisher=publisher, year=year, edition=edition,
                                 page_no=page_no, category=cat1, price=price,
                                 offer=offer, description=description, image1=img1,
                                 image2=img2)
            return redirect(booklist)
    else:
        return render(request, 'admin/add_book.html', {'cats': cats})


def edit_book(request, pk):
    if request.session.has_key("key"):
        cats = Category.objects.all()
        if request.method == 'GET':
            book = Books.objects.get(pk=pk)
            img1, img2 = book.image1, book.image2
            imgstr1 = base64.b64encode(img1.read())
            imgstr2 = base64.b64encode(img2.read())
            context = {'book': book, 'cats': cats, 'imgstr2': imgstr2, 'imgstr1': imgstr1}
            return render(request, 'admin/edit_book.html', context)
        if request.method == 'POST':
            book = Books.objects.get(pk=pk)
            cat2 = request.POST['category']
            author = request.POST['author_n']
            cat1 = Category.objects.get(category=cat2)
            aut1, created = Author.objects.get_or_create(name=author)
            img1 = request.POST['book_image1']
            img2 = request.POST['book_image2']
            format, imgstr1 = img1.split(';base64,')
            ext = format.split('/')[-1]
            img3 = ContentFile(base64.b64decode(imgstr1), name=book.name + '.' + ext)
            format, imgstr2 = img2.split(';base64,')
            img4 = ContentFile(base64.b64decode(imgstr2), name=book.name + '.' + ext)

            book.name = request.POST['book_n']
            book.author = aut1
            book.publisher = request.POST['publish']
            book.year = request.POST['year']
            book.edition = request.POST['edition']
            book.page_no = request.POST['page_no']
            book.category = cat1
            # label = request.POST['label']
            book.price = request.POST['price']
            book.offer = request.POST['offer']
            book.description = request.POST['description']
            book.image1 = img3
            book.image2 = img4

            if Books.objects.exclude(pk=pk).filter(name=book.name).exists():
                messages.info(request, 'Book is already exists')
                return redirect(add_book)
            else:
                book.save()
                return redirect(booklist)
    else:
        return redirect(login)


def view_book(request, pk):
    if request.session.has_key("key"):
        book = Books.objects.get(pk=pk)
        return render(request, 'admin/view_book.html', {'book': book})

    else:
        return redirect(login)


def delete_book(request, pk):
    if request.session.has_key("key"):
        book = Books.objects.get(pk=pk)
        book.delete()
        # messages.warning(request, 'User is deleted')
        return redirect(booklist)
    else:
        return redirect(login)


def order_manage(request):
    orders = Order.objects.filter().order_by('-start_date')
    context = {'orders': orders}
    return render(request, 'admin/order_manage.html', context)


def admin_order_status(request):
    order_id = request.POST['order_id']
    value = request.POST['clicked']
    this_order = Order.objects.get(pk=order_id)
    if request.POST['clicked'] == 'Shipped':
        this_order.status = 'Shipped'
        this_order.save()
    elif request.POST['clicked'] == 'Delivered':
        this_order.status = 'Delivered'
        this_order.save()
    return JsonResponse('true', safe=False)


g_orders = 0


def report(request):
    if request.method == 'POST':
        date = request.POST['start_date']
        start_date = date[0:10]
        end_date = date[13:23]
        # start_date = request.POST['start_date']
        # end_date = request.POST['end_date']
        global g_orders
        g_orders = Order.objects.filter(start_date__range=[start_date, end_date]).order_by('-start_date')
    else:
        g_orders = Order.objects.filter().order_by('-start_date')
    context = {'orders': g_orders}
    return render(request, 'admin/report.html', context)


def download_excel_data(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("sheet1")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Order Id', 'Item', 'Customer', 'Date', 'Quantity', 'Price',
               'Payment Method', 'Status']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    global g_orders
    for my_row in g_orders:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row.id, font_style)
        ws.write(row_num, 1, my_row.item.book.name, font_style)
        ws.write(row_num, 2, my_row.user.username, font_style)
        ws.write(row_num, 3, my_row.start_date, font_style)
        ws.write(row_num, 4, my_row.item.quantity, font_style)
        ws.write(row_num, 5, my_row.price, font_style)
        ws.write(row_num, 6, my_row.pay_method, font_style)
        ws.write(row_num, 7, my_row.status, font_style)
    wb.save(response)
    return response


def coupon(request):
    if request.method == 'POST':
        coupon_name = request.POST['coupon_name']
        coupon_code = request.POST['coupon_code']
        coupon_offer = request.POST['coupon_offer']
        Coupon.objects.create(name=coupon_name, coupon_code=coupon_code, offer=coupon_offer)
        return redirect(coupon)
    else:
        null_offer = Coupon.objects.filter(user__isnull=True)
        count = 0
        for i in null_offer:
            bulk_coupon = BulkCoupon.objects.values('name').annotate(Count('id')).order_by().filter(id__count__gt=0)
            print(bulk_coupon.id__count, "//////////////////////")
        context = {'bulk_coupon': bulk_coupon, 'null_offer': null_offer}
        return render(request, 'admin/coupon.html', context)
