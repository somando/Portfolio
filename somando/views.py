from django.shortcuts import render
from .models import *

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
    
    skills = SkillData.objects.all().order_by('date')
    
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
        product.title = product.title.replace('\span', "</span><span>")
        product.event = product.event.replace('\span', "</span><span>")
        product.team = product.team.replace('\span', "</span><span>")
        product.prize = product.prize.replace('\span', "</span><span>")
        product.link_title = product.link_title.replace('\span', "</span><span>")
        product.detail = product.detail.replace('\n', "</span><br><span>").replace('\span', "</span><span>")
    
    return render(request, 'somando/products.html', {
        'products': products,
    })
