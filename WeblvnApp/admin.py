from django.contrib import admin
from Weblvn.WeblvnApp.models import Branch, Lvn_entry, DBUpdate, Wiki_entry, LVN_Feature_Related, Build_entry 

admin.site.register(Branch)
admin.site.register(Lvn_entry)
admin.site.register(DBUpdate)
admin.site.register(Wiki_entry)
admin.site.register(LVN_Feature_Related)
admin.site.register(Build_entry)
