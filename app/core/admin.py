from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models
from django.utils.translation import ugettext_lazy as _


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'email', 'nome',
                    # 'cognome', 'telefono',
                    # 'provincia_ita', 'provincia_estero',
                    # 'stato', 'stato_estero'
                    ]
    fieldsets = (
                    (None, {'fields': ('email', 'password')}),
                    (_('Dati personali'), 
                        {'fields': ('nome',
                         'cognome', 'telefono', 'indirizzo','citta',
                         'provincia_ita', 'provincia_estero', 'stato',
                         'stato_estero')
                        }
                    ),
                (
        _('Permissions'),
        {
            'fields': (
                        'is_active',
                        'is_admin',
                        'is_teacher',
                        'is_staff',
                        'is_superuser',
                        'is_student'

                        )
        }
    ),
    (_('Important dates'), {'fields': ('last_login',)}),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Provincia)
