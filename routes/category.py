from app import app, render_template, request, redirect
import mysql.connector

con = mysql.connector.connect(host='localhost',
                              user='root',
                              passwd='',
                              db='flask',
                              port=3306)

cursor = con.cursor(dictionary=True)


@app.route('/admin/category')
def admin():
    cursor.execute('SELECT * FROM categories')
    row = cursor.fetchall()
    return render_template('admin/category.html', data=row)


@app.route('/admin/category_index/<string:name>')
def category_index(name):
    select_index = 'SELECT * FROM categories WHERE category_name = %s'
    try:
        cursor.execute(select_index, (name,))
        row = cursor.fetchone()  # Fetch all results
        # Consume the results to avoid "Unread result found" error
        cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error executing SQL query: {err}")
        return render_template('error.html', message="Database error")

    return render_template('admin/category_edit.html', row=row)


@app.route('/admin/category_edit/<string:name>', methods=['POST'])
def category_edit(name):
    if request.method == 'POST':
        new_category_name = request.form['cname']
        status = request.form['status']
        update_sql = "UPDATE categories SET category_name = %s, status = %s WHERE category_name = %s"
        cursor.execute(update_sql, (new_category_name, status, name))
        con.commit()

        return redirect(url_for('admin'))


# Route for adding a category
@app.route('/admin/category_add', methods=['POST'])
def category_add():
    if request.method == 'POST':
        category_name = request.form['cname']
        status = request.form['status']
        if not category_name == '':
            category_name
        else:
            category_name = 'No Name'

        # SQL statement to insert a new category
        insert_sql = "INSERT INTO categories (category_name, status) VALUES (%s, %s)"

        # Execute the SQL statement
        cursor.execute(insert_sql, (category_name, status))
        con.commit()  # Commit the changes to the database

        return redirect(url_for('admin'))


@app.route('/admin/category_delete/<string:name>', methods=['POST'])
def category_delete(name):
    if request.method == 'POST':
        n = name
        try:
            delete_sql = "DELETE FROM categories WHERE category_name = %s"
            cursor.execute(delete_sql, (name,))
            con.commit()
            msg = "Record successfully deleted"
            return redirect(url_for('admin'))
        except Exception as e:
            con.rollback()
            msg = "Error in delete operation: " + str(e)
