from django.shortcuts import render

# Create your views here.
from .models import Program, News, Staff

def home(request):
    news = News.objects.all().order_by('-date_posted')[:3]
    return render(request, 'school/home.html', {'news': news})

def about(request):
    staff = Staff.objects.all()
    return render(request, 'school/about.html', {'staff': staff})

def programs(request):
    program_list = Program.objects.all()
    return render(request, 'school/programs.html', {'programs': program_list})

def news(request):
    news_list = News.objects.all().order_by('-date_posted')
    return render(request, 'school/news.html', {'news': news_list})

def student_life(request):
    news_list = News.objects.all().order_by('-date_posted')
    return render(request, 'school/student_life.html', {'student_life': news_list})


def contact(request):
    news_list = News.objects.all().order_by('-date_posted')
    return render(request, 'school/contact.html', {'contact': news_list})


import os
from django.conf import settings
from django.shortcuts import render

def gallery(request):
    # Define category folders to scan
    gallery_categories = {
        "Sports Activities": {
            "icon": "🏆",
            "folder": "static/GALLERY/sports"
        },
        "Quiz Competitions": {
            "icon": "📖",
            "folder": "static/GALLERY/quiz"
        }
        # Add more categories as needed
    }
    
    gallery_data = {}
    
    # Scan each category folder and get image paths
    for category, info in gallery_categories.items():
        folder_path = os.path.join(settings.MEDIA_ROOT, info["folder"])
        images = []
        
        if os.path.exists(folder_path):
            # Get image files from the folder
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            for file in os.listdir(folder_path):
                if any(file.lower().endswith(ext) for ext in valid_extensions):
                    # Get full path for the template
                    image_url = f"{settings.MEDIA_URL}{info['folder']}/{file}"
                    # Generate a caption from the filename (remove extension and replace underscores)
                    caption = os.path.splitext(file)[0].replace('_', ' ').title()
                    images.append({
                        'url': image_url,
                        'caption': caption,
                        'alt': caption
                    })
        
        # Add category with images to gallery data
        gallery_data[category] = {
            "icon": info["icon"],
            "images": images
        }
    
    return render(request, 'school/gallery.html', {'gallery_data': gallery_data})