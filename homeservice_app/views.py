from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
from homeservice_app.forms import Login_form, register_form, register_form1, FeedbackForm, ScheduleForm, work_form, AddBill, CreditCard_form
from homeservice_app.models import register, Login, register1, Complaints, schedule_add, work, Take_appointment, Bill, CreditCard

@login_required(login_url='loginpage')
def home(request):
    return render(request,"home.html")

def index(request):
    return render(request,"index.html")

@login_required(login_url='loginpage')
def index1(request):
    return render(request,"index1.html")

def loginpage(request):
    if request.method=="POST":
        username=request.POST.get("uname")
        password=request.POST.get("pass")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_staff:
                return redirect("base")
            if user.is_customer:
                return redirect("customerbase")
            if user.is_workers:
                return redirect("workerbase")
        else:
            messages.info(request,"no user found")

    return render(request,"login.html")
#################admin#########################


@login_required(login_url='loginpage')
def adminbase(request):
    return render(request,"admin/admin base.html")



@login_required(login_url='loginpage')
def feedbacks(request):
    n = Complaints.objects.all()
    return render(request,"admin/feedbacks.html",{"feedbacks":n})

#this is admin view feedback data

@login_required(login_url='loginpage')
def reply_feedback(request,id):
    feedback = Complaints.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('reply')
        feedback.reply = r
        feedback.save()
        messages.info(request, 'reply send for complaints')
        return redirect('feedbacks')
    return render(request,'admin/reply_feedback.html',{'feedback':feedback})

#this is the reply given by admin to customer

@login_required(login_url='loginpage')
def view_schedule(request):
    n = schedule_add.objects.all()
    return render(request, "admin/view_schedule.html",{"view_schedule":n})

#this is for admin to view schedules of workers

@login_required(login_url='loginpage')
def work_add(request):
    form = work_form()
    if request.method=='POST':
        form=work_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect("work_view")
    return render(request,'admin/work_add.html',{'form':form})

#this is for admin to add diffrent types of work so it willn come in the dropdown menu in worker registration form so they can select it


@login_required(login_url='loginpage')
def work_view(request):
    data=work.objects.all()
    return render(request,'admin/work_view.html',{'data':data})

#this is for admin to view different types of work he added and its amount


@login_required(login_url='loginpage')
@login_required(login_url='loginpage')
def delete_work_view(request,id):
    wn = work.objects.get(id=id)
    wn.delete()
    return redirect("work_view")

#this is for delete work


@login_required(login_url='loginpage')
def update_work_view(request,id):
    a = work.objects.get(id=id)
    form = work_form(instance=a)
    if request.method == 'POST':
        form = work_form(request.POST,instance=a)
        if form.is_valid():
            form.save()
            return redirect('work_view')

    return render(request,'admin/update_work_view.html',{'form':form})

#this is to update work

@login_required(login_url='loginpage')
def admin_view_appointment(request):
    a = Take_appointment.objects.all
    return render(request,"admin/admin_view_appointment.html",{"app":a})

#this is for admin to see the appointment status of worker

@login_required(login_url='loginpage')
def approve_appointment(request, id):
    n = Take_appointment.objects.get(id=id)
    n.status = 1
    n.save()
    messages.info(request, 'Appointment confirmed')
    return redirect('admin_view_appointment')

#this is for admin approve appointment

@login_required(login_url='loginpage')
def reject_appointment(request, id):
    n = Take_appointment.objects.get(id=id)
    n.status = 2
    n.save()
    messages.info(request, 'Appointment Rejected')
    return redirect('admin_view_appointment')

#this is admin reject appointment


