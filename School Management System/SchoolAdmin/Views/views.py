from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from ..models import *
from django.http import JsonResponse,HttpResponse 
from django.conf import settings
from django.core.mail import send_mail
import random


# Create your views here.

def login(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        msg  = ""
        try:
            select_user = users.objects.get(user_email=email)
            if check_password(password,select_user.user_password) and select_user.user_status==1:
                request.session['user_id'] = select_user.id
                request.session['is_login'] = True
                request.session['user_role'] = select_user.user_role
                request.session['user_email'] = select_user.user_email
                request.session['user_name'] = select_user.user_name
                request.session['user_image'] = select_user.user_image.url
                return redirect('dashboard')
            else:
                msg = "Wrong Password"
        except:
            msg = "Wrong Email"
        
        return render(request,"login.html",{"msg":msg})
    else:
        try:
            if  request.session['is_login']==True:
                return redirect('dashboard')
        except:
            return render(request,"login.html")

def isLogin(request):
     if request.session.get('is_login',False)==False:
         return False
     else:
         return True
        
    
def dashboard(request):
   
    if isLogin(request)==False:
        return redirect('login')
    
    if request.session.get('user_role','none')=="admin":
        return render(request,"dashboard_admin.html")
    elif request.session.get('user_role','none')=="Branch":
        return render(request,"dashboard_principal.html")
    elif request.session.get('user_role','none')=="teacher":
        return render(request,"dashboard_teacher.html")
    elif request.session.get('user_role','none')=="student":
        return render(request,"dashboard_student.html")
    

def logout(request):
    del request.session['user_id']
    del request.session['user_role']
    del request.session['user_email']
    del request.session['user_name']
    del request.session['is_login']
    return redirect('login')

def addbranch(request):

    if request.method=="POST":
        branchid=request.POST['branchid']
        if branchid!="":
            try:
                branch_edit=branch.objects.get(id=branchid)
                branch_edit.branch_name= request.POST['branch_name']
                branch_edit.branch_address= request.POST['branch_address']
            
                id1=branch_edit.user_id_id
                user_edit=users.objects.get(id=id1)
                user_edit.user_name= request.POST['user_name']
                user_edit.user_email= request.POST['user_email']
                try:
                    user_edit.user_image= request.FILES['user_image']
                except:
                    user_edit.user_image = user_edit.user_image
                    
                if request.POST['user_password']!="":
                    user_edit.user_password= make_password(request.POST['user_password'])
                branch_edit.save()
                user_edit.save()
                
                return JsonResponse({'success':True})
            except:
                return JsonResponse({'success':False})
        else:
            try:
                user_image1 = request.FILES['user_image']
            except:
                user_image1 = "profile/default_img.jpg"
            try:
                users.objects.create(
                    user_role = "Branch",
                    user_name = request.POST['user_name'],
                    user_email = request.POST['user_email'],
                    user_password = make_password(request.POST['user_password']),
                    user_image = user_image1
                )
            except:
                pass

            user_id1 = users.objects.latest('id')
            branch.objects.create(
                user_id = user_id1,
                branch_name = request.POST['branch_name'],
                branch_address = request.POST['branch_address']   
            )
            return JsonResponse({'success':True})

    else:
        all_branch = branch.objects.all()
        return render(request,"branch.html",{"all_branch":all_branch})


def editBranch(request):
    branchid = request.POST['id']
    selectbranch=branch.objects.get(id=branchid)
    all_branch = branch.objects.all()
    return render(request,"ajax_form_editbranch.html",{"selectbranch":selectbranch,"all_branch":all_branch,"isedit":1})

def deleteBranch(request):
    branchid = request.POST['id']
    selectbranch=branch.objects.get(id=branchid)
    id1 = selectbranch.user_id_id
    selectuser=users.objects.get(id=id1)
    selectuser.delete()
    selectbranch.delete()
    
    return JsonResponse({'success':True})

def forgotPassword(request):
    if request.method=="POST":
        if request.POST['action'] == 'email':
            email = request.POST['email']
            try:
                select_user = users.objects.get(user_email=email)
                global otp
                global cemail
                otp=random.randint(100000,900000)
                cemail = select_user.user_email
                subject = 'Forgot Password'
                message = f'Your OTP IS : {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [select_user.user_email, ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,"forgot-password.html",{"page":"otp"})
            except:
                msg = "Email Not Found";
                return render(request,"forgot-password.html",{"msg":msg,"page":"email"})
        elif request.POST['action'] == 'otp':
            eotp = int(request.POST['eotp'])
            if eotp==otp:
                return render(request,"forgot-password.html",{"page":"password"})
            else:
                msg = "Wrong OTP"
                return render(request,"forgot-password.html",{"msg":eotp,"page":"otp"})
        elif request.POST['action'] == 'password':
            npassword = request.POST['npassword']
            cpassword = request.POST['cpassword']
            if npassword == cpassword:
                select_user = users.objects.get(user_email=cemail)
                select_user.user_password=make_password(npassword)
                select_user.save1()
                return redirect('login')
            else:
                msg = "New password and confirm Password does not match"
                return render(request,"forgot-password.html",{"msg":msg,"page":"password"})
    else:    
        return render(request,"forgot-password.html",{"page":"email"})
