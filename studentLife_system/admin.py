from django.contrib import admin
from .models import studentInfo, RequestedGMC, Schedule, equipment
from .models import Alumni, graduateForm, Event, Yearbook, Event, JobFair
from .models import (
    studentInfo,
    RequestedGMC,
    Schedule,
    equipment,
    Program,
    Project,
    MOD,
    QrDonation,
)
from .models import (
    IndividualProfileBasicInfo,
    TestArray,
    FileUploadTest,
    counseling_schedule,
    exit_interview_db,
    OjtAssessment,
    IntakeInverView,
    GuidanceTransaction,
)


class StudentInfoAdmin(admin.ModelAdmin):

    list_display = (
        "studID",
        "lastname",
        "firstname",
        "middlename",
        "degree",
        "yearlvl",
        "sex",
        "emailadd",
        "contact",
    )
    search_fields = ("studID", "lastname", "firstname", "lrn")
    list_filter = ("degree", "yearlvl", "sex")


admin.site.register(studentInfo, StudentInfoAdmin)


class requestedgmcAdmin(admin.ModelAdmin):
    list_display = ("student", "reason", "or_num", "request_date", "processed")


admin.site.register(RequestedGMC, requestedgmcAdmin)


class scheduleAdmin(admin.ModelAdmin):
    list_display = (
        "sched_Id",
        "title",
        "description",
        "start_datetime",
        "end_datetime",
    )


class AlumniAdmin(admin.ModelAdmin):
    list_display = (
        "alumniID",
        "student_id",
        "firstname",
        "lastname",
        "degree",
        "alumniaddress",
    )

    def get_firstname(self, obj):
        return obj.student.fname

    get_firstname.short_description = "First Name"

    def get_lastname(self, obj):
        return obj.student.lname

    get_lastname.short_description = "Last Name"


class graduateFormAdmin(admin.ModelAdmin):
    list_display = (
        "get_alumniID",
        "dategraduated",
        "firstname",
        "lastname",
        "alumniaddress",
    )

    def get_alumniID(self, obj):
        return obj.alumniID.alumniID

    get_alumniID.short_description = "Alumni ID"


class EventAdmin(admin.ModelAdmin):
    list_display = ("eventID", "eventsName", "eventsDate", "eventsLocation")


class JobFairAdmin(admin.ModelAdmin):
    list_display = (
        "jobfair_id",
        "jobtitle",
        "companyname",
        "joblocation",
        "employmenttype",
        "jobsalary",
    )


class YearbookAdmin(admin.ModelAdmin):
    list_display = (
        "yearbookID",
        "yearbookFirstname",
        "yearbookLastname",
        "yearbookGender",
        "yearbookAddress",
        "yearbookCourse",
        "yearbookYearGrad",
    )


admin.site.register(Yearbook, YearbookAdmin)
admin.site.register(JobFair, JobFairAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(graduateForm, graduateFormAdmin)
admin.site.register(Alumni, AlumniAdmin)
admin.site.register(Schedule, scheduleAdmin)

admin.site.register(equipment)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "caption", "date_time", "archive", "image_upload")


class ProgramAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "caption", "date_time", "archive", "image_upload")


class DonationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "donated",
        "donation_type",
        "name",
        "gcash_number",
        "bank_number",
        "bank_card",
        "contact_number",
        "amount",
        "what_kind",
        "recepient",
        "recepient_things",
        "date_sched",
        "date",
        "image_details",
    )


class QrDonationAdmin(admin.ModelAdmin):
    list_display = (
        "qr_id",
        "gcash",
        "bpi",
        "bdo",
        "landbank",
        "pnb",
        "metro",
        "union",
        "china",
    )


admin.site.register(Program, ProgramAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(MOD, DonationAdmin)
admin.site.register(QrDonation, QrDonationAdmin)


class IndividualProfileBasicInfoAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.get_fields()]
        super().__init__(model, admin_site)


class IntakeInverViewAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.get_fields()]
        super().__init__(model, admin_site)


admin.site.register(IndividualProfileBasicInfo)
admin.site.register(IntakeInverView)


class counselingSceduleAdmin(admin.ModelAdmin):
    list_display = (
        "counselingID",
        "dateRecieved",
        "studentID",
        "reason",
        "scheduled_date",
        "scheduled_time",
        "email",
        "status",
    )
    list_editable = (
        "dateRecieved",
        "reason",
        "scheduled_date",
        "scheduled_time",
        "email",
        "status",
    )


class OjtAssessmentAdmin(admin.ModelAdmin):
    list_display = [
        "OjtRequestID",
        "studentID",
        "dateRecieved",
        "schoolYear",
        "status",
        "dateAccepted",
        "orno",
    ]
    list_editable = ["schoolYear", "status", "dateAccepted"]


class exitInterviewAdmine(admin.ModelAdmin):
    list_display = (
        "exitinterviewId",
        "studentID",
        "dateRecieved",
        "date",
        "dateEnrolled",
        "reasonForLeaving",
        "satisfiedWithAcadamic",
        "feedbackWithAcademic",
        "satisfiedWithSocial",
        "feedbackWithSocial",
        "satisfiedWithServices",
        "feedbackWithServices",
        "contributedToDecision",
        "intendedMajor",
        "firstConsider",
        "whatCondition",
        "recommend",
        "howSatisfied",
        "planTOReturn",
        "accademicExperienceSatisfied",
        "knowAboutYourTime",
        "currentlyEmployed",
        "explainationEmployed",
        "status",
        "scheduled_date",
        "scheduled_time",
        "emailadd",
    )
    list_editable = (
        "date",
        "dateEnrolled",
        "reasonForLeaving",
        "satisfiedWithAcadamic",
        "feedbackWithAcademic",
        "satisfiedWithSocial",
        "feedbackWithSocial",
        "satisfiedWithServices",
        "feedbackWithServices",
        "intendedMajor",
        "firstConsider",
        "whatCondition",
        "recommend",
        "howSatisfied",
        "planTOReturn",
        "accademicExperienceSatisfied",
        "knowAboutYourTime",
        "currentlyEmployed",
        "explainationEmployed",
        "status",
        "scheduled_date",
        "scheduled_time",
        "emailadd",
    )


admin.site.register(counseling_schedule, counselingSceduleAdmin)
admin.site.register(exit_interview_db, exitInterviewAdmine)
admin.site.register(OjtAssessment, OjtAssessmentAdmin)
admin.site.register(GuidanceTransaction)
