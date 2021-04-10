import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import random
from twilio.rest import Client
from .models import Profile, Address
from adminn.models import Books, Category, Author, \
    Cart, Order, Coupon, BulkCoupon

# Create your views here.

cats = Category.objects.all()
auts = Author.objects.all()


def home(request):
    books = Books.objects.all()
    context = {'books': books, 'cats': cats, 'auts': auts}
    return render(request, 'user/home.html', context)


def category(request, pk):
    cb = Category.objects.get(pk=pk)
    books = Books.objects.filter(category=cb)
    context = {'books': books, 'cats': cats, 'auts': auts}
    return render(request, 'user/home.html', context)


def author(request, pk):
    at = Author.objects.get(pk=pk)
    books = Books.objects.filter(author=at)
    context = {'books': books, 'cats': cats, 'auts': auts}
    return render(request, 'user/home.html', context)


def book_view(request, pk):
    book = Books.objects.get(pk=pk)
    context = {'book': book, 'cats': cats, 'auts': auts}
    return render(request, 'user/book_view.html', context)


def cart(request):
    if request.user.is_authenticated:
        my_cart = Cart.objects.filter(user=request.user, status='Pending')
        if not my_cart:
            message = "Your cart is Empty"
            context = {'cats': cats, 'auts': auts, 'my_cart': my_cart, 'message': message}
        else:
            sub_total = 0
            disc_sub_total = 0
            grand_total = 40

            for cart in my_cart:
                quantity = cart.quantity
                disc_price = cart.book.disc_price
                price = cart.book.price
                total_price = quantity * price
                sub_total += total_price

                cart.disc_total_price = quantity * disc_price
                disc_sub_total += cart.disc_total_price
                disc = sub_total - disc_sub_total
                grand_total += cart.disc_total_price

            context = {'cats': cats, 'auts': auts, 'my_cart': my_cart,
                       'total_price': total_price, 'sub_total': sub_total,
                       'disc': disc, 'grand_total': grand_total}
        return render(request, 'user/cart.html', context)
    else:
        return redirect(login)


@csrf_exempt
def cart_count(request):
    quantity = request.POST['qty']
    pk = request.POST['pk']
    Cart.objects.filter(pk=pk).update(user=request.user, quantity=quantity)
    return redirect(cart)


def add_to_cart(request, pk):
    book = Books.objects.get(pk=pk)
    mycart, created = Cart.objects.get_or_create(user=request.user, book=book, status='Pending')
    mycart.quantity += 1
    mycart.save()
    return redirect(home)


def buy_now(request, pk):
    book = Books.objects.get(pk=pk)
    mycart, created = Cart.objects.get_or_create(user=request.user, book=book, status='Pending')
    mycart.quantity += 1
    mycart.save()
    return redirect(cart)


def delete_cart(request, pk):
    my_cart = Cart.objects.get(pk=pk)
    my_cart.delete()
    return redirect(cart)


offer_id = 0


def checkout(request):
    my_cart = Cart.objects.filter(user=request.user, status='Pending')
    address = Address.objects.filter(user=request.user)
    user_prof = Profile.objects.get(user=request.user)
    active_off = Coupon.objects.filter(user=user_prof, status='active')
    other_off = BulkCoupon.objects.filter(user=user_prof, status='active')

    sub_total = 0
    disc_sub_total = 0
    grand_total = 0
    disc = 0
    for car in my_cart:
        car.total_price = car.quantity * car.book.price
        car.disc_total_price = car.quantity * car.book.disc_price
        sub_total += car.total_price
        disc_sub_total += car.disc_total_price
        disc = sub_total - disc_sub_total
        grand_total += car.disc_total_price
    request.session['grand_total'] = grand_total

    if not my_cart:
        return redirect(cart)

    elif request.method == 'POST':
        global offer_id
        offer_id = request.POST['offer_id']
        offer = request.POST['offer']
        current_total = request.session['grand_total']
        reduce = int(current_total) * int(offer) / 100
        final_offer_total = int(current_total) - int(reduce)
        request.session['grand_total'] = final_offer_total
        return JsonResponse(final_offer_total, safe=False)

    else:
        context = {'cats': cats, 'auts': auts, 'my_cart': my_cart, 'address': address,
                   'sub_total': sub_total, 'disc': disc, 'grand_total': grand_total,
                   'active_off': active_off, 'other_off': other_off}
        return render(request, 'user/checkout.html', context)


