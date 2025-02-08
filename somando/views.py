from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.db.models import Case, When, Value, IntegerField, Prefetch
from django.core.mail import EmailMultiAlternatives
from .models import *
import random, string

# Create your views here.

def splitSlash(items_text):
    
    if items_text != '':
        items_list = items_text.split('\n')
        items = []
        for item in items_list:
            item = item.split(' \ ')
            items.append(item)
        return items
    else:
        return ''


def top(request):
    
    static_profile = StaticProfileData.objects.first()
    static_profile.description = static_profile.description.replace('\span', "</span><span>")
    
    profiles = ProfileData.objects.filter(draft=False)
    for profile in profiles:
        profile.detail = profile.detail.replace('\span', "</span><span>")
    
    experiences = ExperienceData.objects.all().order_by('date').filter(show_top=True).filter(draft=False)
    for experience in experiences:
        date_list = str(experience.date).split('-')
        experience.date = date_list[0] + '/' + date_list[1]
        experience.title = experience.title.replace('\span', "</span><span>")
    
    products = ProductsData.objects.all().order_by('-date').filter(show_top=True).filter(draft=False)
    for product in products:
        date_list = str(product.date).split('-')
        product.date = date_list[0] + '/' + date_list[1]
        product.github = splitSlash(product.github)
        product.title = product.title.replace('\span', "</span><span>")
        product.event = product.event.replace('\span', "</span><span>")
        product.team = product.team.replace('\span', "</span><span>")
        product.prize = product.prize.replace('\span', "</span><span>")
        product.link = product.link.replace('\span', "</span><span>")
        product.link = splitSlash(product.link)
    
    skills = SkillData.objects.filter(show_top=True).annotate(
        null_category=Case(
            When(category__isnull=True, then=Value(1)),  # category が NULL の場合は 1
            default=Value(0),                            # それ以外は 0
            output_field=IntegerField()
        )
    ).order_by('null_category', 'category__position', 'position')
    
    return render(request, 'somando/top.html', {
        'static_profile': static_profile,
        'profiles': profiles,
        'experiences': experiences,
        'products': products,
        'skills': skills,
    })


def experiences(request):
    
    experiences = ExperienceData.objects.all().order_by('date').filter(draft=False)
    for experience in experiences:
        date_list = str(experience.date).split('-')
        experience.date = date_list[0] + '/' + date_list[1]
        experience.title = experience.title.replace('\span', "</span><span>")
        experience.detail = experience.detail.replace('\n', "</span><br><span>").replace('\span', "</span><span>")
        experience.link = splitSlash(experience.link)
    
    return render(request, 'somando/experiences.html', {
        'experiences': experiences,
    })


def products(request):
    
    products = ProductsData.objects.all().order_by('-date').filter(draft=False)
    for product in products:
        date_list = str(product.date).split('-')
        product.github = splitSlash(product.github)
        product.date = date_list[0] + '/' + date_list[1]
        product.title = product.title.replace('\span', "</span><span>")
        product.event = product.event.replace('\span', "</span><span>")
        product.team = product.team.replace('\span', "</span><span>")
        product.prize = product.prize.replace('\span', "</span><span>")
        product.link = product.link.replace('\span', "</span><span>")
        product.link = splitSlash(product.link)
        product.about = product.about.replace('\n', "</span><br><span>").replace('\span', "</span><span>")
    
    return render(request, 'somando/products.html', {
        'products': products,
    })


def product(request, url):
    
    product = ProductsData.objects.get(url=url)
    
    date_list = str(product.date).split('-')
    product.date = date_list[0] + '/' + date_list[1]
    product.github = splitSlash(product.github)
    product.technology = splitSlash(product.technology)
    product.infrastracture = splitSlash(product.infrastracture)
    product.collaborators = splitSlash(product.collaborators)
    product.title = product.title.replace('\span', "</span><span>")
    product.event = product.event.replace('\span', "</span><span>")
    product.team = product.team.replace('\span', "</span><span>")
    product.prize = product.prize.replace('\span', "</span><span>")
    product.link = product.link.replace('\span', "</span><span>")
    product.link = splitSlash(product.link)
    description = product.about.replace('/n', '').replace('\span', "")
    product.about = product.about.replace('\n', "</span><br><span>").replace('\span', "</span><span>")
    product.detail = product.detail.replace('\n', "</span></span><br><span class='br'><span>").replace('\span', "</span><span>")
    
    return product, description


def productPublic(request, url):
    
    print("C")
    
    if (not ProductsData.objects.filter(url=url).filter(draft=False).exists()):
        return render(request, '404.html', status=404)
    
    product_data, description = product(request, url)
    
    return render(request, 'somando/product.html', {
        'product': product_data,
        'description': description,
        'preview': False
    })


def productDraft(request, url):
    
    product_data = ProductsData.objects.filter(url=url)
    
    if not product_data.exists():
        print("A")
        return render(request, '404.html', status=404)
    
    if not product_data.first().draft:
        print("B")
        return redirect('somando:product', url=url, permanent=False)
    
    if request.user.is_authenticated:
        
        product_data_format, description = product(request, url)
        
        return render(request, 'somando/product.html', {
            'product': product_data_format,
            'description': description,
            'preview': True
        })
    
    else:
        
        return render(request, '401.html', status=401)


def skills(request):
    
    categories = SkillCategoryData.objects.prefetch_related(
        Prefetch('skills', queryset=SkillData.objects.all().order_by('position'))
    ).order_by('position')
    
    uncategorized_skills = SkillData.objects.filter(category__isnull=True).order_by('position')
    
    return render(request, 'somando/skills.html', {
        'categories': categories,
        'uncategorized_skills': uncategorized_skills,
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
