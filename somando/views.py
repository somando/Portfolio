from django.shortcuts import render
from django.core.mail import send_mail
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
        return render(request, '404.html')
    
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
    product.about = product.about.replace('\n', "</span><br><span>").replace('\span', "</span><span>")
    product.detail = product.detail.replace('\n', "</span></span><br><span class='br'><span>").replace('\span', "</span><span>")
    
    return render(request, 'somando/product.html', {
        'product': product,
    })

def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def contact(request):
    
    if request.method == "GET":
        
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
        
        return render(request, 'somando/contact.html', {
            'open': False,
        })
    
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
        )
        
        ContactMessageData.objects.create(
            room_id = room_id,
            user = name,
            organization = organization,
            admin = False,
            message = details,
        )
        
        subject = 'お問い合わせを受け付けました｜Soma Ando'
        
        message = name + email + organization + details
        
        send_mail(subject, message, 'no-reply@somando.jp', [email])
        send_mail(subject, message, 'no-reply@somando.jp', ['info@somando.jp'])
        
        response = render(request, 'somando/submitted.html', {
            'auth': auth_code,
            'id': room_id,
        })
        response.set_cookie('contact_room_id', room_id)
        response.set_cookie('contact_room_auth', auth_code)
        
        return response

def contactChat(request, id):
    return render(request, 'somando/contact-chat.html', {
        'id': id,
    })

def termsOfUse(request):
    
    return render(request, 'somando/terms-of-use.html')

def privacyPolicy(request):
    
    return render(request, 'somando/privacy-policy.html')
