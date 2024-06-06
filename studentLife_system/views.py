from time import localtime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import studentInfo, RequestedGMC, equipment, Schedule
from .models import (
    studentInfo,
    RequestedGMC,
    equipment,
    Schedule,
    Program,
    Project,
    MOD,
    QrDonation,
)
from .models import Alumni, graduateForm, Event, JobFair, Yearbook
from django.utils import timezone
from django.db.models import Avg
from django.core.mail import send_mail, BadHeaderError
import socket
import json
from django.contrib.auth.decorators import login_required

import csv
from datetime import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import (
    CounselingSchedulerForm,
    IndividualProfileForm,
    FileUpload,
    UploadFileForm,
    ExitInterviewForm,
    OjtAssessmentForm,
)
from .models import (
    TestArray,
    studentInfo,
    counseling_schedule,
    exit_interview_db,
    OjtAssessment,
    IndividualProfileBasicInfo,
    IntakeInverView,
    GuidanceTransaction,
)
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template.defaulttags import register
from django.core.mail import send_mail
from django.http import HttpResponse
import calendar
from django.utils import timezone
from .reportpdf import html2pdf
from xhtml2pdf import pisa
from django.template.loader import get_template

# Create your views here.


# Student
def home(request):
    user = request.user.is_staff
    return render(
        request,
        "studentLife/main.html",
        {"user": user},
    )


# Admin
def adminhome(request):
    return render(request, "adminUser/adminmain.html")


def adminGmc(request):
    return render(request, "adminUser/adminRequestedGmc.html")


def gmcform(request):
    return render(request, "adminUser/gmcform.html")


def equipmentTracker(request):
    return render(request, "studentLife/equipmentTracker.html")


# Request for GoodMoral Certificate Student Side


def adminGmc(request):
    return render(request, "adminUser/adminRequestedGmc.html")


def gmcform(request):
    return render(request, "adminUser/gmcform.html")


def equipmentTracker(request):
    return render(request, "studentLife/equipmentTracker.html")


# Request for GoodMoral Certificate Student Side
def requestgmc(request):
    student = None

    if request.method == "GET" and "searchID" in request.GET:
        student_id = request.GET.get("searchID")
        if student_id:
            if student_id.isdigit():
                try:
                    student = studentInfo.objects.get(studID=student_id)
                except studentInfo.DoesNotExist:
                    student = None
                    messages.error(request, "Student not found")
            else:
                messages.error(request, "Student ID must be numeric")

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        reason = request.POST.get("reason")
        if student_id and reason:
            if student_id.isdigit():
                try:
                    student = studentInfo.objects.get(studID=student_id)
                    RequestedGMC.objects.create(student=student, reason=reason)
                    messages.success(
                        request, "Good Moral Certificate request submitted successfully"
                    )
                    return redirect("requestgmc")
                    messages.success(
                        request, "Good Moral Certificate request submitted successfully"
                    )
                    return redirect("requestgmc")
                except studentInfo.DoesNotExist:
                    messages.error(request, "Student not found")
            else:
                messages.error(request, "Student ID must be numeric")

    context = {"student": student}
    return render(request, "studentLife/requestgmc.html", context)


# Processing Goodmoral Certificate Admin side
def adminRequestedGmc(request):
    gmc_requests = RequestedGMC.objects.filter(processed=False)
    context = {"gmc_requests": gmc_requests}
    return render(request, "adminUser/adminRequestedGmc.html", context)


# Making of Goodmoral Certificate
def generateGmc(request, request_id):
    try:
        gmc_request = RequestedGMC.objects.get(id=request_id)
        student = gmc_request.student

        or_num = request.GET.get(
            "ornum", ""
        )  # Capture the OR Number from the query parameters
        or_num = request.GET.get(
            "ornum", ""
        )  # Capture the OR Number from the query parameters

        # Mark the request as processed
        gmc_request.or_num = or_num
        gmc_request.processed = True
        gmc_request.save()

        context = {
            "student_name": f"{student.firstname} {student.lastname}",
            "student_degree": student.degree,
            "request_date": localtime(gmc_request.request_date).strftime("%B %d, %Y"),
            "reason": gmc_request.reason,
            "today_date": localtime(now()).strftime("%B %d, %Y"),
            "or_num": or_num,  # Include the OR Number in the context
        }
        return render(request, "adminUser/good_moral_certificate.html", context)
    except RequestedGMC.DoesNotExist:
        messages.error(request, "GMC Request not found")
        return redirect("adminRequestedGmc")


# Calendar Of Activities Student Side
def monthlyCalendar(request):
    schedules = Schedule.objects.all()
    sched_res = {}
    user = request.user.is_staff

    for schedule in schedules:
        sched_res[schedule.sched_Id] = {
            "id": schedule.sched_Id,
            "title": schedule.title,
            "description": schedule.description,
            "start_datetime": schedule.start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "end_datetime": schedule.end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "sdate": schedule.start_datetime.strftime("%B %d, %Y %I:%M %p"),
            "edate": schedule.end_datetime.strftime("%B %d, %Y %I:%M %p"),
        }

    context = {"sched_json": json.dumps(sched_res), "user": user}
    return render(request, "studentLife/monthlyCalendar.html", context)


# Calendar of Activities Admin
def monthlyCalendarAdmin(request):
    schedules = Schedule.objects.all()
    sched_res = {}

    for schedule in schedules:
        sched_res[schedule.sched_Id] = {
            "id": schedule.sched_Id,
            "title": schedule.title,
            "description": schedule.description,
            "start_datetime": schedule.start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "end_datetime": schedule.end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "sdate": schedule.start_datetime.strftime("%B %d, %Y %I:%M %p"),
            "edate": schedule.end_datetime.strftime("%B %d, %Y %I:%M %p"),
        }

    context = {"sched_json": json.dumps(sched_res)}
    return render(request, "adminUser/monthlyCalendarAdmin.html", context)


# Save Schedule
def save_schedule(request):
    if request.method == "POST":
        schedule_id = request.POST.get("id")
        if schedule_id:
            schedule = get_object_or_404(Schedule, pk=schedule_id)
            form = ScheduleForm(request.POST, instance=schedule)
        else:
            form = ScheduleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("monthlyCalendarAdmin")
    else:
        form = ScheduleForm()
    return render(request, "adminUser/monthlyCalendarAdmin.html", {"form": form})


# Delete Schedule
def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    schedule.delete()
    return redirect("monthlyCalendarAdmin")


def equipmentTrackerAdmin(request):
    student = None
    user = request.user.is_staff
    if request.method == "GET" and "search" in request.GET:
        search_id = request.GET.get("search")
        if search_id:
            try:
                student = studentInfo.objects.get(studID=search_id)
            except studentInfo.DoesNotExist:
                messages.error(request, "Student not found")

    all_equipment = equipment.objects.all()

    context = {"student": student, "all_equipment": all_equipment, "user": user}
    return render(request, "adminUser/equipmentTrackerAdmin.html", context)


# Add Equipment
def addEquipment(request):
    if request.method == "POST":
        equipment_name = request.POST.get("equipmentname")
        serial = request.POST.get("serialnum")
        if equipment_name:
            new_equipment = equipment(equipmentName=equipment_name, equipmentSN=serial)
            new_equipment.save()
            messages.success(request, "Equipment added successfully")

            return redirect("addEquipment")
        else:
            messages.error(request, "Both fields are required")

    # Fetch all equipment objects from the database
    all_equipment = equipment.objects.all()

    # Pass the equipment objects to the template context

    return render(
        request, "adminUser/addEquipment.html", {"all_equipment": all_equipment}
    )


def idRequest(request):
    return render(request, "alumni/users/id_alumni.html")


