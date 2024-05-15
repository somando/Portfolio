from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from .models import *
import random, string

# Create your views here.
def top(request):
    
    static_profile = StaticProfileData.objects.first()
    static_profile.description = static_profile.description.replace('\span', "</span><span>")
    
    profiles = ProfileData.objects.all()
    for profile in profiles:
        profile.detail = profile.detail.replace('\span', "</span><span>")
    
    experiences = ExperienceData.objects.all().order_by('date').filter(show_top=True)
    for experience in experiences:
        date_list = str(experience.date).split('-')
        experience.date = date_list[0] + '/' + date_list[1]
        experience.title = experience.title.replace('\span', "</span><span>")
    
    products = ProductsData.objects.all().order_by('-date').filter(show_top=True)
    for product in products:
        product.title = product.title.replace('\span', "</span><span>")
        product.event = product.event.replace('\span', "</span><span>")
        product.team = product.team.replace('\span', "</span><span>")
        product.prize = product.prize.replace('\span', "</span><span>")
        product.link_title = product.link_title.replace('\span', "</span><span>")
    
    skills = SkillData.objects.all()
    
    return render(request, 'somando/top.html', {
        'static_profile': static_profile,
        'profiles': profiles,
        'experiences': experiences,
        'products': products,
        'skills': skills,
    })


def experiences(request):
    
    experiences = ExperienceData.objects.all().order_by('date')
    for experience in experiences:
        date_list = str(experience.date).split('-')
        experience.date = date_list[0] + '/' + date_list[1]
        experience.title = experience.title.replace('\span', "</span><span>")
        experience.detail = experience.detail.replace('\n', "</span><br><span>").replace('\span', "</span><span>")
    
    return render(request, 'somando/experiences.html', {
        'experiences': experiences,
    })


def products(request):
    
    products = ProductsData.objects.all().order_by('-date')
    for product in products:
        date_list = str(product.date).split('-')
        product.date = date_list[0] + '/' + date_list[1]
        if product.technology != '':
            technology_list = product.technology.split('\n')
            product.technology = []
            for technology in technology_list:
                technology = technology.split(' \ ')
                product.technology.append(technology)
        if product.infrastracture != '':
            infrastracture_list = product.infrastracture.split('\n')
            product.infrastracture = []
            for infrastructure in infrastracture_list:
                infrastructure = infrastructure.split(' \ ')
                product.infrastracture.append(infrastructure)
        product.title = product.title.replace('\span', "</span><span>")
        product.event = product.event.replace('\span', "</span><span>")
        product.team = product.team.replace('\span', "</span><span>")
        product.prize = product.prize.replace('\span', "</span><span>")
        product.link_title = product.link_title.replace('\span', "</span><span>")
        product.about = product.about.replace('\n', "</span><br><span>").replace('\span', "</span><span>")
    
    return render(request, 'somando/products.html', {
        'products': products,
    })

def product(request, url):
    
    if (ProductsData.objects.filter(url=url).count() == 0):
        return render(request, '404.html', status=404)
    
    product = ProductsData.objects.get(url=url)
    
    date_list = str(product.date).split('-')
    product.date = date_list[0] + '/' + date_list[1]
    if product.technology != '':
        technology_list = product.technology.split('\n')
        product.technology = []
        for technology in technology_list:
            technology = technology.split(' \ ')
            product.technology.append(technology)
    if product.infrastracture != '':
        infrastracture_list = product.infrastracture.split('\n')
        product.infrastracture = []
        for infrastructure in infrastracture_list:
            infrastructure = infrastructure.split(' \ ')
            product.infrastracture.append(infrastructure)
    product.title = product.title.replace('\span', "</span><span>")
    product.event = product.event.replace('\span', "</span><span>")
    product.team = product.team.replace('\span', "</span><span>")
    product.prize = product.prize.replace('\span', "</span><span>")
    product.link_title = product.link_title.replace('\span', "</span><span>")
    description = product.about.replace('/n', '').replace('\span', "")
    product.about = product.about.replace('\n', "</span><br><span>").replace('\span', "</span><span>")
    product.detail = product.detail.replace('\n', "</span></span><br><span class='br'><span>").replace('\span', "</span><span>")
    
    return render(request, 'somando/product.html', {
        'product': product,
        'description': description,
    })

