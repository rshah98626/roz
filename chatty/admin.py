#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Article)
admin.site.register(Fund)
admin.site.register(Post)
admin.site.register(StockHolding)
admin.site.register(Video)
