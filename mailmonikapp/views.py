# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,Http404
import datetime
from django.core.mail import send_mail
from mailmonikapp.models import Subscription,Newsletter
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from mailmonik.settings_local import usermail,password

from django.shortcuts import render
import smtplib
import hashlib
import time

# Create your views here.

#dict = { "ghetiyaamit791@gmail.com","patelamit791@gmail.com","deepmehta899@gmail.com","ketavbhatt@gmail.com","menkudlekrutik@gmail.com","ikbalsinghdhanjal23@gmail.com","thecoders000@gmail.com","ronak01doshi@gmail.com"}

def values():
	global usermail
	usermail = usermail
	global password
	password = password



def subscribe(request):
	return render(request,"subscribe.html")


dictionary = {}


def subscription(request):
	if request.method == 'POST':
        
		subscribermail = request.POST.get('email')


        hash = hashlib.sha1()
        now = datetime.datetime.now()
        hash.update(str(now)+subscribermail+'kuttu_is_best')
        subkey = hash.hexdigest()

        hash = hashlib.sha1()
        now = datetime.datetime.now()
        hash.update(str(now)+subscribermail+'kuttu_is_worst')
        unsubkey = hash.hexdigest()

        fromaddr = usermail
        toaddr = subscribermail
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Confirmational Email"
 
        body = "Please Click On The Link To Subscribe: http://localhost:8000/subscription_complete/%s" %subkey 
        msg.attach(MIMEText(body, 'plain'))
 
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

        checkmail = []

        for u in Subscription.objects.all():
            checkmail.append(u.email)

        print checkmail
        if subscribermail in checkmail:
            user = Subscription.objects.get(email=subscribermail)
            user.is_active = 0
            user.subkey = subkey
            user.unsubkey = unsubkey
            user.save()
        
        else:
            user = Subscription.objects.create(email=subscribermail,subkey=subkey,unsubkey=unsubkey)

            

        html = "<html><body>Please Confirm Your Subscription By Going To The URL Send To Your Mail-ID</body></html>" 
        return HttpResponse(html)



def subscription_complete(request,p):
    subkeys = []
    for u in Subscription.objects.all():
        subkeys.append(u.subkey)
        print subkeys
        email = u.email
        print email
        unsubkeys = u.unsubkey
        print p
        
    if p in subkeys:
        try:
            print "HI"
            user = Subscription.objects.get(subkey=p)
            print user
            user.is_active = 1
            user.save()
        except:
            print "error"
            raise Http404
            
        fromaddr = usermail
        toaddr = user.email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Subscription Complete"

        body = "Welcome To Doodle! Hope You Have A Great Time" + "To Unsubscribe Visit: http://localhost:8000/%s/unsubscribe" %unsubkeys
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

        html = "<html><body>Thank You For Subscribing!</body></html>" 
        return HttpResponse(html)



def msg(request):
    if request.user.is_authenticated():
        return render(request,"msg.html")
    else:
        html = "<html><body>Please First Login In Admin Panel</body></html>" 
        return HttpResponse(html)




def mail(request):
	if request.method == 'POST':
		message = request.POST.get('msg')
        subject = request.POST.get('sub')

        user = Newsletter.objects.create(subject=subject,body=message)

        for u in Subscription.objects.filter(is_active=1):
            fromaddr = usermail
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['Subject'] = subject
 
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, password)
            toaddr = u.email
            msg['To'] = toaddr

            body = message + "To Unsubscribe Visit: http://localhost:8000/%s/unsubscribe" %u.unsubkey
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()

            server.sendmail(fromaddr, toaddr, text)
            server.quit()

        now = datetime.datetime.now()
        html = "<html><body>Mail send at %s.</body></html>" % now
        return HttpResponse(html)


def unsubscribe(request,p):
		if Subscription.objects.filter(unsubkey=p):
            		instancetemp = Subscription.objects.filter(unsubkey=p)
			return render(request,'unsubscribed.html',{ 'instance' : instancetemp })
    
		else:
			html = "<html><body>Invalid Account</body></html>"
			return HttpResponse(html)



def unsubscribed(request,p):
    if Subscription.objects.get(unsubkey=p):
        u = Subscription.objects.get(unsubkey=p)
        print u
	if u.is_active == 1:
		u.is_active = 2
		u.save()

		html = "<html><body>Sucessfully Unsubscribed</body></html>"
		return HttpResponse(html)
        
	else:
	    	html = "<html><body>Invalid Account</body></html>"
	    	return HttpResponse(html)
