from app import app, render_template

@app.route('/detail/<int:product_id>/<string:category>/<string:detail_name>')
def product_detail(product_id, category, detail_name):
    # Get the product name based on the product_id
    return render_template('detail.html', product_id=product_id, category=category, detail_name=detail_name)