def search_id(request):
    if request.method == "GET":
        student_id = request.GET.get("student_id")
        if student_id:
            try:
                student_obj = studentInfo.objects.get(studID=student_id)
                return render(
                    request, "alumni/users/id_alumni.html", {"student": student_obj}
                )
            except studentInfo.DoesNotExist:

                messages.error(request, "No student found with the provided ID.")
                return render(request, "alumni/users/id_alumni.html")
        else:

            messages.error(request, "Please provide a student ID.")
            return render(request, "alumni/users/id_alumni.html")
    else:

        return render(request, "alumni/users/id_alumni.html")


def add_alumni(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        email_add = request.POST.get("email_add")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        alumnidate = request.POST.get("alumnidate")
        alumnibirthday = request.POST.get("alumnibirthday")
        alumnicontact = request.POST.get("alumnicontact")
        sssgsis = request.POST.get("sssgsis")
        tin = request.POST.get("tin")
        parentguardian = request.POST.get("parentguardian")
        alumniaddress = request.POST.get("alumniaddress")
        degree = request.POST.get("degree")
        sex = request.POST.get("sex")

        if Alumni.objects.filter(student__studID=student_id).exists():
            messages.error(request, f"You already requested Alumni ID!")
            return redirect("idRequest")

        student = get_object_or_404(studentInfo, studID=student_id)
        alumni = Alumni.objects.create(
            student=student,
            firstname=firstname,
            lastname=lastname,
            alumnidate=alumnidate,
            alumnibirthday=alumnibirthday,
            alumnicontact=alumnicontact,
            sssgsis=sssgsis,
            tin=tin,
            parentguardian=parentguardian,
            alumniaddress=alumniaddress,
            email_add=email_add,
            degree=degree,
            sex=sex,
        )
        alumni_id = alumni.alumniID

        messages.success(
            request,
            f"Your request is successful! Your alumni ID requested is {alumni_id}",
        )

        return redirect("idRequest")
    else:
        return redirect("idRequest")


def graduateTracer(request):
    return render(request, "alumni/users/graduateTracer.html")


def search_id2(request):
    if request.method == "GET":
        student_id = request.GET.get("student_id")
        if student_id:
            try:

                alumni_obj = Alumni.objects.get(student__studID=student_id)

                if graduateForm.objects.filter(student__studID=student_id).exists():
                    messages.error(request, "You have already filled out this form.")
                    return render(request, "alumni/users/graduateTracer.html")

                return render(
                    request, "alumni/users/graduateTracer.html", {"alumni": alumni_obj}
                )
            except Alumni.DoesNotExist:
                messages.error(request, "Not Found! Please request first for alumni ID")
                return render(request, "alumni/users/graduateTracer.html")
        else:
            messages.error(request, "Please provide a student ID.")
            return render(request, "alumni/users/graduateTracer.html")
    else:
        return render(request, "alumni/users/graduateTracer.html")


def graduateTracer_submit(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        degree = request.POST.get("degree")
        email_add = request.POST.get("email_add")
        contactnum = request.POST.get("contactnum")
        sex = request.POST.get("sex")
        alumniaddress = request.POST.get("alumniaddress")
        dategraduated = request.POST.get("dategraduated")
        nameoforganization = request.POST.get("nameoforganization")
        employmenttype = request.POST.get("employmentype")
        occupationalClass = request.POST.get("occupationalClass")
        gradscholrelated = request.POST.get("gradscholrelated")
        yearscompany = request.POST.get("yearscompany")
        placework = request.POST.get("placework")
        firstjobgraduate = request.POST.get("firstjobgraduate")
        reasonstayingjob = request.POST.get("reasonstayingjob")
        designation = request.POST.get("designation")
        status = request.POST.get("status")
        monthlyincome = request.POST.get("monthlyincome")
        workwhileworking = request.POST.get("workwhileworking")
        ifnotworking = request.POST.get("ifnotworking")
        reasontimegap = request.POST.get("reasontimegap")
        natureemployment = request.POST.get("natureemployment")
        numberofyears = request.POST.get("numberofyears")
        monthlyincome2 = request.POST.get("monthlyincome2")
        academicprofession = request.POST.get("academicprofession")
        researchcapability = request.POST.get("researchcapability")
        learningefficiency = request.POST.get("learningefficiency")
        peopleskills = request.POST.get("peopleskills")
        problemsolvingskills = request.POST.get("problemsolvingskills")
        informationtechnologyskills = request.POST.get("informationtechnologyskills")
        meetingprofessionalneeds = request.POST.get("meetingprofessionalneeds")
        communityfield = request.POST.get("communityfield")
        globalfield = request.POST.get("globalfield")
        criticalskills = request.POST.get("criticalskills")
        rangeofcourses = request.POST.get("rangeofcourses")
        relevanceprofession = request.POST.get("relevanceprofession")
        extracurricular = request.POST.get("extracurricular")
        premiumresearch = request.POST.get("premiumresearch")
        interlearning = request.POST.get("interlearning")
        teachingenvironment = request.POST.get("teachingenvironment")
        qualityinstruction = request.POST.get("qualityinstruction")
        teachrelationship = request.POST.get("teachrelationship")
        libraryresources = request.POST.get("libraryresources")
        labresources = request.POST.get("labresources")
        classize = request.POST.get("classize")
        profexpertise = request.POST.get("profexpertise")
        profsubjectmatter = request.POST.get("profsubjectmatter")
        enrollmentdate = request.POST.get("enrollmentdate")
        studiesdegree = request.POST.get("studiesdegree")
        universityinstitution = request.POST.get("universityinstitution")
        studiesAddress = request.POST.get("studiesAddress")
        pursuingstudies = request.POST.get("pursuingstudies")
        department = request.POST.get("department")
        salaryimprovement = request.POST.get("salaryimprovement")
        opportunitiesabroad = request.POST.get("opportunitiesabroad")
        personalitydevelopment = request.POST.get("personalitydevelopment")
        technologiesvaluesformation = request.POST.get("technologiesvaluesformation")
        try:
            student = get_object_or_404(studentInfo, studID=student_id)
        except:
            messages.error(request, "Student ID not found.")
            return redirect("graduateTracer")

        try:
            alumni = get_object_or_404(Alumni, student=student)
        except:
            messages.error(request, "No Alumni matches the given query.")
            return redirect("graduateTracer")
        gradform = graduateForm.objects.create(
            alumniID=alumni,
            student=student,
            degree=degree,
            email_add=email_add,
            contactnum=contactnum,
            sex=sex,
            firstname=firstname,
            lastname=lastname,
            alumniaddress=alumniaddress,
            dategraduated=dategraduated,
            nameoforganization=nameoforganization,
            employmenttype=employmenttype,
            occupationalClass=occupationalClass,
            gradscholrelated=gradscholrelated,
            yearscompany=yearscompany,
            placework=placework,
            firstjobgraduate=firstjobgraduate,
            reasonstayingjob=reasonstayingjob,
            designation=designation,
            status=status,
            monthlyincome=monthlyincome,
            workwhileworking=workwhileworking,
            ifnotworking=ifnotworking,
            reasontimegap=reasontimegap,
            numberofyears=numberofyears,
            monthlyincome2=monthlyincome2,
            academicprofession=academicprofession,
            researchcapability=researchcapability,
            learningefficiency=learningefficiency,
            peopleskills=peopleskills,
            problemsolvingskills=problemsolvingskills,
            informationtechnologyskills=informationtechnologyskills,
            communityfield=communityfield,
            globalfield=globalfield,
            criticalskills=criticalskills,
            rangeofcourses=rangeofcourses,
            relevanceprofession=relevanceprofession,
            extracurricular=extracurricular,
            premiumresearch=premiumresearch,
            interlearning=interlearning,
            teachingenvironment=teachingenvironment,
            qualityinstruction=qualityinstruction,
            teachrelationship=teachrelationship,
            libraryresources=libraryresources,
            labresources=labresources,
            classize=classize,
            profexpertise=profexpertise,
            profsubjectmatter=profsubjectmatter,
            enrollmentdate=enrollmentdate,
            studiesdegree=studiesdegree,
            universityinstitution=universityinstitution,
            studiesAddress=studiesAddress,
            pursuingstudies=pursuingstudies,
            department=department,
            natureemployment=natureemployment,
            meetingprofessionalneeds=meetingprofessionalneeds,
            salaryimprovement=salaryimprovement,
            opportunitiesabroad=opportunitiesabroad,
            personalitydevelopment=personalitydevelopment,
            technologiesvaluesformation=technologiesvaluesformation,
        )
        alumni_id = alumni.alumniID

        messages.success(
            request, f"Your request is successful! Your alumni ID is {alumni_id}"
        )
        return redirect("graduateTracer")
    else:
        return redirect("graduateTracer")


def alumni_events(request):
    events = Event.objects.all()
    return render(request, "alumni/users/alumni_events.html", {"events": events})


def jobfairs(request):

    job_fairs = JobFair.objects.all()
    return render(request, "alumni/users/jobfairs.html", {"job_fairs": job_fairs})


def yearbook(request):
    return render(request, "alumni/users/yearbook.html")


def search_yearbook(request):
    if request.method == "GET":
        first_name = request.GET.get("yeargetfirstname")
        last_name = request.GET.get("yeargetlastname")

        if first_name and last_name:
            try:

                first_name = first_name.lower()
                last_name = last_name.lower()

                yearbook_entry = Yearbook.objects.get(
                    yearbookFirstname__iexact=first_name,
                    yearbookLastname__iexact=last_name,
                )
                return render(
                    request,
                    "alumni/users/yearbook.html",
                    {"yearbook_entry": yearbook_entry},
                )
            except Yearbook.DoesNotExist:
                return render(
                    request,
                    "alumni/users/yearbook.html",
                    {"error_message": "No yearbook entry found."},
                )
        else:
            return render(
                request,
                "alumni/users/yearbook.html",
                {
                    "error_message": "Please provide both first name and last name in the search."
                },
            )
    else:
        return render(request, "alumni/users/yearbook.html")


def transaction_alumni(request):
    return render(request, "alumni/users/transaction_alumni.html")


def transac_search(request):
    context = {}

    if request.method == "POST":
        transac_choice = request.POST.get("transac_choice")
        transac_frequency = request.POST.get("transac_frequency")

        current_month = timezone.now().month

        # Alumni ID Requests
        if transac_choice == "Alumni ID Requests":
            if transac_frequency == "Monthly":
                alumni_requests = Alumni.objects.filter(alumnidate__month=current_month)
            elif transac_frequency == "Yearly":
                alumni_requests = Alumni.objects.filter(
                    alumnidate__year=timezone.now().year
                )
            else:
                alumni_requests = Alumni.objects.all()

            total_count = alumni_requests.count()
            context = {
                "alumni_requests": alumni_requests,
                "transac_frequency": transac_frequency,
                "total_count": total_count,
                "transac_choice": transac_choice,
            }

        # Graduate Tracer
        elif transac_choice == "Graduate Tracer":
            if transac_frequency == "Monthly":
                graduate_tracer_data = graduateForm.objects.filter(
                    enrollmentdate__month=current_month
                )
            elif transac_frequency == "Yearly":
                graduate_tracer_data = graduateForm.objects.filter(
                    enrollmentdate__year=timezone.now().year
                )
            else:
                graduate_tracer_data = graduateForm.objects.all()

            total_count = graduate_tracer_data.count()
            has_reports = total_count > 0

            # Aggregate weighted means
            weighted_means = {
                "academicprofession": graduate_tracer_data.aggregate(
                    Avg("academicprofession")
                )["academicprofession__avg"],
                "researchcapability": graduate_tracer_data.aggregate(
                    Avg("researchcapability")
                )["researchcapability__avg"],
                "learningefficiency": graduate_tracer_data.aggregate(
                    Avg("learningefficiency")
                )["learningefficiency__avg"],
                "peopleskills": graduate_tracer_data.aggregate(Avg("peopleskills"))[
                    "peopleskills__avg"
                ],
                "problemsolvingskills": graduate_tracer_data.aggregate(
                    Avg("problemsolvingskills")
                )["problemsolvingskills__avg"],
                "informationtechnologyskills": graduate_tracer_data.aggregate(
                    Avg("informationtechnologyskills")
                )["informationtechnologyskills__avg"],
                "meetingprofessionalneeds": graduate_tracer_data.aggregate(
                    Avg("meetingprofessionalneeds")
                )["meetingprofessionalneeds__avg"],
                "communityfield": graduate_tracer_data.aggregate(Avg("communityfield"))[
                    "communityfield__avg"
                ],
                "globalfield": graduate_tracer_data.aggregate(Avg("globalfield"))[
                    "globalfield__avg"
                ],
                "criticalskills": graduate_tracer_data.aggregate(Avg("criticalskills"))[
                    "criticalskills__avg"
                ],
                "salaryimprovement": graduate_tracer_data.aggregate(
                    Avg("salaryimprovement")
                )["salaryimprovement__avg"],
                "opportunitiesabroad": graduate_tracer_data.aggregate(
                    Avg("opportunitiesabroad")
                )["opportunitiesabroad__avg"],
                "personalitydevelopment": graduate_tracer_data.aggregate(
                    Avg("personalitydevelopment")
                )["personalitydevelopment__avg"],
                "technologiesvaluesformation": graduate_tracer_data.aggregate(
                    Avg("technologiesvaluesformation")
                )["technologiesvaluesformation__avg"],
                "rangeofcourses": graduate_tracer_data.aggregate(Avg("rangeofcourses"))[
                    "rangeofcourses__avg"
                ],
                "relevanceprofession": graduate_tracer_data.aggregate(
                    Avg("relevanceprofession")
                )["relevanceprofession__avg"],
                "extracurricular": graduate_tracer_data.aggregate(
                    Avg("extracurricular")
                )["extracurricular__avg"],
                "premiumresearch": graduate_tracer_data.aggregate(
                    Avg("premiumresearch")
                )["premiumresearch__avg"],
                "interlearning": graduate_tracer_data.aggregate(Avg("interlearning"))[
                    "interlearning__avg"
                ],
                "teachingenvironment": graduate_tracer_data.aggregate(
                    Avg("teachingenvironment")
                )["teachingenvironment__avg"],
                "qualityinstruction": graduate_tracer_data.aggregate(
                    Avg("qualityinstruction")
                )["qualityinstruction__avg"],
                "teachrelationship": graduate_tracer_data.aggregate(
                    Avg("teachrelationship")
                )["teachrelationship__avg"],
                "libraryresources": graduate_tracer_data.aggregate(
                    Avg("libraryresources")
                )["libraryresources__avg"],
                "labresources": graduate_tracer_data.aggregate(Avg("labresources"))[
                    "labresources__avg"
                ],
                "classize": graduate_tracer_data.aggregate(Avg("classize"))[
                    "classize__avg"
                ],
                "profexpertise": graduate_tracer_data.aggregate(Avg("profexpertise"))[
                    "profexpertise__avg"
                ],
                "profsubjectmatter": graduate_tracer_data.aggregate(
                    Avg("profsubjectmatter")
                )["profsubjectmatter__avg"],
            }

            context = {
                "graduate_tracer_data": graduate_tracer_data,
                "transac_frequency": transac_frequency,
                "total_count": total_count,
                "transac_choice": transac_choice,
                "weighted_means": weighted_means,
                "has_reports": has_reports,
            }

    return render(request, "alumni/users/transaction_alumni.html", context)


# admin alumni
def admin_id_request(request):
    alumni_requests = Alumni.objects.all()
    return render(
        request,
        "alumni/users/admin_idRequest.html",
        {"alumni_requests": alumni_requests},
    )


def approve_alumni_request(request, alumni_id):
    if request.method == "POST":
        alumni = get_object_or_404(Alumni, pk=alumni_id)
        email_add = alumni.email_add

        try:
            send_mail(
                "Alumni ID Request Approved",
                f"Hello {alumni.firstname} {alumni.lastname},\n\nYour alumni ID request has been approved. Your ID is ready to claim.\n\nThank you!",
                "alumni_ctuac@ctu.edu.ph",
                [email_add],
                fail_silently=False,
            )
            alumni.approved = True  # Mark as approved
            alumni.save()

        except (socket.error, BadHeaderError) as e:
            messages.error(request, f"Error sending email: {e}")

        return redirect("admin_idRequest")

    return redirect("admin_idRequest")


def claim_alumni_id(request, alumni_id):
    if request.method == "POST":
        alumni = get_object_or_404(Alumni, pk=alumni_id)
        alumni.claimed_date = timezone.now()
        alumni.save()
        return redirect("admin_idRequest")

    return redirect("admin_idRequest")


def admin_gradTracer(request):
    graduate_requests = graduateForm.objects.select_related("alumniID").all()
    return render(
        request,
        "alumni/users/admin_gradTracer.html",
        {"graduate_requests": graduate_requests},
    )


def admin_events(request):
    if request.method == "POST":

        eventsName = request.POST.get("eventsName")
        eventsDate = request.POST.get("eventsDate")
        eventsLocation = request.POST.get("eventsLocation")
        eventsDescription = request.POST.get("eventsDescription")
        eventsImage = request.FILES.get("eventsImage")

        event = Event.objects.create(
            eventsName=eventsName,
            eventsDate=eventsDate,
            eventsLocation=eventsLocation,
            eventsDescription=eventsDescription,
            eventsImage=eventsImage,
        )
        messages.success(request, "Successfully Added!")

        return redirect("admin_events")

    return render(request, "alumni/users/admin_events.html")


def admin_jobfairs(request):
    if request.method == "POST":

        jobtitle = request.POST.get("jobtitle")
        companyname = request.POST.get("companyname")
        joblocation = request.POST.get("joblocation")
        jobsalary = request.POST.get("jobsalary")
        employmenttype = request.POST.get("employmenttype")
        jobdescription = request.POST.get("jobdescription")

        jobfair = JobFair.objects.create(
            jobtitle=jobtitle,
            companyname=companyname,
            joblocation=joblocation,
            jobsalary=jobsalary,
            employmenttype=employmenttype,
            jobdescription=jobdescription,
        )

        messages.success(request, "Successfully Added!")
        return redirect("admin_jobfairs")

    return render(request, "alumni/users/admin_jobfairs.html")


def admin_yearbook(request):
    if request.method == "POST":
        yearbookFirstname = request.POST.get("yearfirstname")
        yearbookLastname = request.POST.get("yearlastname")
        yearbookAddress = request.POST.get("yearaddress")
        yearbookCourse = request.POST.get("yearcourse")
        yearbookImage = request.FILES.get("yearImage")
        yearbookGender = request.POST.get("yeargender")
        yearbookYearGrad = request.POST.get("yeargraduated")

        # Check if an entry with the same first name and last name already exists
        if Yearbook.objects.filter(
            yearbookFirstname=yearbookFirstname, yearbookLastname=yearbookLastname
        ).exists():
            messages.error(request, "An entry with this name already exists.")
        else:
            yearbook_entry = Yearbook.objects.create(
                yearbookFirstname=yearbookFirstname,
                yearbookLastname=yearbookLastname,
                yearbookAddress=yearbookAddress,
                yearbookCourse=yearbookCourse,
                yearbookImage=yearbookImage,
                yearbookGender=yearbookGender,
                yearbookYearGrad=yearbookYearGrad,
            )
            messages.success(request, "Successfully Added!")

        return redirect("admin_yearbook")

    return render(request, "alumni/users/admin_yearbook.html")
    return render(
        request, "adminUser/addEquipment.html", {"all_equipment": all_equipment}
    )


# COMMUNITY INVOLVEMENT


def programs(request):
    loadProgram = Program.objects.filter(archive=False).order_by("-date_time")
    user = request.user.is_staff

    return render(
        request,
        "community_involvement/programs.html",
        {
            "url": "programs",
            "title": "Programs",
            "loadPrograms": loadProgram,
            "user": user,
        },
    )


def projects(request):
    loadProjects = Project.objects.filter(archive=False).order_by("-date_time")
    qrCodeID = QrDonation.objects.all()

    user = request.user.is_staff

    return render(
        request,
        "community_involvement/projects.html",
        {
            "url": "projects",
            "title": "Projects",
            "loadProjects": loadProjects,
            "user": user,
            "qrCodeID": qrCodeID,
        },
    )


@login_required(login_url="home")
def program_form(request):
    user = request.user.is_staff
    return render(
        request,
        "community_involvement/admin/programs-forms.html",
        {
            "url": "program-form",
            "user": user,
        },
    )


@login_required(login_url="home")
def project_form(request):
    user = request.user.is_staff
    return render(
        request,
        "community_involvement/admin/projects-forms.html",
        {
            "url": "project-form",
            "user": user,
        },
    )


def add_program(request):
    if request.method == "POST":
        Program(request.POST)

        title = request.POST.get("title")
        caption = request.POST.get("caption")
        image_upload = request.FILES.getlist("images")

        for image in image_upload:
            program = Program(
                title=title,
                caption=caption,
                image_upload=image,
            )
            program.save()

    return redirect("program-form")


def add_project(request):
    if request.method == "POST":
        Project(request.POST)

        title = request.POST.get("title")
        caption = request.POST.get("caption")
        image_upload = request.FILES.getlist("images")

        for image in image_upload:
            project = Project(
                title=title,
                caption=caption,
                image_upload=image,
            )
            project.save()

    return redirect("project-form")


def gcash_mode(request):
    if request.method == "POST":
        MOD(request.POST)

        donated = request.POST["title"]
        name = request.POST["name"]
        gcash_number = request.POST["gcash_number"]
        amount = request.POST["amount"]
        image_details = request.FILES.getlist("images")

        for image in image_details:

            donation = MOD(
                donation_type="GCash",
                donated=donated,
                name=name,
                gcash_number=gcash_number,
                amount=amount,
                image_details=image,
            )

            donation.save()

    return redirect("projects")


def gcash_mode_admin(request, id):
    qr = request.FILES.getlist("images")

    for image in qr:
        if int(QrDonation.objects.count()) == 0:
            qrCode = QrDonation(gcash=image)

        else:
            qrCode = QrDonation.objects.get(qr_id=id)
            qrCode.gcash = image

        qrCode.save()

    return redirect("projects")

def bank_mode(request):
    if request.method == "POST":
        MOD(request.POST)

        donated = request.POST["title"]
        name = request.POST["name"]
        bank_card = request.POST["banks"]
        bank_number = request.POST["bank_number"]
        amount = request.POST["amount"]
        image_details = request.FILES.getlist("images")

        for image in image_details:

            donation = MOD(
                donation_type="Bank",
                donated=donated,
                name=name,
                bank_number=bank_number,
                bank_card=bank_card,
                amount=amount,
                image_details=image,
            )

            donation.save()

    return redirect("projects")

def bank_mode_admin(request, id):
    qr = request.FILES.getlist("images")
    banks = request.POST.get('banks')

    for image in qr:
        if int(QrDonation.objects.count()) == 0:
            if banks == "BPI":
                qrCode = QrDonation(bpi=image)
            
            if banks == "BDO":
                qrCode = QrDonation(bdo=image)

            if banks == "LANDBACK":
                qrCode = QrDonation(landbank=image)
            
            if banks == "PNB":
                qrCode = QrDonation(pnb=image)
            
            if banks == "METRO BANK":
                qrCode = QrDonation(metro=image)
            
            if banks == "UNION BANK":
                qrCode = QrDonation(union=image)
            
            if banks == "CHINA BANK":
                qrCode = QrDonation(china=image)

        else:
            qrCode = QrDonation.objects.get(qr_id=id)

            if banks == "BPI":
                qrCode.bpi = image
            
            if banks == "BDO":
                qrCode.bdo = image

            if banks == "LANDBACK":
                qrCode.landbank = image
            
            if banks == "PNB":
                qrCode.pnb = image
            
            if banks == "METRO BANK":
                qrCode.metro = image
            
            if banks == "UNION BANK":
                qrCode.union = image
            
            if banks == "CHINA BANK":
                qrCode.china = image

        qrCode.save()

    return redirect("projects")

def volunteer_mode(request):
    if request.method == "POST":
        MOD(request.POST)

        donated = request.POST["title"]
        name = request.POST["name"]
        contact_number = request.POST["contact_number"]
        images = request.FILES.getlist("images")

        what_kind = request.POST["what_kind"]

        for image in images:
            if what_kind == "CAN GOODS":

                donation = MOD(
                    donation_type="Volunteer",
                    donated=donated,
                    name=name,
                    contact_number=contact_number,
                    what_kind=what_kind,
                    recepient_things=request.POST['recepient_things'],
                    image_details=image,
                )

                donation.save()
        
        # date_sched = request.POST["date_sched"]
        # amount = request.POST["amount"]

        

    return redirect("projects")


@login_required(login_url="home")
def reports(request):
    user = request.user.is_staff

    # loadDonations = MOD.objects.all()

    # for i in loadDonations:
    #     print(i.date_time)

    return render(
        request,
        "community_involvement/reports.html",
        {"url": "report", "user": user},
    )


def reports_all(request):
    loadDonations = MOD.objects.all()
    return render(
        request,
        "community_involvement/reports.html",
        {
            "url": "report",
            "loadDonations": loadDonations,
        },
    )


def reports_find(request):

    if request.method == "POST":
        month = request.POST.get("month")
        year = request.POST.get("year")

        loadDonations = MOD.objects.filter(date__month=month, date__year=year)
    return render(
        request,
        "community_involvement/reports.html",
        {
            "url": "report",
            "loadDonations": loadDonations,
        },
    )


def archive_project(request, id):

    Project.objects.filter(id=id).update(archive=True)

    return redirect("projects")


def archive_program(request, id):
    Program.objects.filter(id=id).update(archive=True)

    return redirect("programs")


def dashboard(request):
    user = request.user.is_staff
    return render(
        request,
        "community_involvement/admin/dashboard.html",
        {"user": user},
    )


def donation_validate(request):
    loadDonations = MOD.objects.filter(status=None)
    return render(
        request,
        "community_involvement/admin/donation-validate.html",
        {
            "url": "report",
            "loadDonations": loadDonations,
        },
    )


def donation_accept(request, id):
    MOD.objects.filter(id=id).update(status="Accepted")

    return redirect("donation")


def donation_decline(request, id):
    MOD.objects.filter(id=id).update(status="Declined")

    return redirect("donation")


def donation_filter(request):
    if request.method == "POST":
        statusFilter = request.POST.get("filterStatus")

        # print(statusFilter)

        filterStatus = MOD.objects.filter(status=statusFilter)

    return render(
        request,
        "community_involvement/admin/donation.html",
        {"loadDonations": filterStatus},
    )


def calculate_age(birth_date):
    today = datetime.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    return age


def individualProfile(request):
    if request.method == "POST":
        form = IndividualProfileForm(request.POST, request.FILES)
        if form.is_valid():
            siblings_name = request.POST.getlist("name[]")
            siblings_age = request.POST.getlist("age[]")
            siblings_placework = request.POST.getlist("placework[]")

            name_of_organization = request.POST.getlist("name_of_organization[]")

            inout_school = []
            for i in range(1, len(name_of_organization) + 1):
                inout_school.append(request.POST.get(f"inoutSchool_{i}[]"))

            position = request.POST.getlist("position[]")
            inclusive_years = request.POST.getlist("inclusiveyears[]")

            current_datetime = timezone.now()

            # Daghan kaau kuhaon na fields kay yawa ka daghan na checkbox
            describeYouBest_values = [
                "Friendly",
                "Self-Confident",
                "Calm",
                "Quick-Tempered",
                "Feels Inferior",
                "Unhappy",
                "Easily Bored",
                "Talented",
                "Withdrawn",
                "Conscientious",
                "Talkative",
                "Cheerful",
                "Moody",
                "Easily Exhausted",
                "Lazy",
                "Sensitive",
                "Poor health",
                "Reserved",
                "Quiet",
                "Independent",
                "Depressed",
                "Suspicious",
                "Irritable",
                "Stubborn",
                "Thoughtful",
                "Lovable",
                "Jealous",
                "Shy",
                "Sarcastic",
                "Tactful",
                "Pessimistic",
                "Submissive",
                "Optimistic",
                "Happy-go-lucky",
                "Goal-oriented",
            ]
            # This shit so slow but it works

            describeYouBest_checked = request.POST.getlist("describeYouBest[]")

            student_id = request.POST.get("student_id_val")

            date_of_birth_str = form.cleaned_data["dateOfBirth"]
            date_of_birth = datetime.strptime(str(date_of_birth_str), "%Y-%m-%d")
            age = calculate_age(date_of_birth)

            # Get the studentInfo instance corresponding to the provided student ID
            student = get_object_or_404(studentInfo, studID=student_id)

            # Create a dictionary to store the state (checked or not) of each value
            describeYouBest_state = {
                value: value in describeYouBest_checked
                for value in describeYouBest_values
            }

            new_form = form.save(commit=False)
            new_form.age = age
            new_form.studentId = student
            new_form.dateFilled = current_datetime
            new_form.siblingsName = siblings_name
            new_form.siblingsAge = siblings_age
            new_form.siblingsSchoolWork = siblings_placework

            # Assuming the other fields are also JSONFields
            new_form.nameOfOrganization = name_of_organization
            new_form.inOutSchool = inout_school
            new_form.positionTitle = position
            new_form.inclusiveYears = inclusive_years
            new_form.describeYouBest = describeYouBest_state

            # Handle the studentPhoto field
            if "studentPhoto" in request.FILES:
                new_form.studentPhoto = request.FILES["studentPhoto"]
            transaction = GuidanceTransaction(
                transactionType=f"{student.lastname} {student.firstname} fillup Individual Profile.",
                transactionDate=timezone.now(),
            )
            transaction.save()
            new_form.save()
            messages.success(request, "Your information has been submitted.")
            return redirect("Individual Profile")
    else:
        form = IndividualProfileForm()
    context = {"form": form}
    return render(request, "guidance/user/individual_profile.html", context)


def intake_interview_view(request):

    # Mas daghan panig bug kaysa wuthering waves

    if request.method == "POST":
        individualId = request.POST.get("individualId")

        individualActivity = request.POST.getlist("individualActivity[]")
        individualDateAccomplished = request.POST.getlist("individualAccomplished[]")
        individualRemarks = request.POST.getlist("individualRemarks[]")

        apprailsalTest = request.POST.getlist("appraisalTest[]")
        apprailsalDateTaken = request.POST.getlist("appraisalDateTaken[]")
        apprailsalDateInterpreted = request.POST.getlist("appraisalDateInterpreted[]")
        apprailsalRemarks = request.POST.getlist("appraisalRemarks[]")

        counseling_types = request.POST.getlist("couseling_type[]")
        selected_types = []

        for ctype in counseling_types:
            if ctype == "True":
                selected_types.append("Referral")
            elif ctype == "False":
                selected_types.append("Walk-in")

        counselingDate = request.POST.getlist("counselingDate[]")
        counselingConcern = request.POST.getlist("counselingConcern[]")
        counselingRemarks = request.POST.getlist("counselingRemarks[]")

        followActivity = request.POST.getlist("followActivity[]")
        followDate = request.POST.getlist("followDate[]")
        followRemarks = request.POST.getlist("followRemarks[]")

        informationActivity = request.POST.getlist("informationActivity[]")
        informationDate = request.POST.getlist("informationDate[]")
        informationRemarks = request.POST.getlist("informationRemarks[]")

        counsultationActivity = request.POST.getlist("counseltationActivity[]")
        counsultationDate = request.POST.getlist("counseltationDate[]")
        counsultationRemarks = request.POST.getlist("counseltationRemarks[]")

        individual = get_object_or_404(
            IndividualProfileBasicInfo, individualProfileID=individualId
        )

        # Issue: Di mag sunod2 sa database

        # 'If ignoring this issue is a sin then I am a sinner - Bryan Antier 2024'

        obj = IntakeInverView(
            individualProfileId=individual,
            individualActivity=individualActivity,
            individualDateAccomplished=individualDateAccomplished,
            individualRemarks=individualRemarks,
            appraisalTest=apprailsalTest,
            appraisalDateTaken=apprailsalDateTaken,
            appraisalDateInterpreted=apprailsalDateInterpreted,
            appraisalRemarks=apprailsalRemarks,
            counselingType=selected_types,
            counselingDate=counselingDate,
            counselingConcern=counselingConcern,
            counselingRemarks=counselingRemarks,
            followActivity=followActivity,
            followDate=followDate,
            followRemarks=followRemarks,
            informationActivity=informationActivity,
            informationDate=informationDate,
            informationRemarks=informationRemarks,
            counsultationActivity=counsultationActivity,
            counsultationDate=counsultationDate,
            counsultationRemarks=counsultationRemarks,
        )
        obj.save()

        transaction = GuidanceTransaction(
            transactionType=f"Counselor fill out the intake interview for {individual.studentId.studID}",
            transactionDate=timezone.now(),
        )
        transaction.save()

        new_intake_id = obj.intakeId

        return redirect("individual_profile_sheet", id=new_intake_id)

    return render(request, "guidance/admin/intake_interview.html", {})


def individual_profile_sheet(request, id):
    intake = IntakeInverView.objects.get(intakeId=id)
    return render(
        request, "guidance/admin/individual_profile_sheet.html", {"form": intake}
    )


def search_student_info_for_intake(request):
    if request.method == "POST":
        id_number = request.POST.get("id_number", "")
        try:
            student = studentInfo.objects.get(studID=id_number)
            individual = IndividualProfileBasicInfo.objects.filter(studentId=student)
            items = []
            for val in individual:
                response = {
                    "profile_number": val.individualProfileID,
                    "studentid": val.studentId.studID,
                    "name": f"{val.studentId.lastname}, {val.studentId.middlename}, {val.studentId.firstname}",
                    "datefilled": val.dateFilled.strftime("%B %d, %Y"),
                }
                items.append(response)

            return JsonResponse({"response": items})
        except studentInfo.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)


@register.filter
def extract_initials(text):
    words = text.split()
    result = ""
    for word in words:
        if word[0].isupper():
            result += word[0]
    return result


def counseling_app(request):
    if request.method == "POST":
        form = CounselingSchedulerForm(request.POST)
        if form.is_valid():
            current_datetime = timezone.now()
            student_id = request.POST.get("student_id_val")

            # Get the studentInfo instance corresponding to the provided student ID
            student = get_object_or_404(studentInfo, studID=student_id)

            # Check for ongoing schedules
            ongoing_schedule = counseling_schedule.objects.filter(
                studentID=student, scheduled_date__gte=current_datetime.date()
            ).first()

            if (
                ongoing_schedule
                and not ongoing_schedule.status == "Declined"
                and not ongoing_schedule.status == "Expired"
            ):
                time = {
                    "8-9": "8:00 AM - 9:00 AM",
                    "9-10": "9:00 AM - 10:00 AM",
                    "10-11": "10:00 AM-11:00 AM",
                    "11-12": "11:00 AM -12:00 PM",
                    "1-2": "1:00 PM - 2:00 PM",
                    "2-3": "2:00 PM - 3:00 PM",
                    "3-4": "3:00 PM - 4:00 PM",
                    "4-5": "4:00 PM - 5:00 PM",
                }

                scheduled_date = ongoing_schedule.scheduled_date.strftime("%B %d, %Y")
                scheduled_time = time[f"{ongoing_schedule.scheduled_time}"]
                messages.error(
                    request,
                    f"You still have an ongoing schedule on {scheduled_date} on {scheduled_time}.",
                )
                return redirect("Counseling App With Scheduler")

            formatted_date = current_datetime.strftime("%Y-%m-%d")
            counseling = form.save(commit=False)
            counseling.orno = 0
            counseling.dateRecieved = formatted_date
            counseling.studentID = student  # Assign the studentInfo instance
            counseling.save()
            transaction = GuidanceTransaction(
                transactionType=f"{student.lastname} {student.firstname} requested a counseling schedule",
                transactionDate=timezone.now(),
            )
            transaction.save()

            messages.success(
                request,
                "Your request has been successfully added. An email will be sent if it is accepted.",
            )
            return redirect("Counseling App With Scheduler")
    else:
        form = CounselingSchedulerForm()

    context = {"form": form}
    return render(request, "guidance/user/counseling_app.html", context)


def counseling_app_admin_view(request):
    meeting_requests = counseling_schedule.objects.select_related("studentID").order_by(
        "-dateRecieved"
    )

    time = {
        "8-9": "8:00 AM - 9:00 AM",
        "9-10": "9:00 AM - 10:00 AM",
        "10-11": "10:00 AM-11:00 AM",
        "11-12": "11:00 AM -12:00 PM",
        "1-2": "1:00 PM - 2:00 PM",
        "2-3": "2:00 PM - 3:00 PM",
        "3-4": "3:00 PM - 4:00 PM",
        "4-5": "4:00 PM - 5:00 PM",
    }

    context = {
        "meeting_requests": meeting_requests,
        "time": time,
    }
    return render(request, "guidance/admin/counseling_app_admin_view.html", context)


def exit_interview(request):
    if request.method == "POST":
        form = ExitInterviewForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            fields = [
                "academically_too_challenging",
                "not_academically_challenging_enough",
                "does_not_offer_my_academic_major",
                "what_is_your_intended_major",
                "size_of_the_school",
                "location_of_the_school",
                "negative_social_campus_climate",
                "residence_hall_environment_not_positive",
                "social_environment_not_diverse_enough",
                "not_enough_campus_activities",
                "needed_more_academic_support",
                "financial",
                "medical_injury",
                "medical_pyscho",
                "family-obligations",
                "major_event",
            ]
            values = []
            for field in fields:
                value = request.POST.get(field, "")
                if value == "":
                    values.append("")
                else:
                    values.append(value)
            student_id = request.POST.get("studentID")

            # Get the studentInfo instance corresponding to the provided student ID
            student = get_object_or_404(studentInfo, studID=student_id)

            ongoing_request = exit_interview_db.objects.filter(
                studentID=student, status="Pending"
            ).first()

            if ongoing_request:
                messages.error(request, f"You still have an pending request.")
                return redirect("Exit Interview")

            current_date = timezone.localtime(timezone.now())
            date_number = current_date.strftime("%m%d%y")  # Format date as MMDDYY

            # Sum the digits of the student ID
            digit_sum = sum(int(digit) for digit in str(student_id))

            # Combine date number and digit sum into a preliminary final number
            preliminary_final_number = f"{date_number}{digit_sum}"

            # Calculate the number of zeros needed to make the length 10 digits
            total_length = 10
            number_of_zeros_needed = total_length - len(preliminary_final_number)

            # Insert zeros between date number and digit sum
            final_number = f"{date_number}{'0' * number_of_zeros_needed}{digit_sum}"

            new_form.date = timezone.now()
            new_form.contributedToDecision = values
            new_form.studentID = student
            new_form.dateRecieved = timezone.now()
            new_form.save()
            transaction = GuidanceTransaction(
                transactionType=f"{student.lastname} {student.firstname} requested a exit interview schedule",
                transactionDate=timezone.now(),
            )
            transaction.save()
            messages.success(
                request,
                "Your request has been successfully added. An email will be sent if it is accepted.",
            )
            return redirect("Exit Interview")
    else:
        form = ExitInterviewForm()
    return render(request, "guidance/user/exit_interview.html", {"form": form})


def exit_interview_admin_view(request):
    exit_interview_request = exit_interview_db.objects.select_related(
        "studentID"
    ).order_by("-dateRecieved")
    context = {
        "exit_interview_request": exit_interview_request,
    }
    return render(request, "guidance/admin/exit_interview_admin.html", context)


def ojt_assessment(request):
    if request.method == "POST":
        form = OjtAssessmentForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            student_id = request.POST.get("student_id_val")
            student = get_object_or_404(studentInfo, studID=student_id)
            currentdate = timezone.now()
            ongoing_request = OjtAssessment.objects.filter(
                studentID=student, status="Pending"
            ).first()

            if ongoing_request:
                messages.error(request, f"You still have an pending request.")
                return redirect("OJT Assessment")

            new_form.studentID = student
            new_form.dateRecieved = currentdate
            new_form.dateAccepted = currentdate
            new_form.save()
            transaction = GuidanceTransaction(
                transactionType=f"{student.lastname} {student.firstname} requested a ojt assessment",
                transactionDate=timezone.now(),
            )
            transaction.save()
            messages.success(
                request,
                "Your request has been successfully added. An email will be sent if it is accepted.",
            )
            return redirect("OJT Assessment")
    else:
        form = OjtAssessmentForm()
    return render(request, "guidance/user/ojt_assessment.html", {"form": form})


def ojt_assessment_admin_view(request):
    ojt_assessment_request = OjtAssessment.objects.select_related("studentID").order_by(
        "-dateRecieved"
    )
    context = {
        "ojt_assessment_request": ojt_assessment_request,
    }
    return render(request, "guidance/admin/ojt_assessment_admin.html", context)


def guidance_transaction(request):
    transactions = GuidanceTransaction.objects.all()
    return render(request, "guidance/admin/transaction.html", {"form": transactions})


# Checker/Getter


def check_date_time_validity(request):
    if request.method == "POST":
        selected_date = request.POST.get("selected_date")
        try:
            # Convert the selected date string to a Python datetime object
            selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
            # Query the counseling_schedule model for entries with the same scheduled_date
            counseling_schedules = counseling_schedule.objects.filter(
                scheduled_date=selected_date
            )
            # You can now do something with the counseling_schedules queryset, like serialize it to JSON
            serialized_data = [
                {"scheduled_time": schedule.scheduled_time, "status": schedule.status}
                for schedule in counseling_schedules
            ]
            return JsonResponse({"counseling_schedules": serialized_data})
        except ValueError:
            # Handle invalid date format
            return JsonResponse({"error": "Invalid date format"}, status=400)


def check_date_time_validity_for_exit(request):
    if request.method == "POST":
        selected_date = request.POST.get("selected_date")
        try:
            # Convert the selected date string to a Python datetime object
            selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
            # Query the counseling_schedule model for entries with the same scheduled_date
            counseling_schedules = exit_interview_db.objects.filter(
                scheduled_date=selected_date
            )
            # You can now do something with the counseling_schedules queryset, like serialize it to JSON
            serialized_data = [
                {"scheduled_time": schedule.scheduled_time, "status": schedule.status}
                for schedule in counseling_schedules
            ]
            return JsonResponse({"counseling_schedules": serialized_data})
        except ValueError:
            # Handle invalid date format
            return JsonResponse({"error": "Invalid date format"}, status=400)


def search_student_info_for_individual(request):
    if request.method == "POST":
        id_number = request.POST.get("id_number", "")
        try:
            student = studentInfo.objects.get(studID=id_number)
            response = {
                "student_id": student.studID,
                "name": f"{(student.lastname).title()}, {(student.middlename).title()}, {(student.firstname.title())}",
                "program": student.degree,
                "sex": student.sex,
            }
            return JsonResponse(response)
        except studentInfo.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)


