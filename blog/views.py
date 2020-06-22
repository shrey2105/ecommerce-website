from django.shortcuts import render, redirect, HttpResponse
from blog.models import BlogPost, BlogComment
from django.contrib import messages
import json
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth.decorators import login_required
from blog.templatetags import get_dict

# Create your views here.
def index(request):
	blogposts = BlogPost.objects.all()
	params = {'blogposts':blogposts}
	return render(request, 'blog/index.html', params)

def blogpost(request, id):
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
	return redirect(f"/blog/blog/blogPost/{post_id}")
	# return render(request, 'blog/blogpost.html')

# def loadComment(request):
# 	if request.method == "POST":
# 		post_id = request.POST.get("post_id")
# 		blogpost = BlogPost.objects.filter(post_id=post_id)
# 		comments = BlogComment.objects.filter(post=blogpost[0])
# 		if len(comments) > 0:
# 			updates = []
# 			for data in comments:
# 				updates.append({"user":data.user, "comment":data.comment, "comment_id":data.comment_id, "timestamp":naturaltime(data.timestamp)})
# 				response = json.dumps({"status":"success", "updates":updates}, default=str)
# 			return HttpResponse(response)
# 		else:
# 			response = json.dumps({"status":"noitem"})
# 			return HttpResponse(response)
# 	return HttpResponse(request)
