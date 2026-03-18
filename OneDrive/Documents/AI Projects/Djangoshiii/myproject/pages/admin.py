# Mở file onlinecourse/admin.py và sửa lại như sau:
from django.contrib import admin
# Đảm bảo import đủ 7 class sau (điều chỉnh tên nếu boilerplate của bạn có tên khác chút ít)
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

# 1. Tạo ChoiceInline và QuestionInline
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4 # Hiển thị sẵn 4 ô trống để nhập lựa chọn (A, B, C, D)

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

# 2. Tạo QuestionAdmin
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['content', 'course']

# 3. Tạo LessonAdmin
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']

class LessonInline(admin.StackedInline): 
    model = Lesson 
    extra = 5
# Cập nhật CourseAdmin để chứa LessonInline và QuestionInline
class CourseAdmin(admin.ModelAdmin):
    # Khai báo LessonInline nếu boilerplate đã có sẵn, thêm QuestionInline vào
    # Giả sử boilerplate đã định nghĩa LessonInline ở trên
    inlines = [LessonInline, QuestionInline] 
    list_display = ('name', 'pub_date')

# Đăng ký các model với admin site
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)