def search_student_info(request):
    if request.method == "POST":
        id_number = request.POST.get("id_number", "")
        try:
            student = studentInfo.objects.get(studID=id_number)
            response = {
                "student_id": student.studID,
                "name": f"{student.lastname}, {student.firstname}",
                "program": student.degree,
                "year": student.yearlvl,
                "contact_number": student.contact,
                "email": student.emailadd,
            }
            return JsonResponse(response)
        except studentInfo.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)


def search_exit_interview_request(request):
    if request.method == "POST":
        id_number = request.POST.get("id_number", "")
        students = exit_interview_db.objects.filter(studentID__studID=id_number)
        if students.exists():
            response = []
            for student in students:
                response.append(
                    {
                        "exit_interview_id": student.exitinterviewId,
                        "date_received": student.dateRecieved.strftime("%B %d, %Y"),
                        "student_id": student.studentID.studID,
                        "name": f"{student.studentID.lastname}, {student.studentID.firstname}",
                        "status": student.status,
                    }
                )
            return JsonResponse(
                response, safe=False
            )  # safe=False to allow serialization of non-dict objects
        else:
            return JsonResponse({"error": "Student not found"}, status=404)


def search_ojt_assessment_request(request):
    if request.method == "POST":
        id_number = request.POST.get("id_number", "")
        students = OjtAssessment.objects.filter(studentID__studID=id_number)
        if students.exists():
            response = []
            for student in students:
                response.append(
                    {
                        "ojt_assessment_id": student.OjtRequestID,
                        "date_received": student.dateRecieved.strftime("%B %d, %Y"),
                        "student_id": student.studentID.studID,
                        "name": f"{student.studentID.lastname}, {student.studentID.firstname}",
                        "schoolyear": student.schoolYear,
                        "status": student.status,
                    }
                )
            return JsonResponse(
                response, safe=False
            )  # safe=False to allow serialization of non-dict objects
        else:
            return JsonResponse({"error": "Student not found"}, status=404)


