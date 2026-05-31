import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
import sys
sys.path.insert(0, os.path.dirname(__file__))
django.setup()
from blog.models import Post
print('Total posts:', Post.objects.count())
print('Empty slug:', Post.objects.filter(slug='').count())