def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def contact(request):
    
    if request.method == "GET":
        
        response = render(request, 'somando/contact.html', {
            'open': False,
        })
        
        if request.COOKIES.get('contact_room_id') != None:
            
            room_id = request.COOKIES.get('contact_room_id')
            auth_code = request.COOKIES.get('contact_room_auth')
            
            if ContactRoomData.objects.filter(room_id=room_id, close=False).exists():
                
                room = ContactRoomData.objects.get(room_id=room_id)
                
                if room.auth_code == auth_code:
                    
                    return render(request, 'somando/contact.html', {
                        'open': True,
                        'id': room_id,
                        'email': room.email,
                        'auth': auth_code,
                    })
            
            response.delete_cookie('contact_room_id')
            response.delete_cookie('contact_room_auth')
        
        return response
    
    elif request.method == "POST":
        
        name = request.POST['name']
        email = request.POST['email']
        organization = request.POST['organization']
        details = request.POST['details']
        
        while True:
            room_id = randomname(20)
            if ContactRoomData.objects.filter(room_id=room_id).count() == 0:
                break
        
        auth_code = randomname(6)
        
        ContactRoomData.objects.create(
            room_id = room_id,
            auth_code = auth_code,
            email = email,
            close = False,
        )
        
        ContactMessageData.objects.create(
            room_id = room_id,
            user = name,
            organization = organization,
            admin = False,
            message = details,
        )
        
        subject = 'お問い合わせを受け付けました｜Soma Ando'
        
        context = {
            'name': name, 
            'email': email, 
            'organization': organization, 
            'message': details, 
            'id': room_id, 
            'key': auth_code,
        }
        txt_content = get_template('mail/contact_create.txt').render(context)
        mail = EmailMultiAlternatives(subject=subject, body=txt_content, from_email='no-reply@somando.jp', to=[email], bcc=['info@somando.jp'])
        mail.send()
        
        response = render(request, 'somando/submitted.html', {
            'auth': auth_code,
            'id': room_id,
            'email': email,
        })
        response.set_cookie('contact_room_id', room_id)
        response.set_cookie('contact_room_auth', auth_code)
        
        return response

def contactLogin(request):
    
    if request.method == "GET":
        
        if 'id' in request.GET:
            room_id = request.GET['id']
        else:
            room_id = ''
        
        return render(request, 'somando/contact-login.html', {
            'id': room_id,
            'error': False,
        })
    
    elif request.method == "POST":
        
        room_id = request.POST['room_id']
        auth_code = request.POST['auth_code']
        
        if ContactRoomData.objects.filter(room_id=room_id, auth_code=auth_code).exists():
            
            url = reverse('somando:contactChat', kwargs={'id': room_id})
            response = redirect(url + '?key=' + auth_code)
            response.set_cookie('contact_room_id', room_id)
            response.set_cookie('contact_room_auth', auth_code)
            
            return response
        
        else:
            
            return render(request, 'somando/contact-login.html', {
                'id': room_id,
                'error': True,
            }, status=401)

def contactChat(request, id):
    
    if not ContactRoomData.objects.filter(room_id=id).exists():
        
        return render(request, '404.html', status=404)
    
    room = ContactRoomData.objects.get(room_id=id)
    
    room_auth_code = room.auth_code
    
    if request.method == "GET":
        
        if 'key' in request.GET:
            
            auth_code = request.GET['key']
            
            if room.auth_code == auth_code:
                
                messages = ContactMessageData.objects.filter(room_id=id).order_by('created_at')
                
                for message in messages:
                    message.message = message.message.replace('\n', "</span><br><span>")
                
                organization = messages[0].organization
                
                response = render(request, 'somando/contact-chat.html', {
                    'name': messages[0].user,
                    'organization': organization,
                    'id': room.room_id,
                    'email': room.email,
                    'close': room.close,
                    'room': room,
                    'messages': messages,
                })
                
                response.set_cookie('contact_room_id', id)
                response.set_cookie('contact_room_auth', auth_code)
                
                return response
        
        else:
            
            url = reverse('somando:contactLogin')
            response = redirect(url + '?id=' + id, status=400)
            
            return response
    
    elif request.method == "POST":
        
        if request.POST['method'] == 'send_message':
            
            message = request.POST['message']
            
            past_messages = ContactMessageData.objects.filter(room_id=id).order_by('created_at').first()
            
            room = ContactRoomData.objects.get(room_id=id)
            
            room_auth_code = room.auth_code
            
            if request.user.is_authenticated:
                
                subject = '担当者からの返信がありました｜Soma Ando'
                
                email = room.email
                
                context = {
                    'name': past_messages.user, 
                    'message': message, 
                    'id': room.room_id, 
                    'key': room_auth_code,
                }
                txt_content = get_template('mail/contact_message.txt').render(context)
                mail = EmailMultiAlternatives(subject=subject, body=txt_content, from_email='no-reply@somando.jp', to=[email], bcc=['info@somando.jp'])
                mail.send()
                
                ContactMessageData.objects.create(
                    room_id = id,
                    user = '安戸 蒼真',
                    organization = '',
                    admin = True,
                    message = message,
                )
            
            else:
                
                subject = '質問者からの返信がありました｜Soma Ando'
                
                email = room.email
                
                context = {
                    'name': past_messages.user, 
                    'message': message, 
                    'id': room.room_id, 
                    'key': room.auth_code,
                }
                txt_content = get_template('mail/contact_message_admin.txt').render(context)
                mail = EmailMultiAlternatives(subject=subject, body=txt_content, from_email='no-reply@somando.jp', to=['info@somando.jp'])
                mail.send()
                
                ContactMessageData.objects.create(
                    room_id = id,
                    user = past_messages.user,
                    organization = past_messages.organization,
                    admin = False,
                    message = message,
                )
        
        elif request.POST['method'] == 'close_room':
            
            room = ContactRoomData.objects.get(room_id=id)
            
            room.close = not room.close
            
            room.save()

        url = reverse('somando:contactChat', kwargs={'id': id})
        return redirect(url + '?key=' + room_auth_code)

def termsOfUse(request):
    
    return render(request, 'somando/terms-of-use.html')

def privacyPolicy(request):
    
    return render(request, 'somando/privacy-policy.html')


def productRedirect(request, url):
    
    return redirect('somando:product', url=url, permanent=True)
