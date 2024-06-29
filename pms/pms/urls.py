
from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.reg, name="reg" ),
    path("log", views.log, name="log" ),
    path("lout", views.lout, name="lout" ),
    path("add", views.add, name="add" ),
    path("pview", views.pview, name="pview" ),
    path("update/<int:id>", views.update, name="update"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("pview_json/<int:id>", views.pview_json, name="pview_json"),
    path("pview_json/<str:name>", views.pview_json1, name="pview_json1"),
    path("product_view/", views.pview_html, name="product_view_html"),
    path("product_view/<int:id>/", views.pview_html, name="product_view_html_with_id"),
    path("add_product_json", views.add_product_json, name="add_product_json"),
    path("view_product_json", views.view_product_json, name="view_product_json"),
    path("update_product_json/<int:id>", views.update_product_json, name="update_product_json"),
    path("delete_product_json/<int:id>", views.delete_product_json, name="delete_product_json"),
    path("part_update_product_json/<int:id>",views.part_update_product_json, name="part_update_product_json"),
]
