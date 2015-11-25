#!coding=utf-8
from django.contrib import admin
from api.menu import send_menu
from models import *


class WMenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu_type', 'value', 'position')
    list_filter = ('menu_type',)
    actions = ['update_menu']

    def update_menu(self, request, queryset):
        result, code = send_menu()
        if not result:
            self.message_user(request, u'%s' % code)
        else:
            self.message_user(request, u'菜单更新成功！')
    update_menu.short_description = "更新菜单到微信"

admin.site.register(WMenu, WMenuAdmin)
admin.site.register(PayInfoModel)
admin.site.register(User)
