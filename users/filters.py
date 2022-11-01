from django.contrib.admin import SimpleListFilter


class NFTCollectionIdFilter(SimpleListFilter):
    title = 'collection id'
    parameter_name = 'collection_id'

    def lookups(self, request, model_admin):
        objects = model_admin.model.objects
        filter_objects = objects.all() if request.user.is_superuser else objects.filter(user=request.user)
        lookups = set((c.id, c.id) for c in filter_objects)

        return lookups if len(lookups) > 1 else None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(pk=self.value())

        return queryset


class NFTCollectionWalletFilter(SimpleListFilter):
    title = 'wallet address'
    parameter_name = 'user__wallet_address'

    def lookups(self, request, model_admin):
        objects = model_admin.model.objects
        filter_objects = objects.all() if request.user.is_superuser else objects.filter(user=request.user)
        lookups = set((c.user.wallet_address, c.user.wallet_address) for c in filter_objects if c.user.wallet_address)

        return lookups if len(lookups) > 1 else None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__wallet_address=self.value())

        return queryset


class NFTCollectionUsernameFilter(SimpleListFilter):
    title = 'username'
    parameter_name = 'user__username'

    def lookups(self, request, model_admin):
        objects = model_admin.model.objects
        filter_objects = objects.all() if request.user.is_superuser else objects.filter(user=request.user)
        lookups = set((c.user.username, c.user.username) for c in filter_objects)

        return lookups if len(lookups) > 1 else None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__username=self.value())

        return queryset


class NFTCollectionCategoryFilter(SimpleListFilter):
    title = 'category'
    parameter_name = 'collection__category'

    def lookups(self, request, model_admin):
        objects = model_admin.model.objects
        filter_objects = objects.all() if request.user.is_superuser else objects.filter(user=request.user)
        lookups = set((c.category.pk, c.category.name) for c in filter_objects if c.category)

        return lookups if len(lookups) > 1 else None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__pk=self.value())

        return queryset


class NFTCollectionFilter(SimpleListFilter):
    title = 'collection'
    parameter_name = 'collection'

    def lookups(self, request, model_admin):
        objects = model_admin.model.objects
        filter_objects = objects.all() if request.user.is_superuser else objects.filter(user=request.user)
        lookups = set((c.collection.id, c.collection.name) for c in filter_objects)

        return lookups if len(lookups) > 1 else None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(collection__pk=self.value())

        return queryset
