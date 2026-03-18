from django.urls import path
from . import views

# Dòng này cực kỳ quan trọng để sửa lỗi NoReverseMatch lúc nãy
app_name = 'pages' 

urlpatterns = [
    # Trang chủ danh sách khóa học
    path('', views.CourseListView.as_view(), name='index'), 
    
    # Trang chi tiết khóa học (Lưu ý dùng <int:pk> cho DetailView)
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    
    # Hàm đăng ký khóa học (nếu có dùng)
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    
    # 2 hàm mới cho phần thi Final Project
    path('<int:course_id>/submit/', views.submit, name='submit'),
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]