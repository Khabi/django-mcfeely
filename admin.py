from django.contrib import admin
from mcfeely.models import Queue, Email, Unsubscribe, Attachment, Alternative, Header

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
    list_display = ('m_to', 'subject', 'queue', 'deferred', 'sent')
    inlines = [AlternativeInline, AttachmentInline, HeaderInline]
    list_filter = ('queue', 'm_to', 'deferred', 'sent')


admin.site.register(Queue)
admin.site.register(Email, EmailAdmin)
admin.site.register(Unsubscribe)

