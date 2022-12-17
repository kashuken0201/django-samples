from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from .forms import StudentForm


def create_view(request):
    initial_value = {
        'code': '102140055',
        'name': 'An trinh',
        'address': 'Quang nam'
    }
    form = StudentForm(request.POST or None, initial=initial_value)
    if form.is_valid():
        form.save()
        return redirect('/students')
    context = {'form': form}
    return render(request, 'create.html', context)


def update_view(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('/students')
    context = {'form': form}
    return render(request, 'create.html', context)


def delete_view(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
        return redirect('/students')
    context = {'student': student}
    return render(request, 'delete.html', context)


def detail_view(request, id):
    student = get_object_or_404(Student, id=id)
    context = {'student': student}
    return render(request, 'detail.html', context)


def list_view(request):
    keyword = request.GET.get('keyword')
    if keyword:
        students = Student.objects.filter(code=keyword)
    else:
        students = Student.objects.all()
    students = Student.objects.all()
    context = {
        'students': students,
        'keyword':keyword
    }
    return render(request, 'list.html', context)
