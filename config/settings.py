import os
from pathlib import Path
import dj_database_url

BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY=os.getenv('DJANGO_SECRET_KEY','change-this-key-before-deployment')

DEBUG=os.getenv('DJANGO_DEBUG','True').lower()=='true'

ALLOWED_HOSTS=[] #os.getenv('DJANGO_ALLOWED_HOSTS','127.0.0.1,localhost').split(',')

INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','patrimoine']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF='config.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'patrimoine/templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION='config.wsgi.application'

#if os.getenv('DB_NAME'):
# DATABASES={'default':{'ENGINE':'django.db.backends.postgresql','NAME':os.getenv('DB_NAME'),'USER':os.getenv('DB_USER'),'PASSWORD':os.getenv('DB_PASSWORD'),'HOST':os.getenv('DB_HOST','127.0.0.1'),'PORT':os.getenv('DB_PORT','5432')}}
#else: DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}

AUTH_PASSWORD_VALIDATORS=[{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'}]
LANGUAGE_CODE='fr-fr'; TIME_ZONE='Africa/Conakry'; USE_I18N=True; USE_TZ=True
STATIC_URL='static/'; MEDIA_URL='media/'; MEDIA_ROOT=BASE_DIR/'media'; DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_URL='login'; LOGIN_REDIRECT_URL='dashboard'; LOGOUT_REDIRECT_URL='login'


DATABASES = {
    'default': dj_database_url.config()
}
