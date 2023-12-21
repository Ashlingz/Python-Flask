from app import app, render_template, request, redirect
import mysql.connector

con = mysql.connector.connect(host='localhost',
                              user='root',
                              passwd='',
                              db='flask',
                              port=3306)

cursor = con.cursor(dictionary=True)


@app.route('/admin/product')
def product():
    cursor.execute('SELECT product_name, price, image, p.status, category_name FROM products p JOIN categories c ON p.category_id = c.category_id;')
    row = cursor.fetchall()
    return render_template('admin/product.html', product=row)

def category_display():
    cursor.execute('SELECT category_name, category_id FROM categories')
    c = cursor.fetchall()
    return render_template('admin/product.html', category=c)


@app.route('/admin/product_index/<string:name>')
def product_index(name):
    select_index = 'SELECT * FROM products WHERE product_name = %s'
    try:
        cursor.execute(select_index, (name,))
        row = cursor.fetchone()
        cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error executing SQL query: {err}")
        return render_template('error.html', message="Database error")

    return render_template('admin/product_edit.html', row=row)

@app.route('/admin/product_edit/<string:name>', methods=['POST'])
def product_edit(name):
    if request.method == 'POST':
        category_id = request.form['category_name']
        product_name = request.form['product_name']
        price = request.form['price']
        status = request.form['status']

        update_sql = "UPDATE products SET product_name = %s, price = %s, status = %s WHERE product_name = %s"
        cursor.execute(update_sql, (product_name, price, status, name))
        con.commit()

        return redirect('/admin/product')
#
#
@app.route('/admin/product_add', methods=['POST'])
def product_add():
    if request.method == 'POST':
        category_id = request.form['category_name']
        product_name = request.form['name']
        price = request.form['price']
        status = request.form['status']
        if not product_name == '':
            product_name
        else:
            product_name = 'No Name'

        insert_sql = "INSERT INTO products(category_id, product_name, price, image, status, cost) VALUES(1, %s, %s, 'null', %s, %s)"
        cursor.execute(insert_sql, (product_name, price, status, price))
        con.commit()
        return redirect('/admin/product')


@app.route('/admin/product_delete/<string:name>', methods=['POST'])
def product_delete(name):
    if request.method == 'POST':
        n = name
        try:
            delete_sql = "DELETE FROM products WHERE product_name = %s"
            cursor.execute(delete_sql, (name,))
            con.commit()
            msg = "Record successfully deleted"
            return redirect('/admin/product')
        except Exception as e:
            con.rollback()
            msg = "Error in delete operation: " + str(e)


