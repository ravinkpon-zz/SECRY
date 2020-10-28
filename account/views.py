from django.http import Http404, HttpResponse, JsonResponse, request
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.views.static import serve
from django.contrib import messages
from django.core.files import File
from django.core.mail import EmailMessage, EmailMultiAlternatives
from secry.settings import BASE_DIR
from shutil import copyfile
from account.models import *
from .functions import *
from .keys import *
from uuid import uuid4
from django.urls import reverse_lazy
import os
import random
import sys
import shutil
import logging
import socket
import smtplib
import hashlib
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

file_name = ""
User = get_user_model()
uid = " "
storedb = ['default', 'storage1', 'storage2']

if sys.platform == 'win32':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def my_random_string(string_length):  # Random string generation for making id
    random = str(uuid4())
    random = random.upper()
    random = random.replace("-", "")
    return random[0:string_length]


@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='signin')
def upload(request):  # Upload page request function
    if request.user.is_authenticated and request.user.is_active:
        user = User.objects.get(username=request.user.username)
        current_user = request.user
        uid = current_user.user_id
        return render(request, 'upload.html', {"user": user})
    else:
        return redirect('signin')

# Download page request function
@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='signin')
def download(request):
    if request.user.is_authenticated and request.user.is_active:
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


# Upload_file function - process the uploading of file
@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='signin')
def upload_file(request):
    global storedb
    global uid
    global file_name
    if request.method == 'POST' and request.FILES['myfile']:
        index = 0
        myfile = request.FILES['myfile']
        file_name = myfile.name
        size = myfile.size
        if file_info.objects.filter(file_name=file_name, user=request.user).exists():
            messages.warning(request, 'File with same name already exists.')
            return redirect(reverse_lazy('upload'))
        else:
            dest = os.path.join(MEDIA_ROOT, 'temp/')

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
            listDir = sorted(os.listdir(dest))
            info = file_info.objects.create(
                file_id=fileid, file_name=file_name, user=request.user, file_size=filesize,file_key=data)
            for file in listDir:
                id = hashlib.sha256(fileid.encode('utf-8')).hexdigest()
                file_path = os.path.join(dest, file)
                file_path = shutil.move(file_path, MEDIA_ROOT)
                if(alnum[index] == 1):
                    iv = iv2
                else:
                    iv = iv1
                encypt(alnum[index], key, file_path, iv)
                with open(file_path, 'a') as f:
                    header = '\n' + (str)(alnum[index])
                    f.write(header)
                    f.close()
                with open(file_path, 'rb') as file:
                    binaryData = file.read()
                    file.close()
                data = file_storage(store_id=id[:8], content=binaryData)
                data.save(using=storedb[index])
                os.remove(file_path)
                index = index+1
            emailid = request.user.email
            name = request.user.first_name
            attach = MEDIA_ROOT + '/keys/' + fileid + '.png'
            mail_subject = 'File Upload'
            html_message = render_to_string('key_email.html', {'name': name,'fileid':fileid,'create':1})
            msg = EmailMultiAlternatives(mail_subject, html_message, 'admin@secrycloud.tech', [emailid], reply_to=['admin@secrycloud.tech'], headers={'Message-ID': 'Upload'})
            msg.attach_alternative(html_message, "text/html")
            msg.attach_file(attach)
            msg.send(fail_silently=False)
            os.remove(attach)
            info.save()
            messages.success(request, "File uploaded successfully.")
            return redirect('upload')

# Download_file function to process downloading of the file
@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='signin')
def download_file(request):
    global file_name
    global storedb
    dest = os.path.join(MEDIA_ROOT, 'temp/')
    keyfile = request.FILES.get('keyfile')
    fileid = request.POST.get('fileid')
    file_name = request.POST.get('filename')
    print(file_name)
    data, key, iv1, iv2 = FetchKey(keyfile)
    try:
        info = file_info.objects.get(file_id=fileid, file_key=data)
    except ObjectDoesNotExist:
        info = None
    if info is not None:
        index = 0
        while(index < 3):
            id = hashlib.sha256(fileid.encode('utf-8')).hexdigest()
            try:
                data = file_storage.objects.using(
                storedb[index]).get(store_id=id[:8])
            except:
                response = JsonResponse({"error": "Sorry! File not found"})
                response.status_code = 403
                return response
            fname = file_name.split('.')
            file_path = dest + fname[0] + '_' + \
                str(index+1) + '.' + fname[1]
            with open(file_path, 'wb') as file:
                file.write(data.content)
                file.close()
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
                    file.truncate()
                file.close()
            if(alnum == 1):
                iv = iv2
            else:
                iv = iv1
            decrypt(alnum, key, file_path, iv)
            index = index+1
        todir = os.path.join(MEDIA_ROOT, file_name)
        join(dest, todir)
        if os.path.exists(todir):
            with open(todir, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="text/plain")
                response['Content-Disposition'] = 'attachment; filename=' + file_name
            os.remove(todir)
            return response
        raise Http404
    else:
        response = JsonResponse({"error": " Incorrect key uploaded "})
        response.status_code = 403 
        return response
    

