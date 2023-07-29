import email
import json
from unicodedata import name
from django.shortcuts import render, redirect
from apis.models import UserInfoModel, ContactModel, ProductModel, CartModel
import random
import string
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from rest_framework.views import APIView
from rest_framework.response import Response
import openpyxl
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from datetime import *

#signup screen
@csrf_exempt
def signup(request):
        # POST request to add user details
        if request.method == 'POST':
                data=json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
                email = data.get('email')
                phone = data.get('phone')
                aadhar = data.get('aadhar')
                address = data.get('address')
                secret_question = data.get('secret_question')
                answer = data.get('answer')
                referral = 0
                last_serial_number_user = UserInfoModel.objects.order_by('-user_referral_code').first()
                if last_serial_number_user:
                    referral = int(last_serial_number_user.user_referral_code)+1
                else:
                    referral = 100000
                token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20))
                login_token = token
                if UserInfoModel.objects.filter(username=username):
                    return JsonResponse({'message': 'Username already taken'})
                if UserInfoModel.objects.filter(email=email):
                    return JsonResponse({'message': 'User already exist'}) 
                UserInfoModel.objects.create(username=username, password=password, email=email, phone=phone, aadhar=aadhar, address=address, secret_question=secret_question, answer=answer, user_referral_code=referral, login_token=login_token)
                return JsonResponse({'message': 'User details added successfully'})


#login screen
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            user = UserInfoModel.objects.get(username=username, password=password)
            if not user:
                # Generate a login token
                token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20))
                user.login_token = token
                user.save()
            else:
                token = user.login_token
            return JsonResponse({'token': token})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

@csrf_exempt
def forget_password(request):
    if request.method == 'PUT':
        data=json.loads(request.body)
        email = data.get('email')
        secret_question = data.get('secret_question')
        answer = data.get('answer')
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        user=UserInfoModel.objects.get(email=email, secret_question=secret_question, answer=answer)
        if user and new_password == confirm_new_password :
            user.password = new_password
            user.save()
            return JsonResponse({'message': 'Password updated successfully'})
        else:
            return JsonResponse({'error': 'Invalid Inputs'}, status=401)
          
#contact screen form
@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        email = data.get('email')
        message = data.get('message')
        ContactModel.objects.create(email=email, message=message)
        return JsonResponse({'message': 'Feedback saved successfully'})
    
#product view
@csrf_exempt
def product_details(request, product_id):
    if request.method == 'GET':
        product = ProductModel.objects.get(product_id = product_id)
        product_data = {
            'product_id' : product.product_id,
            'product_name': product.product_name,
            'product_price': str(product.product_price),
            'product_description': product.product_description,
            'product_image': product.product_image.url if product.product_image else None,
        }
        return JsonResponse(product_data)


#cart view
@csrf_exempt
def cart_view(request, username):
    if request.method == 'GET':
        user = UserInfoModel.objects.get(username = username)
        cart_items = CartModel.objects.filter(user=user)
        cart_data = []
        for cart_item in cart_items:
            product_data = {
                'image': cart_item.product.product_image.url,
                'name': cart_item.product.product_name,
                'user_id': cart_item.user.username,
                'product_id': cart_item.product.product_id,
                'final_quantity': cart_item.final_quantity,
                'total_price': str(cart_item.total_price),
                'payment_done': cart_item.payment_done ,
                'order_ref_id' : cart_item.order_ref_id
            }
            cart_data.append(product_data)
        return JsonResponse(cart_data, safe=False)


    elif request.method == 'POST':
        data=json.loads(request.body)
        user = UserInfoModel.objects.get(username = username)
        product_id = data.get('product_id')
        quantity = int(data.get('final_quantity'))

        try:
            product = ProductModel.objects.get(product_id=product_id)
        except ProductModel.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)

        total_price = float(product.product_price) * quantity
        ref_id = 0
        last_ref_id = CartModel.objects.order_by('-order_ref_id').first()
        if last_ref_id:
            ref_id = int(last_ref_id.order_ref_id)+1
        else:
            ref_id = 10000000
        cart_item = CartModel.objects.create(
            user=user,
            product=product,
            final_quantity=quantity,
            total_price=total_price,
            order_ref_id=ref_id
        )
        return JsonResponse({'success': 'Item added to the cart successfully.'})
    
    elif request.method == 'PUT':
        data=json.loads(request.body)
        order_ref_id = data.get('order_ref_id')
        quantity = int(data.get('final_quantity'))

        try:
            cart_item = CartModel.objects.get(order_ref_id=order_ref_id)
        except CartModel.DoesNotExist:
            return JsonResponse({'error': 'Item not found in the cart.'}, status=404)

        cart_item.final_quantity = quantity
        cart_item.total_price = float(cart_item.product.product_price) * quantity
        cart_item.save()
        return JsonResponse({'success': 'Cart item updated successfully.'})
    

    elif request.method == 'DELETE':
        data = json.loads(request.body)
        order_ref_id = data.get('order_ref_id')

        try:
            cart_item = CartModel.objects.get(order_ref_id=order_ref_id)
        except CartModel.DoesNotExist:
            return JsonResponse({'error': 'Item not found in the cart.'}, status=404)

        cart_item.delete()
        return JsonResponse({'success': 'Cart item deleted successfully.'})