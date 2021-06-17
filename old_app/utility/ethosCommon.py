import json
import datetime
from utility.mailTemplates.emailTemplates import emailTemplates
import math
import os
from rest_framework import status
import config_rename.settings as settings
from config_rename.settings import config

#from Models.Common.applicationConfig import webConfigKey


class EthosCommon():

    def sendVerificationCode(name, email, otp):

        # Send email
        subject = ""
        title = ""
        messageBodyPart1 = ""
        messageBodyPart2 = "."
        messageBodyPart3 = ""
        messageBodyPart3 += "<strong>OTP: "+otp+"</strong>"
        messageBodyPart5 = ""
        messageBodyPart6 = ""

        message = '<h3>'+messageBodyPart1+" "+name+","+'</h3><p>'
        message += messageBodyPart2+'</p><p>' + \
            messageBodyPart3+'</p><br/><br/>'+'<br/><br/>'
        message += '<p><br/>'+messageBodyPart5+","+'</p><p>'+messageBodyPart6+'</p>'
        emailFrom = config.EMAIL_HOST_USER
        emailTo = email
        emailTemplates.sendLinkMail(
            subject, emailFrom, emailTo, message, title)

    def send_content_moderation_email(post_details, invalid_content_type = ''):

        # Send email
        subject = ""
        title = ""
        messageBodyPart1 = ""
        messageBodyPart2 = ""
        messageBodyPart3 = ""
        messageBodyPart3 += ""
        messageBodyPart3 += ""
        messageBodyPart3 += ""
        messageBodyPart3 += ""
        messageBodyPart3 += ""
        messageBodyPart5 = ""
        messageBodyPart6 = ""

        message = '<h3>'+messageBodyPart1+'</h3><p>'
        message += messageBodyPart2+'</p><p>' + \
                    messageBodyPart3+'</p><br/><br/>'+'<br/><br/>'
        message += '<p><br/>'+messageBodyPart5+","+'</p><p>'+messageBodyPart6+'</p>'
        emailFrom = config.ADMIN_EMAIL_ID
        emailTo = config.ADMIN_EMAIL_ID
        emailTemplates.sendLinkMail(subject, emailFrom, emailTo, message, title)

    def send_user_moderation_email(user_details):

        # Send email
        subject = ""
        title = ""
        messageBodyPart1 = ""
        messageBodyPart2 = ""
        messageBodyPart3 = ""
        messageBodyPart3 += ""
        messageBodyPart3 += "<strong>Inappropriate content detected in: Users bio</strong><br/>"
        messageBodyPart3 += "<strong>Name: "+user_details['name']+"</strong><br/>"
        messageBodyPart3 += "<strong>Email: "+user_details['email']+"</strong><br/>"
        messageBodyPart3 += "<strong>Bio: "+user_details['bio']+"</strong><br/>"
        messageBodyPart5 = ""
        messageBodyPart6 = ""

        message = '<h3>'+messageBodyPart1+'</h3><p>'
        message += messageBodyPart2+'</p><p>' + \
                    messageBodyPart3+'</p><br/><br/>'+'<br/><br/>'
        message += '<p><br/>'+messageBodyPart5+","+'</p><p>'+messageBodyPart6+'</p>'
        emailFrom = config.ADMIN_EMAIL_ID
        emailTo = config.ADMIN_EMAIL_ID
        emailTemplates.sendLinkMail(subject, emailFrom, emailTo, message, title)

    def get_file_extention(file_name):
        file_ext = file_name.split(".")[-1]
        return file_ext
