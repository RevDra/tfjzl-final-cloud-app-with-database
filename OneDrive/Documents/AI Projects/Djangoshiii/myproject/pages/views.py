from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Course, Enrollment, Question, Choice, Submission

class CourseListView(generic.ListView):
    template_name = 'pages/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-pub_date')[:10]  # Lấy danh sách khóa học

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'pages/course_detail_bootstrap.html'

def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        # Tạo đăng ký học cho user hiện tại
        Enrollment.objects.create(user=request.user, course=course)
        return redirect('pages:course_details', pk=course.id)
    
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Create a submission linked to the user's enrollment
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Check selected choices
        for question in course.question_set.all():
            selected_choice_id = request.POST.get(f'choice_{question.id}')
            if selected_choice_id:
                selected_choice = Choice.objects.get(pk=selected_choice_id)
                submission.choices.add(selected_choice)
                
        submission.save()
        return redirect('pages:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Lấy danh sách ID các câu trả lời mà user đã chọn
    selected_ids = [choice.id for choice in submission.choices.all()]
    
    # Định nghĩa hàm is_get_score() theo đúng yêu cầu của hệ thống chấm điểm
    def is_get_score():
        total_questions = course.question_set.count()
        correct_answers = 0
        for choice in submission.choices.all():
            if choice.is_correct:
                correct_answers += 1
        return (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    # Sử dụng hàm vừa tạo để tính grade
    grade = is_get_score()
    passed = grade >= 80 
    
    # Bổ sung đầy đủ grade và selected_ids vào context
    context = {
        'course': course,
        'submission': submission,
        'grade': round(grade, 2),  # Bắt buộc phải có tên là 'grade'
        'score': round(grade, 2),  # Giữ lại 'score' cho giao diện cũ của bạn
        'passed': passed,
        'selected_ids': selected_ids # Bắt buộc phải có biến này
    }
    return render(request, 'pages/exam_result_bootstrap.html', context)