def shipping_address(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    country = request.POST['country']
    city = request.POST['city']
    zip_code = request.POST['zipcode']
    address = Address.objects.create(user=request.user, name=name, phone=phone, email=email, address=address,
                                     country=country, city=city, zip_code=zip_code)
    address.save()
    return JsonResponse('true', safe=False)


def del_address(request, pk):
    address = Address.objects.get(pk=pk)
    address.delete()
    return redirect(checkout)


@csrf_exempt
def select_address(request):
    address_id = request.POST['pk']
    request.session['address_id'] = address_id
    return JsonResponse('true', safe=False)


@csrf_exempt
def select_pay_methode(request):
    pay_method = request.POST['pay']
    request.session['pay_method'] = pay_method
    return JsonResponse('true', safe=False)


def add_coupon(request):
    code = request.POST['coupon_code']
    prof_user = Profile.objects.get(user=request.user)
    if Coupon.objects.filter(coupon_code=code).exists():
        coupon = Coupon.objects.get(coupon_code=code)
        if BulkCoupon.objects.filter(user=prof_user, name=coupon).exists():
            bc = BulkCoupon.objects.get(user=prof_user, name=coupon)
            if bc.status == 'active':
                return JsonResponse('1', safe=False)
            elif bc.status == 'used':
                return JsonResponse('2', safe=False)
        else:
            BulkCoupon.objects.create(user=prof_user, name=coupon)
            return JsonResponse('true', safe=False)
    else:
        return JsonResponse('false', safe=False)


def order(request):
    my_cart = Cart.objects.filter(user=request.user, status='Pending')
    if not my_cart:
        return redirect(cart)
    else:
        pk = request.session['address_id']
        address = Address.objects.get(pk=pk)
        sub_total = 0
        disc_sub_total = 0
        grand_total = request.session['grand_total']
        disc = 0
        pay_method = request.session['pay_method']
        context = {'cats': cats, 'auts': auts, 'my_cart': my_cart, 'address': address,
                   'sub_total': sub_total, 'disc': disc, 'grand_total': grand_total,
                   'pay_method': pay_method}
        return render(request, 'user/order.html', context)


@csrf_exempt
def success(request):
    my_cart = Cart.objects.filter(user=request.user, status='Pending').order_by('date')
    pk = request.session['address_id']
    address = Address.objects.get(pk=pk)
    try:
        global offer_id
        used_offer = Coupon.objects.get(id=offer_id)
        used_offer.status = 'used'
        used_offer.save()
    except:
        pass
    for car in my_cart:
        car.total_price = car.quantity * car.book.price
        car.disc_total_price = car.quantity * car.book.disc_price
        pay_method = request.session['pay_method']
        order1, created = Order.objects.update_or_create(user=request.user, item=car, price=car.disc_total_price,
                                                         address=address, status='Placed', pay_method=pay_method)
        order1.save()
        car.status = 'Ordered'
        car.save()
    context = {'cats': cats, 'auts': auts}
    return render(request, 'user/success.html', context)


def profile(request):
    prof = Profile.objects.get(user=request.user)
    orde = Order.objects.filter(user=request.user)
    active_off = Coupon.objects.filter(user=prof, status='active')
    used_off = Coupon.objects.filter(user=prof, status='used')
    context = {'cats': cats, 'auts': auts, 'prof': prof,
               'orde': orde, 'active_off': active_off, 'used_off': used_off}
    return render(request, 'user/profile.html', context)


def profile_pic(request):
    prof = Profile.objects.get(user=request.user)
    prof.image = request.FILES.get('profile_image')
    prof.save()
    return redirect(profile)


def order_status(request):
    order_id = request.POST['order_id']
    value = request.POST['clicked']
    this_order = Order.objects.get(pk=order_id)
    if value == 'Cancel':
        this_order.status = 'Canceled'
        this_order.save()
    elif value == 'Return':
        this_order.status = 'Returned'
        this_order.save()
    return JsonResponse('true', safe=False)


def edit_profile(request):
    if request.method == 'POST':
        prof = Profile.objects.get(user=request.user)
        pk = prof.user.pk
        prof.user.first_name = request.POST['f_name']
        prof.user.last_name = request.POST['l_name']
        prof.user.username = request.POST['u_name']
        prof.phone = request.POST['phone_num']
        prof.user.email = request.POST['email']
        prof.birth_date = request.POST['birth_date']
        prof.image = request.FILES.get('pp_image')
        if User.objects.exclude(pk=pk).filter(username=prof.user.username).exists():
            return JsonResponse('1', safe=False)
        elif User.objects.exclude(pk=pk).filter(email=prof.user.email).exists():
            return JsonResponse('2', safe=False)
        elif Profile.objects.exclude(pk=pk).filter(phone=prof.phone).exists():
            return JsonResponse('3', safe=False)
        else:
            prof.user.save()
            prof.save()
            print('saveddddd>>>>>>>')
            return JsonResponse('true', safe=False)
    else:
        prof = Profile.objects.get(user=request.user)
        context = {'cats': cats, 'auts': auts, 'prof': prof}
        return render(request, 'user/edit_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        username = request.POST['u_name']
        email = request.POST['email']
        password1 = request.POST['psd1']
        password2 = request.POST['psd2']
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            user = User.objects.get(username__exact=username)
            user.set_password(password1)
            update_session_auth_hash(request, user)
            user.save()
            return JsonResponse('true', safe=False)
        else:
            return JsonResponse('1', safe=False)
    else:
        return render(request, 'user/change_password.html')


def login(request):
    if request.user.is_authenticated:
        return redirect(home)
    elif request.method == 'POST':
        username = request.POST['u_name']
        password = request.POST['psd1']
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.is_active:
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return JsonResponse('true', safe=False)
                else:
                    return JsonResponse('upw', safe=False)
            else:
                return JsonResponse('blck', safe=False)
        else:
            return JsonResponse('und', safe=False)
    else:
        context = {'cats': cats, 'auts': auts}
        return render(request, 'user/login.html', context)


phone_number = 0
otp = 0


def otp_login(request):
    if request.user.is_authenticated:
        return redirect(home)
    elif request.method == 'POST':
        global phone_number
        phone_number = request.POST['phone_number']
        if Profile.objects.filter(phone=phone_number).exists():
            user = Profile.objects.get(phone=phone_number)
            # request.sessoin['phone_number'] = phone_number
            if user is not None:
                random_num = random.randint(1000, 9999)
                global otp
                otp = random_num
                account_sid = 'AC08d83bdc764a2355a9fbe896d1adf2d9'
                auth_token = 'fdf584bab513f19bca57778de08ec1ce'
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    body=f"Your OTP is {otp}",
                    from_='+13473913920',
                    to=f"+919497117447"
                )
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('upw', safe=False)
        else:
            return JsonResponse('nouser', safe=False)
    else:
        return render(request, 'user/otp_login.html')


def enter_otp(request):
    if request.method == 'POST':
        otp1 = request.POST['otp']
        global phone_number
        user = Profile.objects.get(phone=phone_number)
        thisuser = user.user
        global otp

        if int(otp1) == otp:
            auth.login(request, thisuser)
            return JsonResponse('true', safe=False)
    else:
        return render(request, 'user/enter_otp.html')


def signup(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect(home)
    elif request.method == 'POST':
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        username = request.POST['u_name']
        phone = request.POST['phone_num']
        email = request.POST['email']
        birth_date = request.POST['birth_date']
        password1 = request.POST['psd1']
        password2 = request.POST['psd2']

        if User.objects.filter(username=username).exists():
            return JsonResponse('1', safe=False)
        elif User.objects.filter(email=email).exists():
            return JsonResponse('2', safe=False)
        elif Profile.objects.filter(phone=phone).exists():
            return JsonResponse('3', safe=False)
        else:
            user = User.objects.create_user(first_name=f_name, last_name=l_name,
                                            username=username, email=email, password=password1)
            user.save()
            code = str(uuid.uuid4()).replace("-", "")[:12]
            registered_profile = Profile.objects.create(user=user, phone=phone,
                                                        birth_date=birth_date, code=code)
            random_num = random.randint(10, 9999)
            welcome_code = f"WELCOME{random_num}"
            Coupon.objects.create(name='Welcome', coupon_code=welcome_code,
                                  user=registered_profile, offer=50)
            profile_id = request.session.get('ref_profile')
            if profile_id is not None:
                recommended_by = User.objects.get(id=profile_id)
                recommended_by_profile = Profile.objects.get(user=recommended_by)
                registered_profile.recommended_by = recommended_by
                registered_profile.save()

                random_num = random.randint(10, 9999)
                ref_offer_code = f"REFERRAL1{random_num}"
                Coupon.objects.create(name='Referral', coupon_code=ref_offer_code,
                                      user=recommended_by_profile, offer=30)

                random_num = random.randint(10, 9999)
                ref_offer_code = f"REFERRAL2{random_num}"
                Coupon.objects.create(name='Referral', coupon_code=ref_offer_code,
                                      user=registered_profile, offer=30)
            a = auth.authenticate(username=username, password=password1)
            auth.login(request, a)
            return JsonResponse('true', safe=False)
    else:
        code = str(kwargs.get('ref_code'))
        try:
            profile = Profile.objects.get(code=code)
            request.session['ref_profile'] = profile.id
        except:
            pass
        return render(request, 'user/signup.html')


def logout(request):
    request.session.flush()
    return redirect(login)
