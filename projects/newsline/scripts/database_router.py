# database_router.py
# For each database, we implement a database router that will route the queries appropriately. 
# In our case, we implement a database for each app.

# Database router for newsworm
class MainDatabaseRouter(object):
    '''
    A router to control the main database's operations
    '''

    def db_for_read(self, model, **hints):
        "Point all operations on the main database models to 'newsline_main_db'"

        from django.conf import settings

        # if not settings.TESTING:
        if not 'newsline_main_db' in settings.DATABASES:
            return None
        
        if model._meta.app_label != 'newsworm':
            return 'newsline_main_db'
        elif model._meta.app_label == 'newsworm':
            return 'newsworm_db'
        
        return None
        # else:
        #     if model._meta.app_label != 'newsworm':
        #         return 'test_newsline_main_db'
        #     elif model._meta.app_label == 'newsworm':
        #         return 'test_newsworm_db'

    def db_for_write(self, model, **hints):
        "Point all operations on the main database models to 'newsline_main_db'"

        from django.conf import settings

        # if not settings.TESTING:
        if not 'newsline_main_db' in settings.DATABASES:
            return None

        if model._meta.app_label != 'newsworm':
            return 'newsline_main_db'
        elif model._meta.app_label == 'newsworm':
            return 'newsworm_db'

        return None
        # else:
        #     if model._meta.app_label != 'newsworm':
        #         return 'test_newsline_main_db'
        #     elif model._meta.app_label == 'newsworm':
        #         return 'test_newsworm_db'

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if the two models are in newsworm"

        from django.conf import settings

        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        "Make sure the auth app only appears in the 'newsline_main_db' database."

        from django.conf import settings

        # if not settings.TESTING:
        if app_label != 'newsworm':
            return db == 'newsline_main_db'
        elif model._meta.app_label == 'newsworm':
            return 'newsworm_db'
            
        return None
        # else:
        #     if app_label != 'newsworm':
        #         return db == 'test_newsline_main_db'
        #     elif app_label == 'newsworm':
        #         return db == 'test_newsworm_db'