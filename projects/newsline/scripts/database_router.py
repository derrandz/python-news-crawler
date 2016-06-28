# database_router.py

class MainDatabaseRouter:
    """A router to control newsworm database operations
    """
    
    def db_for_read(self, model, **hints):
        "Point all operations on newsworm models to 'newsworm_db'"

        if model._meta.app_label == 'newsworm':
            return 'newsworm_db'
        return 'newsline_main'

    def db_for_write(self, model, **hints):
        "Point all operations on newsworm models to 'newsworm_db'"

        if model._meta.app_label == 'newsworm':
            return 'newsworm_db'
        return 'newsline_main'

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if the two models are in newsworm"

        if obj1._meta.app_label == 'newsworm' and \
           obj2._meta.app_label == 'newsworm':
            return True

        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        "Make sure the auth app only appears in the 'newsworm_db' database."

        if app_label == 'newsworm':
            print("Routing... allow_migrate: [db: %s, app_label: %s, model_name: %s]" % (db, app_label, model_name))
            return db == 'newsworm_db'

        if db == 'newsline_main':
            return True
        
        return False