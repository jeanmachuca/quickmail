#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from email.mime.image import MIMEImage

os.environ.setdefault('LANG','en_US')
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../../'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../'))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

def main():
    connection = mail.get_connection()
    
    # Manually open the connection
    connection.open()
    DeliveryQueue.objects.filter(enviado=True).delete()
    queue = DeliveryQueue.objects.exclude(enviado=True)
    for q in queue:
        link = 'http://admin.quickmail.cl?m=%s&e=%s' % (str(q.delivery.plantilla.pk),str(q.email.pk))
        nombre = '%s %s' % (q.email.nombre,q.email.apellido)
        msg = EmailMultiAlternatives('%s %s' % (nombre,q.subject), q.plainContent, q.from_email, [q.email.email])
        header_html = '<html><body><h2>Estimado: %s</h2><p>Si no puede ver el contenido de este mensaje haga click en el link <a href="%s">%s</a></p><br/>'% (nombre,link,link)
        disclaimer = u'Este correo electrónico fue enviado a %s. Si no quiere recibir estos emails, haga clic en el link <a href="%s">%s</a> \
                        Este e-mail ha sido enviado por la plataforma QuickMail.' % (q.email.email,link,link)
        footer_html = '</body></footer>'
        msg.attach_alternative('%s%s%s%s' % (header_html,q.htmlContent,disclaimer,footer_html), "text/html")
        msg.mixed_subtype = 'related'
        for f in q.attachedFiles:
            try:
                fp = open(f, 'rb')
                msg_img = MIMEImage(fp.read())
                fp.close()
                msg_img.add_header('Content-ID', '<{}>'.format(os.path.basename(f)))
                msg.attach(msg_img)
            except:
                pass
        try:
            msg.send()
            q.enviado = True
            q.save()
            print 'Sent %s %s %s \n' % (str(q.pk),q.from_email,q.email.email)
            time.sleep(1)
        except:
            pass

    try:
        connection.close()
    except:
        pass


if __name__ == "__main__":
    os.environ['APPLICATION_ID']= 'croncalificacion'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    from django.db import connection as dbconnection
    dbconnection.close()
    
    import settings 
    from django.core.mail import EmailMultiAlternatives
    from django.core import mail
    import time
    from emails.models import * 
    
    sys.exit(main())