@login_required(login_url='signin')
@cache_control(no_cache=True, must_revalidate=True)
def view(request):                                                  #View uploaded files page request function
    if request.user.is_authenticated and request.user.is_active:
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


@login_required(login_url='signin')
@cache_control(no_cache=True, must_revalidate=True)
def dash(request):                                              #Dahboard page of user account request
    if request.user.is_authenticated and request.user.is_active:
        user = User.objects.get(username=request.user.username)
        current_user = request.user
        uid = current_user.user_id
        file = file_info.objects.filter(user_id=uid).count()
        return render(request, 'profile.html', {"user": user, 'count':file})
    else:
        return redirect('signin')


@login_required(login_url='signin')
@cache_control(no_cache=True, must_revalidate=True)
def account(request):                                               #Account pages request for user details
    if request.user.is_authenticated and request.user.is_active:
        user = User.objects.get(username=request.user.username)
        return render(request, 'account.html', {"user": user})
    else:
        return redirect('signin')


@login_required(login_url='signin')
@cache_control(no_cache=True, must_revalidate=True)
def settings(request):                                              #Account settings page request
    global uid
    if request.user.is_authenticated and request.user.is_active:
        user = User.objects.get(username=request.user.username)
        current_user = request.user
        uid = current_user.user_id
        return render(request, 'settings.html', {'user': user})
    else:
        return redirect('signin')


@login_required(login_url='signin')
@cache_control(no_cache=True, must_revalidate=True)
def changepass(request):                                           #User account password change
    if(request.method == "POST"):
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        emailid = request.POST['email']
        user = User.objects.get(email=emailid)
        user.set_password(password1)
        user.save()
        messages.success(request, "Your passsword has been changed.")
        return redirect('settings')


@login_required(login_url='signin')
@cache_control(no_cache=True, must_revalidate=True)
def edituser(request):                                          #User info change process request
    if(request.method == "POST"):
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        location = request.POST['location']
        phone = request.POST['phone']
        user = User.objects.get(username=request.user.username)
        current_user = request.user
        uid = current_user.user_id
        user = User.objects.get(user_id=uid)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.location = location
        user.phone = phone
        user.save()
        user = User.objects.get(username=request.user.username)
        messages.success(request, "Your changes are saved.")
        return render(request, 'settings.html', {"user": user})


@login_required(login_url='signin')
@cache_control(no_cache=True, must_revalidate=True)
def delete_file(request):                               #Delete_file from server request
    global file_name
    global storedb
    if request.method == 'POST' and request.FILES['keyfile']:
        keyfile = request.FILES['keyfile']
        fileid = request.POST['fileid']
        file_name = request.POST['filename']
        data = FetchKeyData(keyfile)
        try:
            info = file_info.objects.get(file_id=fileid, file_key=data)
        except ObjectDoesNotExist:
            info = None
        if info is None:
            messages.info(request, "Incorrect key uploaded.")
            return redirect('view')
        index=0
        while(index < 3):
            id = hashlib.sha256(fileid.encode('utf-8')).hexdigest()
            try :
                data = file_storage.objects.using(storedb[index]).get(store_id=id[:8])
                data.delete()
            except:
                pass
            index = index+1 
        files = file_info.objects.get(file_id=fileid)
        files.delete()
        messages.success(request, "File deleted sucessfully.")
        return redirect('view')


@login_required(login_url='signin')
@cache_control(no_cache=True, must_revalidate=True)
def generate(request):                      #Generate the key file for the user.
    if(request.method=='POST'):
        id = request.POST['fileid']
        try:
            info = file_info.objects.get(file_id=id)
        except ObjectDoesNotExist:
            info = None
        if info is not None:
            fkey = info.file_key
            keygenerate(fkey,id)
            mail = request.user.email
            name = request.user.first_name
            attach = MEDIA_ROOT + '/keys/' + id + '.png'
            mail_subject = 'Regenerate Key'
            html_message = render_to_string(
                'key_email.html', {'name': name, 'fileid': id, 'create': 0})
            msg = EmailMultiAlternatives(mail_subject, html_message, 'admin@secrycloud.tech', [mail], reply_to=['admin@secrycloud.tech'], headers={'Message-ID': 'Upload'})
            msg.attach_alternative(html_message, "text/html")
            msg.attach_file(attach)
            msg.send(fail_silently=False)
            os.remove(attach)
            messages.success(request, "Key send to the email")
            return redirect('view')


@login_required(login_url='signin')
@cache_control(no_cache=True, must_revalidate=True)
def delete_account(request):                #Delete a user account and files request.
    user = User.objects.get(username=request.user.username)
    current_user = request.user.user_id
    files = file_info.objects.filter(user_id=current_user)
    for file in files:
        index=0
        fileid = file.file_id
        while(index < 3):
            id = hashlib.sha256(fileid.encode('utf-8')).hexdigest()
            try:
                data = file_storage.objects.using(storedb[index]).get(store_id=id[:8])
                data.delete()
            except:
                pass 
            index = index+1 
    user.delete()
    return redirect('view')