def get_exit_interview_request(request):
    if request.method == "POST":
        recordID = request.POST.get("requestID", "")
        try:
            student = exit_interview_db.objects.get(exitinterviewId=recordID)
            if student.studentID.middlename == "NONE":
                middleInit = ""  # Set to empty string if text is 'NONE'
            else:
                middleInit = student.studentID.middlename[0]

            response = {
                "name": f"{student.studentID.firstname.title()} {middleInit} {student.studentID.lastname.title()}",
                "date": (student.date).strftime("%B %d, %Y"),
                "dateenrolled": (student.dateEnrolled).strftime("%B %d, %Y"),
                "contact": student.studentID.contact,
                "reasonforleaving": student.reasonForLeaving,
                "satisfiedWithAcadamic": student.satisfiedWithAcadamic,
                "feedbackWithAcademic": student.feedbackWithAcademic,
                "satisfiedWithSocial": student.satisfiedWithSocial,
                "feedbackWithSocial": student.feedbackWithSocial,
                "satisfiedWithServices": student.satisfiedWithServices,
                "feedbackWithServices": student.feedbackWithServices,
                "contributedToDecision": student.contributedToDecision,
                "intendedMajor": student.intendedMajor,
                "firstConsider": student.firstConsider,
                "whatCondition": student.whatCondition,
                "recommend": student.recommend,
                "howSatisfied": (student.howSatisfied).title(),
                "planTOReturn": student.planTOReturn,
                "accademicExperienceSatisfied": student.accademicExperienceSatisfied,
                "knowAboutYourTime": student.knowAboutYourTime,
                "currentlyEmployed": student.currentlyEmployed,
                "explainationEmployed": student.explainationEmployed,
            }
            return JsonResponse(response)
        except studentInfo.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)


