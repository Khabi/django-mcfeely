from django.contrib import admin
from mcfeely.models import Queue, Email, Unsubscribe, Attachment, Alternative, Header
from mcfeely.models import Recipient

class RecipientInline(admin.TabularInline):
    model = Recipient
    extra = 0


class AlternativeInline(admin.TabularInline):
    model = Alternative
    extra = 0


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


class HeaderInline(admin.TabularInline):
    model = Header
    extra = 0


class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'queue', 'created')
    inlines = [RecipientInline, AlternativeInline, AttachmentInline, HeaderInline]
    #list_filter = ('queue', 'm_to', 'status')


class UnsubscribeAdmin(admin.ModelAdmin):
    list_display = ('address', 'added', 'queue')
    list_filter = ('address', 'added', 'queue')


admin.site.register(Queue)
admin.site.register(Email, EmailAdmin)
admin.site.register(Unsubscribe, UnsubscribeAdmin)