@login_required(login_url='loginpage')
def bill(request):
    form = AddBill()
    if request.method == 'POST':
        form = AddBill(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_bill')

    return render(request,'admin/generate_bill.html', {'form': form})

#this is for admin to generate bill for customer

@login_required(login_url='loginpage')
def view_bill(request):
    bill = Bill.objects.all()
    print(bill)
    return render(request, 'admin/view_payment_details.html', {'bill': bill})

#admin to view the payment details of customer

#customer data


@login_required(login_url='loginpage')
def delete_it(request,id):
    wm=register1.objects.get(id=id)
    wm.delete()
    return redirect("customer_data")

#this is to delete the customer data

#workers data




@login_required(login_url='loginpage')
def update(request,id):
    homeservice = register.objects.get(id=id)
    form = register_form(instance=homeservice)
    if request.method == 'POST':
        form =register_form(request.POST,request.FILES,instance=homeservice)
        if form.is_valid():
            form.save()
            return redirect('workers_data')

    return render(request,'admin/update.html',{'form':form})

#this to update workers data
















##########################customer##################################



def customer_registration(request):
    form1 = Login_form()
    form2 =register_form1()
    if request.method =="POST":
        form1 = Login_form(request.POST)
        form2 = register_form1(request.POST,request.FILES)

        if form1.is_valid() and form2.is_valid():
            a = form1.save(commit=False)
            a.is_customer = True
            a.save()
            user1 = form2.save(commit=False)
            user1.user = a
            user1.save()
            return redirect('loginpage')

    return render(request,"customer/customers.html",{'form1': form1,'form2':form2})

#this is for customer registration



@login_required(login_url='loginpage')
def feedback(request):
    form = FeedbackForm()
    u = request.user
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            return redirect("view")

    return render(request,'customer/feedback.html',{"form":form})

#this is feedback form for customer to write their feedbacks

@login_required(login_url='loginpage')
def view(request):
    data = Complaints.objects.filter(user=request.user)
    print(data)
    return render(request, "customer/view.html", {"data": data})

#this is to view the reply given by admin for the feedbacks of customer


#delete feedback

@login_required(login_url='loginpage')
def delete_schedule(request,id):
    wn = schedule_add.objects.get(id=id)
    wn.delete()
    return redirect("worker_view_schedule")

#this is to delete schedule



@login_required(login_url='loginpage')
def customer_view_schedule(request):
    n = schedule_add.objects.all()
    return render(request, "customer/customer_view_schedule.html",{"customer_view_schedule":n})

#this is  to view the schedule given by worker

@login_required(login_url='loginpage')
def view_workers(request):
    data = register.objects.all()
    return render(request,"customer/view_workers.html",{"data":data})

#this is for customer view  the worker


@login_required(login_url='loginpage')
def take_appointment(request,id):
    s = schedule_add.objects.get(id=id)
    c = register1.objects.get(user=request.user)
    app = Take_appointment.objects.filter(user=c,schedule=s)
    if app.exists():
        messages.info(request,"already booked")
        return redirect('customer_view_schedule')
    else:
        if request.method == 'POST':
            obj = Take_appointment()
            obj.user = c
            obj.schedule = s
            obj.save()
            messages.info(request,"appointment is successfully booked")
            return redirect('view_appointment')
    return render(request,"customer/take_appointment.html",{"s":s})

#this is for customer to see the appointment status of the worker

@login_required(login_url='loginpage')
def view_appointment(request):
    # c = register1.objects.get(user=request.user)
    a = Take_appointment.objects.all
    return render(request,"customer/view_appointment.html",{"app":a})

#this is for customer to see the appointment status of the worker




@login_required(login_url='loginpage')
def customer_view_payment(request):
    u = register1.objects.get(user =request.user)
    a = Bill.objects.filter(name=u)
    return render(request, 'customer/customer_view_payment.html',{'a':a})

#this is for customer to view the payment details



@login_required(login_url='loginpage')
def CreditCard_add (request):
    form = CreditCard_form()
    if request.method == 'POST':
        form = CreditCard_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_creditcard')

    return render(request,'customer/creditcard_add.html', {'form': form})

#this is for credit card payment for customer

@login_required(login_url='loginpage')
def view_creditcard(request):
    a = CreditCard.objects.all()
    print(a)
    return render(request, 'customer/view_creditcard.html', {'a': a})

#this is to view credit card details



@login_required(login_url='loginpage')
def pay_bill(request, id):
    bi = Bill.objects.get(id=id)
    form = AddBill()
    if request.method =='POST':
        card = request.POST.get('card')
        c = request.POST.get('cvv')
        da = request.POST.get('exp')
        CreditCard(card_no=card, card_cvv=c, expiry_date=da).save
        bi.status = 1
        bi.save()
        messages.info(request, 'Bill paid successfully')
        return redirect('view_bill')
    return render(request,'customer/pay_bill.html',)

#this is for customer to pay the bill



@login_required(login_url='loginpage')
def pay_in_direct(request, id):
    bi = Bill.objects.get(id=id)
    bi.status = 2
    bi.save()
    messages.info(request, 'choosed to pay fee direct in office')
    return redirect('bill_history')

#this is for customer to pay in direct


@login_required(login_url='loginpage')
def bill_history(request):
    u = register1.objects.get(user=request.user)
    bill =Bill.objects.filter(name=u,status__in=[1,2])

    return render(request, 'customer/customer_view_bill_history.html',{'bill':bill})

#this is for customer to see the bill history only for he/she paid


@login_required(login_url='loginpage')
def del_feedback(request,id):
    wm = Complaints.objects.get(id=id)
    wm.delete()
    return redirect("view")

# here customer can delete feedback















#############################################worker###################################################

@login_required(login_url='loginpage')
def workers(request):
    return render(request,"worker/workers.html")

@login_required(login_url='loginpage')
def workerbase(request):
    return render(request,"worker/worker base.html")

#this the dashborde of worker


def workers_registration(request):
    form1 = Login_form()
    form2 =register_form()
    if request.method =="POST":
        form1 = Login_form(request.POST)
        form2 = register_form(request.POST,request.FILES)

        if form1.is_valid() and form2.is_valid():
            a = form1.save(commit=False)
            a.is_workers = True
            a.save()
            user1 = form2.save(commit=False)
            user1.user = a
            user1.save()
            return redirect('loginpage')
    return render(request,"worker/workers.html",{'form1': form1,'form2':form2})

#this is for worker registration



@login_required(login_url='loginpage')
def schedule(request):
    form = ScheduleForm()
    # u = request.user
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.worker=register.objects.get(user=request.user)
            obj.save()
            return redirect("worker_view_schedule")

    return render(request, "worker/schedule.html",{"form": form})

#this is used to add schedules of worker

@login_required(login_url='loginpage')
def worker_view_schedule(request):
    n = schedule_add.objects.all()
    return render(request, "worker/worker_view_schedule.html",{"worker_view_schedule":n})


#(workerupdate)




@login_required(login_url='loginpage')
def workers_data(request):
    data=register.objects.all
    print(data)
    return render(request,"worker/workers_data.html",{"data":data})


@login_required(login_url='loginpage')
def delete(request,id):
    wm=register.objects.get(id=id)
    wm.delete()
    return redirect("workers_data")





@login_required(login_url='loginpage')
def registration(request):
    return render(request,"registration.html")

@login_required(login_url='loginpage')
def reg1(request):
    return render(request,"reg1.html")


@login_required(login_url='loginpage')
def customers(request):
    return render(request,"customers.html")


@login_required(login_url='loginpage')
def workers_data(request):
    data=register.objects.all
    print(data)
    return render(request,"worker/workers_data.html",{"data":data})


@login_required(login_url='loginpage')
def workers1(request):
    return render(request,"workers1.html")



@login_required(login_url='loginpage')
def customerbase(request):
    return render(request,"customer/customer base.html")



@login_required(login_url='loginpage')
def customer_data(request):
    data=register1.objects.all
    print(data)
    return render(request,"customer/customer_data.html",{"data":data})














@login_required(login_url='loginpage')
def worker_workerdata(request):
    data=register.objects.all
    print(data)
    return render(request,"worker/worker_workerdata.html",{"data": data})



























@login_required(login_url='loginpage')
def worker_view_appointment(request):
    c = request.user.id
    print(c)
    s = Take_appointment.objects.filter(schedule__worker__user =c)
    print(s)

    return render(request,"worker/worker_view_appointment.html",{"b":s})

def logout_view(request):
    logout(request)
    return redirect("loginpage")