def get_ojt_assessment_data(request):
    if request.method == "POST":
        recordID = request.POST.get("OjtRequestID", "")
        try:
            student = OjtAssessment.objects.get(OjtRequestID=recordID)
            if student.studentID.middlename == "NONE":
                middleInit = ""  # Set to empty string if text is 'NONE'
            else:
                middleInit = student.studentID.middlename[0]
            dateAccepted = student.dateAccepted
            formatted_dateAccepeted = dateAccepted.strftime("%B %d, %Y")
            response = {
                "name": f"{student.studentID.firstname.title()} {middleInit} {student.studentID.lastname.title()}",
                "schoolyear": student.schoolYear,
                "program": student.studentID.degree,
                "date_accepted": formatted_dateAccepeted,
            }
            return JsonResponse(response)
        except studentInfo.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)


# Update/Delete


def update_counseling_schedule(request):
    if request.method == "POST":
        requestID = request.POST.get("counselingID", "")
        update_type = request.POST.get("type", "")
        if update_type == "accept":
            obj = get_object_or_404(counseling_schedule, counselingID=requestID)
            obj.status = "Accepted"
            message = f"Hello {obj.studentID.firstname.title()} {obj.studentID.lastname.title()} your Counseling Schedule request has been approved."
            email = obj.email
            obj.save()

            # This shit takes longer to finish that my will to live
            transaction = GuidanceTransaction(
                transactionType=f"{obj.studentID.firstname.title()} {obj.studentID.lastname.title()} Counseling Schedule requested was approved",
                transactionDate=timezone.now(),
            )
            transaction.save()
            send_mail(
                "Counseling Schedule Request",
                message,
                "notifytest391@gmail.com",  # From email
                [email],  # To email
                fail_silently=False,
            )
            obj.save()

            # Optionally, you can return a JSON response indicating success
            return JsonResponse({"message": "Value updated successfully"})
        elif update_type == "decline":
            obj = get_object_or_404(counseling_schedule, counselingID=requestID)
            obj.status = "Declined"
            message = f"Hello {obj.studentID.firstname.title()} {obj.studentID.lastname.title()} your Counseling Schedule request has been declined."
            email = obj.email
            obj.save()
            transaction = GuidanceTransaction(
                transactionType=f"{obj.studentID.firstname.title()} {obj.studentID.lastname.title()}  Counseling Schedule was declined.",
                transactionDate=timezone.now(),
            )
            transaction.save()
            send_mail(
                "Counseling Schedule Request",
                message,
                "notifytest391@gmail.com",  # From email
                [email],  # To email
                fail_silently=False,
            )
            obj.save()

            # Optionally, you can return a JSON response indicating success
            return JsonResponse({"message": "Value updated successfully"})


