from django.contrib import admin

from company_back.models import  Chat, Country, Match, Media, Message, User

admin.site.register(Country)
admin.site.register(Media)
admin.site.register(User)
admin.site.register(Match)
admin.site.register(Chat)
admin.site.register(Message)
