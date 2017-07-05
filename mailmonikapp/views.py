# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from django.core.mail import send_mail
from django.http import HttpResponse,Http404,JsonResponse
from django.shortcuts import render

import smtplib
import hashlib
import time
import datetime

from mailmonik.settings_local import usermail, password, smtpserver, port
from mailmonikapp.models import Subscription, Newsletter,SubscriptionComplete_Email,Welcome_Email


# Create your views here.


def subscribe(request):
    return render(request, "subscribe.html")




def api_subscribe(request):
        try:
            subscribermail = request.GET.get('email')
            print subscribermail

            hash = hashlib.sha1()
            now = datetime.datetime.now()
            hash.update(str(now) + subscribermail + 'kuttu_is_best')
            subkey = hash.hexdigest()

            hash = hashlib.sha1()
            now = datetime.datetime.now()
            hash.update(str(now) + subscribermail + 'kuttu_is_worst')
            unsubkey = hash.hexdigest()


            fromaddr = usermail
            toaddr = subscribermail
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr

            subscriptiondetails = SubscriptionComplete_Email.objects.get(id=1)

            msg['Subject'] = subscriptiondetails.subssubject

            domain = request.get_host()
            scheme = request.is_secure() and "https" or "http"


            body = subscriptiondetails.subsbody
            part1 = MIMEText(body, 'plain')
            msg.attach(part1)


            html = subscriptiondetails.subshtml
            part2 = MIMEText(html,'html')
            msg.attach(part2)

            
            unsub_link = "{0}://{1}/subscription_complete/{2}".format(scheme,domain,subkey)
            part3 = MIMEText(u'<center>Please click <a href="'+unsub_link+'" style="font-size:16px;">here to complete your subscription</a> to our newsletter</center>','html')
            msg.attach(part3)
            

            link = "You may alternatively paste this link in your browser to compelete subscription: {0}://{1}/subscription_complete/{2}".format(scheme,domain,subkey)
            part4 = MIMEText(link,'plain')
            msg.attach(part4)


            server = smtplib.SMTP(smtpserver, port)
            server.starttls()
            server.login(fromaddr, password)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()

            checkmail = []

            for u in Subscription.objects.all():
                checkmail.append(u.email)

            if subscribermail in checkmail:
                user = Subscription.objects.get(email=subscribermail)
                user.is_active = 0
                user.subkey = subkey
                user.unsubkey = unsubkey
                user.save()

            else:
                user = Subscription.objects.create(email=subscribermail, subkey=subkey, unsubkey=unsubkey)

            return JsonResponse({'success':'True'})

        except:
            return JsonResponse({'success':'False'})





def subscription(request):
    if request.method == 'POST':

        subscribermail = request.POST.get('email')

        hash = hashlib.sha1()
        now = datetime.datetime.now()
        hash.update(str(now) + subscribermail + 'kuttu_is_best')
        subkey = hash.hexdigest()

        hash = hashlib.sha1()
        now = datetime.datetime.now()
        hash.update(str(now) + subscribermail + 'kuttu_is_worst')
        unsubkey = hash.hexdigest()

        fromaddr = usermail
        toaddr = subscribermail
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Confirmational Email"

        domain = request.get_host()
        scheme = request.is_secure() and "https" or "http"

        subscriptiondetails = SubscriptionComplete_Email.objects.get(id=1)

        msg['Subject'] = subscriptiondetails.subssubject

        domain = request.get_host()
        scheme = request.is_secure() and "https" or "http"


        body = subscriptiondetails.subsbody
        part1 = MIMEText(body, 'plain')
        msg.attach(part1)


        html = subscriptiondetails.subshtml
        part2 = MIMEText(html,'html')
        msg.attach(part2)

        
        unsub_link = "{0}://{1}/subscription_complete/{2}".format(scheme,domain,subkey)
        part3 = MIMEText(u'<center>Please click <a href="'+unsub_link+'" style="font-size:16px;">here to complete your subscription</a> to our newsletter</center>','html')
        msg.attach(part3)


        link = "You may alternatively paste this link in your browser to compelete subscription: {0}://{1}/subscription_complete/{2}".format(scheme,domain,subkey)
        part4 = MIMEText(link,'plain')
        msg.attach(part4)

        server = smtplib.SMTP(smtpserver, port)
        server.starttls()
        server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

        checkmail = []

        for u in Subscription.objects.all():
            checkmail.append(u.email)

        if subscribermail in checkmail:
            user = Subscription.objects.get(email=subscribermail)
            user.is_active = 0
            user.subkey = subkey
            user.unsubkey = unsubkey
            user.save()

        else:
            user = Subscription.objects.create(email=subscribermail, subkey=subkey, unsubkey=unsubkey)

        html = "<html><body>Please Confirm Your Subscription Confirming The Mail Send To Your Email-ID</body></html>"
        return HttpResponse(html)





