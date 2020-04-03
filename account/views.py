from django.views.decorators.cache import cache_control
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.views.static import serve
from django.contrib import messages
from django.http import Http404, request,HttpResponse
from shutil import copyfile
from account.models import *
from .functions import *
from .keys import *
from uuid import uuid4
import os
import random
import sys
import shutil
import dns.resolver
import dns.exception
import logging
import socket
import smtplib,hashlib
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.core.mail import EmailMessage
from secry.settings import BASE_DIR



logger = logging.getLogger(__name__)

file_name = ""
User = get_user_model()
uid = " "
storedb = ['default', 'storage1', 'storage2']


def check_email_exists(email):

    domain = email.split('@')[1]
    try:
        records = dns.resolver.query(domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
        # Get local server hostname
        host = socket.gethostname()

        # SMTP lib setup (use debug level for full output)
        server = smtplib.SMTP()
        server.set_debuglevel(0)

        # SMTP Conversation
        server.connect(mxRecord)
        server.helo(host)
        server.mail('alinbabu2010@gmail.com')
        code, message = server.rcpt(str(email))
        server.quit()
        # Assume 250 as Success
        if code == 250:
            return True
        else:
            return False
    except:
        pass


if sys.platform == 'win32':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def my_random_string(string_length):
    random = str(uuid4()) 
    random = random.upper() 
    random = random.replace("-", "") 
    return random[0:string_length] 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upload(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        current_user = request.user
        uid = current_user.user_id
        return render(request, 'upload.html', {"user": user})
    else:
        return redirect('signin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def download(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        current_user = request.user
        uid = current_user.user_id
        try:
            files = file_info.objects.filter(user=uid)
        except file_info.DoesNotExist:
            files = None
        return render(request, 'download.html', {'files': files})
    else:
        return redirect('signin')

def upload_file(request):
    global storedb
    global uid
    global file_name
    if request.method == 'POST' and request.FILES['myfile']:
        index = 0
        myfile = request.FILES['myfile']
        file_name = myfile.name
        if file_info.objects.filter(file_name=file_name, user=request.user).exists():
            messages.warning(request, 'File with same name already exists.')
            return redirect('view')
        else:
            dest = os.path.join(MEDIA_ROOT,'temp/')
            size = myfile.size
            try:
                Dir = os.listdir(dest)
                for file in Dir:
                    os.remove(dest+'/'+file)
            except:
                pass
            filesize = size/(1024*1024)
            filesize = "{:.2f}".format(filesize)
            fileid = my_random_string(8)
            split(myfile)
            key, iv1, iv2, data = generateKey(fileid)
            alnum = enc_order()
            print(alnum)
            listDir = os.listdir(dest)
            info = file_info.objects.create(file_id=fileid, file_name=file_name, user=request.user, file_size=filesize, file_key=key, file_keydata=data)
            for file in listDir:
                print(file)
                id = hashlib.sha256(fileid.encode('utf-8')).hexdigest()
                file_path = os.path.join(dest,file)
                file_path = shutil.move(file_path,'./media')
                if(alnum[index] == 1):
                    iv = iv2
                else:
                    iv = iv1
                encypt(alnum[index], key, file_path, iv)
                with open(file_path, 'a') as f:
                    header = '\n' + (str)(alnum[index])
                    print(header)
                    f.write(header)
                    f.close()
                with open(file_path, 'rb') as file:
                    binaryData = file.read()
                data = file_storage.objects.using(storedb[index]).create(store_id=id,content=binaryData)
                data.save(using=storedb[index])
                os.remove(file_path)
                index = index+1
            mail = request.user.email
            name = request.user.first_name
            attach = MEDIA_ROOT + '/keys/' + fileid + '.png'
            email = EmailMessage(
                'Key of '+fileid,
                'Hi '+name+',\n   Please see the attachment below.Use this for accessing the file.Please keep it safe.\n\n\nRegards,\nSecry Team',
                'alinbabu2010@secry.in',
                [mail],
                headers={'Message-ID': 'foo'},
            )
            email.attach_file(attach)
            email.send(fail_silently=False)
            os.remove(attach)
            info.save()
            messages.info(request,"File uploaded successfull.")
            return redirect('view')

def download_file(request):
    global file_name
    global storedb
    if request.method == 'POST' and request.FILES['keyfile']:
        dest = os.path.join(MEDIA_ROOT,'temp/')
        keyfile = request.FILES['keyfile']
        fileid = request.POST['fileid']
        file_name = request.POST['filename']
        key,iv1,iv2 = FetchKey(keyfile)
        try:
            info = file_info.objects.get(file_id=fileid,file_key=key)
        except ObjectDoesNotExist:
            info = None
        if info is not None:
            index = 0
            while(index<3):
                id = hashlib.sha256(fileid.encode('utf-8')).hexdigest()
                try:
                    data = file_storage.objects.using(storedb[index]).get(store_id=id)
                except:
                    pass
                fname = file_name.split('.')
                file_path = dest +fname[0] + '_' + str(index+1) + '.' + fname[1]
                print(file_path)
                with open(file_path,'wb') as file:
                    file.write(data.content)
                    file.close
                with open(file_path, "rb+") as file:
                    file.seek(0, os.SEEK_END)
                    pos = file.tell() - 1
                    while pos > 0 and file.read(1) != b"\n":
                        pos -= 1
                        file.seek(pos, os.SEEK_SET)
                    if pos > 0:
                        file.seek(pos, os.SEEK_SET)
                        alnum = int(file.read().decode())
                        file.seek(pos-1, os.SEEK_SET)
                        file.truncate()
                print(alnum)
                if(alnum == 1):
                    iv = iv2
                else:
                    iv = iv1
                decrypt(alnum, key, file_path, iv)
                index = index+1
            todir = os.path.join(MEDIA_ROOT,file_name)
            join(dest, todir)
            if os.path.exists(todir):
                with open(todir, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="text/plain")
                    response['Content-Disposition'] = 'attachment; filename=' + file_name
                os.remove(todir)
                return response
            raise Http404
        else:
            messages.info(request, "Incorrect key uploaded.")
            return redirect('download')

def view(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        current_user = request.user
        uid = current_user.user_id
        try:
            files = file_info.objects.filter(user=uid)
        except file_info.DoesNotExist:
            files = None
        return render(request, 'view.html', {'files': files})
    else:
        return redirect('signin')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dash(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        current_user = request.user
        uid = current_user.user_id
        file = file_info.objects.filter(user_id=uid).count()
        print(user)
        return render(request, 'profile.html', {"user": user, 'count':file})
    else:
        return redirect('signin')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def account(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        return render(request, 'account.html', {"user": user})
    else:
        return redirect('signin')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def settings(request):
    global uid
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        current_user = request.user
        uid = current_user.user_id
        print(uid)
        return render(request, 'settings.html', {'user': user})
    else:
        return redirect('signin')


def changepass(request):
    if(request.method == "POST"):
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        emailid = request.POST['email']
        user = User.objects.get(email=emailid)
        user.set_password(password1)
        user.save()
        messages.info(request, "Your passsword has been changed.")
        return redirect('settings')


def edituser(request):
    if(request.method == "POST"):
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        location = request.POST['location']
        phone = request.POST['phone']
        try:
            validate_email(email)
            email_exists = check_email_exists(email)
            valid_email = True
        except:
            valid_email = False
        print(valid_email)
        if valid_email == False or email_exists == False :
            messages.info(request, "Email does not exists.")
            user = User.objects.get(username=request.user.username)
            return render(request, 'settings.html', {"user": user})
        else:
            user = User.objects.get(username=request.user.username)
            current_user = request.user
            uid = current_user.user_id
            user = User.objects.get(user_id=uid)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.location = location
            user.phone = phone
            user.save()
            user = User.objects.get(username=request.user.username)
            messages.info(request, "Your changes are saved.")
            return render(request, 'settings.html', {"user": user})

def delete_file(request):
    global file_name
    global storedb
    if request.method == 'POST' and request.FILES['keyfile']:
        keyfile = request.FILES['keyfile']
        fileid = request.POST['fileid']
        file_name = request.POST['filename']
        print(file_name, fileid)
        key,iv1,iv2 = FetchKey(keyfile)
        try:
            info = file_info.objects.get(file_id=fileid, file_key=key)
        except ObjectDoesNotExist:
            info = None
        if info is None:
            messages.info(request, "Incorrect key uploaded.")
            return redirect('view')
        index=0
        while(index < 3):
            id = hashlib.sha256(fileid.encode('utf-8')).hexdigest()
            try :
                data = file_storage.objects.using(storedb[index]).get(store_id=id)
                data.delete()
            except:
                pass
            index = index+1 
        files = file_info.objects.get(file_id=fileid)
        files.delete()
        messages.info(request, "File deleted sucessfully.")
        return redirect('view')

def generate(request):
    if(request.method=='POST'):
        id = request.POST['fileid']
        try:
            info = file_info.objects.get(file_id=id)
        except ObjectDoesNotExist:
            info = None
        if info is not None:
            fkey = info.file_keydata
            keygenerate(fkey,id)
            mail = request.user.email
            name = request.user.first_name
            attach = './media/keys/' + id + '.png'
            email = EmailMessage(
                'Key of '+id,
                'Hi '+name+',\n   Please see the attachment below.Use this for accessing the file.Please keep it safe.\n\n\nRegards,\nSecry Team',
                'alinbabu2010@secry.in',
                [mail],
                headers={'Message-ID': 'foo'},
            )
            email.attach_file(attach)
            email.send(fail_silently=False)
            os.remove(attach)
            messages.info(request, "Key send to the email")
            return redirect('view')

def delete_account(request):
    user = User.objects.get(username=request.user.username)
    current_user = request.user.user_id
    files = file_info.objects.filter(user_id=current_user)
    for file in files:
        index=0
        fileid = file.file_id
        while(index < 3):
            id = hashlib.sha256(fileid.encode('utf-8')).hexdigest()
            try:
                data = file_storage.objects.using(storedb[index]).get(store_id=id)
                data.delete()
            except:
                pass 
            index = index+1 
    user.delete()
    return redirect('view')
