from django.shortcuts import render_to_response,redirect
from django.conf import settings
from django.template import RequestContext
from courses.forms import CourseForm,CourseMemberForm
from courses.models import Course,CourseMembership
#from courses.signals import CreateCourseMembership 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,get_list_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
#Course registration
#permission create and check

@login_required
def RegisterCourse(request):
	if request.method =='POST':
    		form = CourseForm(request.POST,request.FILES)

	if form.is_valid():
		newCourse = form.save(commit=False)
		newCourse.save(user = request.user)

		#CreateCourseMembership.send(sender = Course,instance=newCourse,user=request.user,created = True)
		return redirect(reverse('course_home_url', args(newCourse.id,))) # Redirect after POST
	else:
		form = CourseForm() # An unbound form

	return render_to_response('courses/register.html', {
    		'form': form,
	},context_instance=RequestContext(request))


#decide on membership policy- members only view....or all with restricted access
@login_required
def CourseHome(request,id):
	course = get_object_or_404(Course,pk = id)
	courseAdmin =get_object_or_404(CourseMembership,course__id__exact =id,userType='OW').user

	courseMods =[]
	try:
		courseWithMods = CourseMembership.objects.filter(course__id__exact = id,userType="MO")
		courseMods = [course.user for course in courseWithMods]
	except CourseMembership.DoesNotExist:
		pass
	return render_to_response('courses/course.html',{
		'course':course,
		'courseAdmin':courseAdmin,
		'courseMods':courseMods,
		})


#decide on permission and execution policy
@login_required
def CourseMember(request,id):
	course = get_object_or_404(Course,pk=id)	
	courseMembers = (get_list_or_404(CourseMembership.objects.all().order_by('userType'),course__id__exact=id))
	
	if request.method== 'POST':
		form = CourseMemberForm(request.POST)
		
		if form.is_valid():
			new_member = form.save(commit=False)
			new_member.course = course
			new_member.save()

			return redirect(reverse('course_member_url',args=(id,)))
	else:
		form = CourseMemberForm(course_id=id)
	return render_to_response('courses/courseMember.html', {
			'form': form,
			'course':course,
			'courseMembers':courseMembers,
			},context_instance=RequestContext(request))


#Decide Permission
@login_required
def FlipMembership(request,course_id,user_id):
	course = get_object_or_404(CourseMembership,course__id__exact =course_id,user__id=user_id)
	if(course.userType=='MO'):
		course.userType = 'ST'
	elif(course.userType == 'ST'):
		course.userType = 'MO'
	else:
		return HttpResponseNotFound("<h1>Not a valid request</h1>")

	course.save()
	#respond by redirecting to original page.
	return redirect(reverse('course_member_url',args=(course_id,)))

	#redirect(request.META.HTTP_REFERER)
	
