from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.core.validators import validate_email
import dns.resolver
import dns.exception
import logging
from django.http import request
import socket
import smtplib
from django.contrib.auth import logout,login
from django.http.response import HttpResponseRedirect
from account.views import my_random_string
from django.template.loader import get_template
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)

User = get_user_model()


def home(request):
    return render(request, 'index.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('dash')
        else:
            messages.info(request, 'Invalid crenditals')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

def signout(request):
    if request.method == "POST":
        request.user.is_active = False
        logout(request)
        return HttpResponseRedirect("/")


def register(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        location = request.POST['location']
        phone = request.POST['phone']
        uid = my_random_string(10)
        try:
            validate_email(email)
            email_exists = check_email_exists(email)
            valid_email = True
        except:
            valid_email = False
        if((valid_email == False) or (email_exists == False)):
            messages.info(request, "Enter a valid email address.")
            return redirect('register')
        else:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists.')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists.")
                return redirect('register')
            else:
                user = User.objects.create_user(user_id=uid,username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password1, location=location, phone=phone)
                user.save()
                messages.info(request, "User creation successfull.")
                return redirect('signin')

    else:
        return render(request, 'signup.html')


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
        print(code)
        # Assume 250 as Success
        if code == 250:
            return True
        else:
            return False
    except:
        pass


def change(request):
    if(request.method == "POST"):
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        emailid = request.POST['email']
        if not User.objects.filter(email=emailid).exists():
            messages.info(request, "Email does not exists.")
            return render(request, 'signin.html')
        else:
            user = User.objects.get(email=emailid)
            user.set_password(password1)
            user.save()
            messages.info(request, "Your passsword has been changed.")
            return render(request, 'signin.html')


def contact(request):
    if request.method == 'POST':
        contact_name = request.POST['txtName']
        contact_email = request.POST['txtEmail']
        contact_phone = request.POST['txtPhone']
        form_content = request.POST['txtMsg']
        template = get_template('contact_template.txt')
        context = {'contact_name': contact_name,'contact_email': contact_email,'contact_phone':contact_phone,'form_content': form_content}
        content = template.render(context)
        email = EmailMessage("New contact form submission",content,contact_email,['admin@secrycloud.tech'],headers={'Reply-To': contact_email})
        email.send()
        return redirect('home')


def error_404(request,exception):
        data = {}
        return render(request, '404.html', data)


def error_500(request):
    return render(request, '500.html')

