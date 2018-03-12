from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, StudioItem


app = Flask(__name__)

engine = create_engine('sqlite:///collectioncatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


# Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
# items = []


@app.route('/category/<int:category_id>/studio/JSON')
def categoryStudioJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(StudioItem).filter_by(
        category_id=category_id).all()
    return jsonify(StudioItems=[i.serialize for i in items])


@app.route('/category/<int:category_id>/studio/<int:studio_id>/JSON')
def studioItemJSON(category_id, studio_id):
    Studio_Item = session.query(StudioItem).filter_by(id=studio_id).one()
    return jsonify(Studio_Item=Studio_Item.serialize)


@app.route('/category/JSON')
def categoryJSON():
    category = session.query(Category).all()
    return jsonify(category=[r.serialize for r in categories])


# Show all category
@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).all()
    # return "This page will show all my categories"
    return render_template('categories.html', categories=categories)


# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')
    # return "This page will be for making a new restaurant"

# Edit a category


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            return redirect(url_for('showCategories'))
    else:
        return render_template(
            'editCategory.html', category=editedCategory)

    # return 'This page will be for editing restaurant %s' % restaurant_id

# Delete a restaurant


@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(
            url_for('showCategory', category_id=category_id))
    else:
        return render_template(
            'deleteCategory.html', category=categoryToDelete)
    # return 'This page will be for deleting restaurant %s' % restaurant_id


# Show a category menu
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/studio/')
def showStudio(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(StudioItem).filter_by(
        category_id=category_id).all()
    return render_template('studio.html', items=items, category=category)
    # return 'This page is the studio for category %s' % category_id

# Create a new studio item


@app.route(
    '/category/<int:category_id>/studio/new/', methods=['GET', 'POST'])
def newStudioItem(category_id):
    if request.method == 'POST':
        newStudio = StudioItem(name=request.form['name'], category=request.form[
                           'description'], price=request.form['price'], Address=request.form['course'], category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showStudio', category_id=category_id))
    else:
        return render_template('newstudioitem.html', category_id=category_id)

    #return render_template('newStudioItem.html', category=category)
    # return 'This page is for making a new menu item for restaurant %s'
    # %restaurant_id

# Edit a menu item


@app.route('/category/<int:category_id>/studio/<int:studio_id>/edit',
           methods=['GET', 'POST'])
def editStudioItem(category_id, studio_id):
    editedItem = session.query(StudioItem).filter_by(id=studio_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['Address']:
            editedItem.course = request.form['Address']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showStudio', category_id=category_id))
    else:

        return render_template(
            'editstudioitem.html', category_id=category_id, studio_id=studio_id, item=editedItem)

    # return 'This page is for editing menu item %s' % menu_id

# Delete a menu item


@app.route('/category/<int:category_id>/studio/<int:studio_id>/delete',
           methods=['GET', 'POST'])
def deleteStudioItem(category_id, studio_id):
    itemToDelete = session.query(StudioItem).filter_by(id=studio_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showStudio', category_id=category_id))
    else:
        return render_template('deleteStudioItem.html', item=itemToDelete)
    # return "This page is for deleting menu item %s" % menu_id


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)






