from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    
    z = merge_dicts(a, b, c, d, e, f, g) 
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def merge_message(request,args):
    if 'type' in request.session :
        cur = {'notification' : {'type': request.session['type'], 'msg':request.session['message']}}
        del request.session['type']
        del request.session['message']
        return merge_dicts(args,cur)
    else :
        return args

def add_message(request,type,msg):
    request.session['type'] = type
    request.session['message'] = msg


def home(request):
    if request.user.is_authenticated():
        return redirect(reverse('view_dashboard'))
    else :
    	return render(request, 'accounts/index.html',{'type' : 'home'})

def about(request):
	return render(request, 'accounts/about.html',{'type' : 'about'})

def contact(request):
	args = {'type' : 'contact'}
	args = merge_message(request,args)
	return render(request, 'accounts/contact.html', args)


def login_redirect(request) :
    return  redirect('/accounts/login')


