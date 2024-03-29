from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from blog.models import BlogPost, BlogComment, Contact, BannerImage
from django.contrib import messages
from django.contrib.auth.models import User
import json
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth.decorators import login_required
from blog.templatetags import get_dict
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
msg = """
        Please note that you are not a VERIFIED USER. To verify, Click <a style='color:#000' href='{url}'><strong><em><u>Here</u></em></strong></a> to navigate to Profile Section to validate email address & mobile number and enjoy services.
    """

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
			url = reverse("profile")
			messages.warning(request, mark_safe(msg.format(url=url)))
	blogposts = BlogPost.objects.all().order_by("-pub_date")

	total_members_count = 0
	total_members = User.objects.all()
	for members in total_members:
		if not members.is_staff:
			total_members_count += 1

	total_blogs_count = 0
	total_blogs = BlogPost.objects.all()
	for blogs in total_blogs:
		if blogs.status == "Published" or blogs.status == "Featured":
			total_blogs_count += 1

	page = request.GET.get('page', 1)
	paginator = Paginator(blogposts, 4)
	try:
		records = paginator.page(page)
	except PageNotAnInteger:
		records = paginator.page(1)
	except EmptyPage:
		records = paginator.page(paginator.num_pages)

	banner_image = BannerImage.objects.all()
	params = {'blogposts':blogposts, 'records':records, 'banner':banner_image, 'total_members_count':total_members_count, 'total_blogs_count':total_blogs_count}
	return render(request, 'blog/index.html', params)

def blogpost(request, id):
	if request.user.is_authenticated:
		if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
			url = reverse("profile")
			messages.warning(request, mark_safe(msg.format(url=url)))
	blogpost = BlogPost.objects.filter(post_id=id)
	comments = BlogComment.objects.filter(post=blogpost[0], parent=None)
	replies = BlogComment.objects.filter(post=blogpost[0]).exclude(parent=None)
	replyDict = {}
	for reply in replies:
		if reply.parent.comment_id not in replyDict.keys():
			replyDict[reply.parent.comment_id] = [reply]
		else:
			replyDict[reply.parent.comment_id].append(reply)

	params = {'blogpost':blogpost[0], 'comments':comments, 'user':request.user, 'replyDict':replyDict}
	return render(request, 'blog/blogpost.html', params)

def postComment(request):
	if request.user.profile.is_verified == "VF" and request.user.profile.is_email_verified == "VF":
		if request.method == "POST":
			comment = request.POST.get("comment")
			user = request.user
			post_id = request.POST.get("post_id")
			post = BlogPost.objects.get(post_id=post_id)
			parent_id = request.POST.get("parent_id")

			# if comment != "" and user != "" and post != "":
			if parent_id == "":
				comment_done = BlogComment(comment=comment, user=user, post=post)
				# response = "True"
				comment_done.save()
				messages.success(request, "Your comment has been posted successfully")
				

			else:
				parent = BlogComment.objects.get(comment_id=parent_id)
				comment_done = BlogComment(comment=comment, user=user, post=post, parent=parent)
				# response = "True"
				comment_done.save()
				messages.success(request, "Your reply has been posted successfully")
			# else:
				# response = "False"
				# messages.success(request, "Your comment has been posted successfully")
			# return HttpResponse('%s' % response)
	else:
		return HttpResponseRedirect("/home/notVerified")
	return redirect(f"/blog/blogPost/{post_id}")
	# return render(request, 'blog/blogpost.html')

def search(request):
	if request.user.is_authenticated:
		if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
			url = reverse("profile")
			messages.warning(request, mark_safe(msg.format(url=url)))
	query = request.GET.get("query")
	if len(query) > 60:
		all_posts = BlogPost.objects.none()
	else:
		all_posts_title = BlogPost.objects.filter(title__icontains=query)
		all_posts_content = BlogPost.objects.filter(content_heading1__icontains=query)
		all_posts = all_posts_title.union(all_posts_content)

	params = {'all_posts':all_posts, 'query':query, 'message':''}
	if len(all_posts) == 0 or len(query) <= 1:
		params = {'message':'Search Not Found, Search again...'}
	return render(request, "blog/search.html", params)

def contact(request):
	if request.user.is_authenticated:
		if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
			url = reverse("profile")
			messages.warning(request, mark_safe(msg.format(url=url)))
		
	if request.method == "POST":
		try:
			name = request.POST.get("name")
			email = request.POST.get("email")
			mobile = request.POST.get("mobile")
			message = request.POST.get("message")
			contact = Contact(name=name, email=email, mobile=mobile, message=message)
			contact.save()
			response = json.dumps({"status": "success"})
			return HttpResponse(response)
		except Exception as e:
			response = json.dumps({"status": "failure"})
			return HttpResponse(response)
        # messages.success(request, "Your response has been successfully recorded."
	return render(request, "blog/contact.html")

def publish(request):
	if request.user.is_authenticated:
		if request.user.profile.is_verified == "VF" and request.user.profile.is_email_verified == "VF":
			if request.method == "POST":
				title = request.POST.get("title")
				first_heading = request.POST.get("first_heading")
				first_content = request.POST.get("first_content")
				second_heading = request.POST.get("second_heading")
				second_content = request.POST.get("second_content")
				sub_heading = request.POST.get("sub_heading")
				sub_content = request.POST.get("sub_content")
				
				publish = BlogPost(title=title, heading1=first_heading, content_heading1=first_content, heading2=second_heading, content_heading2=second_content, sub_heading=sub_heading, sub_heading_content=sub_content, author=request.user.first_name)
				publish.save()
				messages.success(request, "Your content has been submitted successfully for review. Your content will be published after successful review.")
				return HttpResponseRedirect("/blog/publish")
		else:
			return HttpResponseRedirect("/home/notVerified")
	else:
		return HttpResponseRedirect("/home/cannot_access")
	return render(request, "blog/publish.html")