def delete_counseling_schedule(request):
    if request.method == "POST":
        requestID = request.POST.get("counselingID", "")
        obj = get_object_or_404(counseling_schedule, counselingID=requestID)
        obj.delete()
        return JsonResponse({"message": "Value updated successfully"})


def update_exit_interview_status(request):
    if request.method == "POST":
        requestID = request.POST.get("exitinterviewId", "")
        update_type = request.POST.get("type", "")
        if update_type == "accept":
            obj = get_object_or_404(exit_interview_db, exitinterviewId=requestID)
            obj.status = "Accepted"
            message = f"Hello {obj.studentID.firstname.title()} {obj.studentID.lastname.title()} your Exit Interview request has been approved."
            email = obj.emailadd
            obj.save()
            transaction = GuidanceTransaction(
                transactionType=f"{obj.studentID.firstname.title()} {obj.studentID.lastname.title()}  Exit Interview was approved.",
                transactionDate=timezone.now(),
            )
            transaction.save()
            send_mail(
                "Exit Interview Request",
                message,
                "notifytest391@gmail.com",  # From email
                [email],  # To email
                fail_silently=False,
            )
            obj.save()

            # Optionally, you can return a JSON response indicating success
            return JsonResponse({"message": "Value updated successfully"})
        elif update_type == "decline":
            obj = get_object_or_404(exit_interview_db, exitinterviewId=requestID)
            obj.status = "Declined"
            message = f"Hello {obj.studentID.firstname.title()} {obj.studentID.lastname.title()} your Exit Interview request has been declined."
            email = obj.emailadd
            obj.save()
            transaction = GuidanceTransaction(
                transactionType=f"{obj.studentID.firstname.title()} {obj.studentID.lastname.title()}  Exit Interview was declined.",
                transactionDate=timezone.now(),
            )
            transaction.save()
            send_mail(
                "Exit Interview Request",
                message,
                "notifytest391@gmail.com",  # From email
                [email],  # To email
                fail_silently=False,
            )
            obj.save()

            # Optionally, you can return a JSON response indicating success
            return JsonResponse({"message": "Value updated successfully"})


