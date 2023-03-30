from django.contrib import admin

from company_back.models import Balance, Chat, Country, Gift, Match, Media, Message, Purchase, User

admin.site.register(Country)
admin.site.register(Balance)
admin.site.register(Media)
admin.site.register(Gift)
admin.site.register(User)
admin.site.register(Purchase)
admin.site.register(Match)
admin.site.register(Chat)
admin.site.register(Message)
