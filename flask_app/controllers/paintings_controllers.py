from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user_model import User
from flask_app.models.painting_model import Painting




# =================================================
#  Dashboard
# =================================================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    user_id = session["user_id"]     
    # Retrieve the user name
    user_data = {
        'id' : user_id
    }
    user = User.get_by_id(user_data)
    # Retrieve the paintings
    paintings = Painting.get_all_paintings()

    return render_template("dashboard.html", user = user, paintings = paintings)

#==================================================
#Route from Dashboard to New Painting Page
# =================================================



@app.route("/new/painting")
def new_painting():
    return render_template("new_painting.html")


# ===================================================
# Route from New Painting Page to Create New Painting
# ===================================================


@app.route("/create/painting", methods=["post"])
def create_painting():
    # 1 validate form info
    if not Painting.validate_painting(request.form):
        return redirect("/new/painting")
    if 'user_id' not in session:
        flash("Please log in to see this page")
        return redirect('/')
    query_data = {
        "title" : request.form["title"],
        "description" : request.form["description"],
        "price" : int(request.form["price"]),
        "user_id" : session["user_id"]
    }
   
    Painting.create_new_painting(query_data)
    return redirect("/dashboard")


# =========================================
# Route from Dashboard to Delete Painting
# =========================================


@app.route("/paintings/<int:id>/delete")
def delete_painting(id):
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    user_id = session["user_id"]     
    query_data = {
        "id" : id,
        "user_id" : user_id
    }
    Painting.delete_painting(query_data)
    return redirect("/dashboard")


# ========================================
# Route from Dashboard to Edit Painting Page
# ========================================

@app.route("/paintings/<int:id>/edit")
def edit_painting_page(id):
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    user_id = session["user_id"]
    query_data = {
        "id" : id,
        "user_id" : user_id
    }
    painting = Painting.get_painting_by_id(query_data)
    return render_template("edit_painting.html", painting = painting)

# ============================================
# Route to sumbit Edit from Edit Page
# =============================================

@app.route("/paintings/<int:id>/edit", methods=["post"])
def edit_painting(id):
    # 1 validate form info
    painting_id = request.form["painting_id"]
    if not Painting.validate_painting(request.form):
        return redirect(f"/paintings/{painting_id}/edit")
   
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    user_id = session["user_id"]     
    query_data = {
        "id" : id,
        "user_id" : user_id,
        "title" : request.form["title"],
        "description" : request.form["description"],
        "price" : int(request.form["price"])
    }
    Painting.edit_painting(query_data)
    return redirect("/paintings/" + str(id))




# =====================================
# Route to One Painting
# =====================================


@app.route("/paintings/<int:id>")
def one_painting(id):
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    query_data = {
        "id" : id
    }
    painting = Painting.get_painting_by_id(query_data)
    return render_template("one_painting.html", painting = painting)