def delete_exit_interview_status(request):
    if request.method == "POST":
        requestID = request.POST.get("exitinterviewId", "")
        obj = get_object_or_404(exit_interview_db, exitinterviewId=requestID)
        obj.delete()
        return JsonResponse({"message": "Value updated successfully"})


def update_ojt_assessment(request):
    if request.method == "POST":
        requestID = request.POST.get("OjtRequestID", "")
        orno = request.POST.get("orno", "")
        update_type = request.POST.get("type", "")
        if update_type == "accept":
            obj = get_object_or_404(OjtAssessment, OjtRequestID=requestID)
            obj.status = "Accepted"
            obj.orno = orno
            obj.dateAccepted = timezone.now()
            message = f"Hello {obj.studentID.firstname.title()} {obj.studentID.lastname.title()} your OJT Assessments/Psychological Issuance request has been approved."
            transaction = GuidanceTransaction(
                transactionType=f"{obj.studentID.firstname.title()} {obj.studentID.lastname.title()}  OJT Assessments/Psychological Issuance was approved.",
                transactionDate=timezone.now(),
            )
            transaction.save()
            email = obj.emailadd
            obj.save()
            send_mail(
                "OJT Assessments/Psychological Issuance Request",
                message,
                "notifytest391@gmail.com",  # From email
                [email],  # To email
                fail_silently=False,
            )

            # Optionally, you can return a JSON response indicating success
            return JsonResponse({"message": "Value updated successfully"})
        elif update_type == "decline":
            obj = get_object_or_404(OjtAssessment, OjtRequestID=requestID)
            obj.status = "Declined"
            obj.save()

            transaction = GuidanceTransaction(
                transactionType=f"{obj.studentID.firstname.title()} {obj.studentID.lastname.title()}  OJT Assessments/Psychological Issuance was declined.",
                transactionDate=timezone.now(),
            )
            transaction.save()
            message = f"Hello {obj.studentID.firstname.title()} {obj.studentID.lastname.title()} your OJT Assessments/Psychological Issuance request has been declined."
            email = obj.emailadd
            send_mail(
                "OJT Assessments/Psychological Issuance Request",
                message,
                "notifytest391@gmail.com",  # From email
                [email],  # To email
                fail_silently=False,
            )
            # Optionally, you can return a JSON response indicating success
            return JsonResponse({"message": "Value updated successfully"})


def delete_ojt_assessment(request):
    if request.method == "POST":
        requestID = request.POST.get("exitinterviewId", "")
        obj = get_object_or_404(OjtAssessment, OjtRequestID=requestID)
        obj.delete()
        return JsonResponse({"message": "Value updated successfully"})


# Filter


@register.filter
def get_formatted_time(dictionary, key):
    return dictionary.get(key)