def subscription_complete(request, p):
    subkeys = []
    for u in Subscription.objects.all():
        subkeys.append(u.subkey)
        print subkeys
        email = u.email

    if p in subkeys:
        try:
            user = Subscription.objects.get(subkey=p)
            unsubkeys = user.unsubkey
            user.is_active = 1
            user.save()

        except:
            raise Http404

        fromaddr = usermail
        toaddr = user.email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr


        welcomedetails = Welcome_Email.objects.get(id=1)

        msg['Subject'] = welcomedetails.welcomesubject

        domain = request.get_host()
        scheme = request.is_secure() and "https" or "http"

        body = welcomedetails.welcomebody
        part1 = MIMEText(body, 'plain')
        msg.attach(part1)


        html = welcomedetails.welcomehtml
        part2 = MIMEText(html,'html')
        msg.attach(part2)

        
        unsub_link = "{0}://{1}/{2}/unsubscribe".format(scheme,domain,unsubkeys)
        part3 = MIMEText(u'<a href="'+unsub_link+'" style="font-size:12px;"><center>Click Here To Unsubscribe</center></a>','html')
        msg.attach(part3)


        server = smtplib.SMTP(smtpserver, port)
        server.starttls()
        server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

        html = "<html><body>Thank You For Subscribing!</body></html>"
        return HttpResponse(html)






def msg(request):
    if request.user.is_authenticated():
        subjects = Newsletter.objects.filter(sent_at=None)
        return render(request, "msg.html", {'subject': subjects})
    else:
        html = "<html><body>Please First Login In Admin Panel</body></html>"
        return HttpResponse(html)






def mail(request):
    if request.method == 'POST':
        sub = request.POST.get('sub')
        print sub

        for u in Subscription.objects.filter(is_active=1):
            fromaddr = usermail
            msg = MIMEMultipart()
            msg['From'] = fromaddr

            server = smtplib.SMTP(smtpserver, port)
            server.starttls()
            server.login(fromaddr, password)
            toaddr = u.email
            msg['To'] = toaddr

            domain = request.get_host()
            scheme = request.is_secure() and "https" or "http"

            newsletter = Newsletter.objects.get(subject=sub)

            msg['Subject'] = newsletter.subject
            body = newsletter.body
            html = newsletter.html
            
            part2 = MIMEText(html, 'html')
            part1 = MIMEText(body, 'plain')
            
            
            unsub_link = "{0}://{1}/{2}/unsubscribe".format(scheme,domain,u.unsubkey)
            part3 = MIMEText(u'<a href="'+unsub_link+'" style="font-size:12px;"><center>Click Here To Unsubscribe</center></a>','html')
        
            msg.attach(part1)
            msg.attach(part2)
            msg.attach(part3)

            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            print '1'

        now = datetime.datetime.now()

        u = Newsletter.objects.get(subject=sub)
        u.sent_at = now
        u.save()

        html = "<html><body>Mail send at %s.</body></html>" % now
        return HttpResponse(html)


    



def unsubscribe(request, p):
    print p
    if Subscription.objects.get(unsubkey=p):
        instancetemp = Subscription.objects.filter(unsubkey=p)
        print instancetemp
        return render(request, 'unsubscribed.html', {'instance': instancetemp})


    else:
        html = "<html><body>Invalid Account</body></html>"
        return HttpResponse(html)




def unsubscribed(request, p):
    if Subscription.objects.get(unsubkey=p):
        u = Subscription.objects.get(unsubkey=p)
        print u

    if u.is_active == 1:
        u.is_active = 2
        u.save()
        html = "<html><body><h1>Sucessfully Unsubscribed</h1></body></html>"
        return HttpResponse(html)


        u.is_active = 2
        u.save()

        html = "<html><body>Sucessfully Unsubscribed</body></html>"
        return HttpResponse(html)

    else:
        html = "<html><body>Invalid Account</body></html>"
        return HttpResponse(html)
