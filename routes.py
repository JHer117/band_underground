from config import app
from controller_functions import home, create_account_page, add_user, login, main_dashboard, user_profile, edit_user, update_user, post_page, create_band_post, edit_band_page, update_band, delete_band, logout

app.add_url_rule("/", view_func=home)
app.add_url_rule("/create_account", view_func=create_account_page)
app.add_url_rule("/add_user", view_func=add_user, methods = ["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/underground/dashboard", view_func=main_dashboard)
app.add_url_rule("/profile/<user_id>", view_func=user_profile)
app.add_url_rule("/edit/<user_id>", view_func=edit_user)
app.add_url_rule("/update_user/<user_id>", view_func=update_user, methods=["POST"])
app.add_url_rule("/post_band", view_func=post_page)
app.add_url_rule("/create_post", view_func=create_band_post, methods=["POST"])
app.add_url_rule("/edit_band/<bandid>", view_func=edit_band_page)
app.add_url_rule("/update_band/<bandid>", view_func=update_band, methods=["POST"])
app.add_url_rule("/delete_band/<bandid>", view_func=delete_band)
app.add_url_rule("/logout", view_func = logout)