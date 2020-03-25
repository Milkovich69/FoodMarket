from app import app, db
from app.models import City, User, Company, ProductGroup, Product, Capability,\
    Need, Supply, Notification, Message


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'City': City, 'User': User, 'Company': Company, 'ProductGroup': ProductGroup,
            'Product': Product, 'Capability': Capability, 'Need': Need, 'Supply': Supply,
            'Message': Message, 'Notification': Notification}