from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import transac_search
from .views import approve_alumni_request, claim_alumni_id
from .views import (
    home,
    counseling_app,
    exit_interview,
    individualProfile,
    search_student_info,
    check_date_time_validity,
)
from .views import (
    counseling_app_admin_view,
    ojt_assessment,
    exit_interview_admin_view,
    ojt_assessment_admin_view,
    update_exit_interview_status,
)
from .views import (
    delete_exit_interview_status,
    update_ojt_assessment,
    delete_ojt_assessment,
    check_date_time_validity_for_exit,
    get_ojt_assessment_data,
)
from .views import (
    search_ojt_assessment_request,
    search_exit_interview_request,
    get_exit_interview_request,
    update_counseling_schedule,
    delete_counseling_schedule,
)
from .views import (
    search_student_info_for_individual,
    intake_interview_view,
    search_student_info_for_intake,
    individual_profile_sheet,
)
from .views import (
    home,
    counseling_app,
    exit_interview,
    individualProfile,
    search_student_info,
    check_date_time_validity,
)
from .views import (
    counseling_app_admin_view,
    ojt_assessment,
    exit_interview_admin_view,
    ojt_assessment_admin_view,
    update_exit_interview_status,
)
from .views import (
    delete_exit_interview_status,
    update_ojt_assessment,
    delete_ojt_assessment,
    check_date_time_validity_for_exit,
    get_ojt_assessment_data,
)
from .views import (
    search_ojt_assessment_request,
    search_exit_interview_request,
    get_exit_interview_request,
    update_counseling_schedule,
    delete_counseling_schedule,
)
from .views import (
    search_student_info_for_individual,
    intake_interview_view,
    search_student_info_for_intake,
    individual_profile_sheet,
    guidance_transaction,
)


urlpatterns = [
    path("", views.home, name="home"),
    path("requestgmc", views.requestgmc, name="requestgmc"),
    path("equipmenttracker", views.equipmentTracker, name="equipmentTracker"),
    path(
        "equipmenttrackerAdmin/",
        views.equipmentTrackerAdmin,
        name="equipmentTrackerAdmin",
    ),
    path("adminmain", views.adminhome, name="adminmain"),
    path("requested-gmc", views.adminRequestedGmc, name="adminRequestedGmc"),
    path("gmc-form", views.gmcform, name="gmcform"),
    path("generate-gmc/<int:request_id>/", views.generateGmc, name="generateGmc"),
    path("monthlyCalendar", views.monthlyCalendar, name="monthlyCalendar"),
    path(
        "monthlyCalendarAdmin", views.monthlyCalendarAdmin, name="monthlyCalendarAdmin"
    ),
    path("save-schedule/", views.save_schedule, name="save_schedule"),
    path(
        "delete-schedule/<int:schedule_id>/",
        views.delete_schedule,
        name="delete_schedule",
    ),
    path("addEquipment/", views.addEquipment, name="addEquipment"),
    path("id_request/", views.idRequest, name="idRequest"),
    path("search_id/", views.search_id, name="search_id"),
    path("add_alumni/", views.add_alumni, name="add_alumni"),
    path("search_id2/", views.search_id2, name="search_id2"),
    path(
        "graduateTracer_submit",
        views.graduateTracer_submit,
        name="graduateTracer_submit",
    ),
    path("graduatetracer/", views.graduateTracer, name="graduateTracer"),
    path("reunionandevents/", views.alumni_events, name="alumni_events"),
    path("jobfairs/", views.jobfairs, name="jobfairs"),
    path("yearbook/", views.yearbook, name="yearbook"),
    path("search_yearbook/", views.search_yearbook, name="search_yearbook"),
    path(
        "transaction_alumni.html/", views.transaction_alumni, name="transaction_alumni"
    ),
    path("transac_search", transac_search, name="transac_search"),
    path("admin_id_request/", views.admin_id_request, name="admin_idRequest"),
    path(
        "approve_alumni_request/<int:alumni_id>/",
        approve_alumni_request,
        name="approve_alumni_request",
    ),
    path("claim_alumni_id/<int:alumni_id>/", claim_alumni_id, name="claim_alumni_id"),
    path("admin_grad_tracer/", views.admin_gradTracer, name="admin_gradTracer"),
    path("admin_events/", views.admin_events, name="admin_events"),
    path("admin_jobfairs", views.admin_jobfairs, name="admin_jobfairs"),
    path("admin_yearbook", views.admin_yearbook, name="admin_yearbook"),
    # COMMUNITY INVOLVEMENT
    path("programs/", views.programs, name="programs"),
    path("projects/", views.projects, name="projects"),
    path("reports/", views.reports, name="reports"),
    # Forms
    path("program-form/", views.program_form, name="program-form"),
    path("project-form/", views.project_form, name="project-form"),
    # Add
    path("program-form/add_program/", views.add_program, name="add_program"),
    path("project-form/add_project/", views.add_project, name="add_project"),
    # Delete
    path(
        "program-form/archive_program/<int:id>/",
        views.archive_program,
        name="archive_program",
    ),
    path(
        "project-form/archive_project/<int:id>/",
        views.archive_project,
        name="archive_project",
    ),
    # Mode
    path("projects/gcash-mode", views.gcash_mode, name="gcash-mode"),
    path("projects/bank-mode", views.bank_mode, name="bank-mode"),
    path("projects/volunteer-mode", views.volunteer_mode, name="volunteer-mode"),
    path("reports/", views.reports, name="reports"),
    path("reports-all/", views.reports_all, name="reports-all"),
    path("reports-find/", views.reports_find, name="reports-find"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("donation/", views.donation, name="donation"),
    path("donation_accept/<int:id>/", views.donation_accept, name="donation_accept"),
    path("donation_decline/<int:id>/", views.donation_decline, name="donation_decline"),
    path("gcash_mode_admin/<int:id>/", views.gcash_mode_admin, name="gcash_mode_admin"),
    path("donation_filter/", views.donation_filter, name="donation_filter"),
    # Individual Profile URLS
    path("individual_profile", individualProfile, name="Individual Profile"),
    path(
        "search_student_info_for_individual_profile/",
        search_student_info_for_individual,
        name="search_student_info_for_individual_profile",
    ),
    # Intake Interview URLS
    path("intake_interview/", intake_interview_view, name="Intake Interview"),
    path(
        "search_student_info_for_intake/",
        search_student_info_for_intake,
        name="search_student_info_for_intake",
    ),
    path(
        "individual_profile_sheet/",
        individual_profile_sheet,
        name="individual_profile_sheet",
    ),
    # Counseling App Views URLS
    path("counseling_app/", counseling_app, name="Counseling App With Scheduler"),
    path(
        "counseling_app/admin/",
        counseling_app_admin_view,
        name="Counseling App With Scheduler Admin View",
    ),
    # Counseling App Validator, Updator URLS
    path(
        "check_date_time_validity/",
        check_date_time_validity,
        name="check_date_time_validity",
    ),
    path(
        "update_counseling_schedule/",
        update_counseling_schedule,
        name="update_counseling_schedule",
    ),
    path(
        "delete_counseling_schedule/",
        delete_counseling_schedule,
        name="delete_counseling_schedule",
    ),
    # Exit Interview Views URLS
    path("exit_interview", exit_interview, name="Exit Interview"),
    path(
        "exit_interview/admin/",
        exit_interview_admin_view,
        name="Exit Interview Admin View",
    ),
    path(
        "search_exit_interview_request/",
        search_exit_interview_request,
        name="search_exit_interview_request",
    ),
    # Exit Interview Searcher, Validator,Updator URLS
    path("search_student_info/", search_student_info, name="search_student_info"),
    path(
        "check_date_time_validity_for_exit/",
        check_date_time_validity_for_exit,
        name="check_date_time_validity_for_exit",
    ),
    path(
        "update_exit_interview_status/",
        update_exit_interview_status,
        name="update_exit_interview_status",
    ),
    path(
        "delete_exit_interview_status/",
        delete_exit_interview_status,
        name="delete_exit_interview_status",
    ),
    path(
        "get_exit_interview_request/",
        get_exit_interview_request,
        name="get_exit_interview_request",
    ),
    # OJT Assessment Views URLS
    path("ojt_assessment", ojt_assessment, name="OJT Assessment"),
    path(
        "ojt_assessment/admin/",
        ojt_assessment_admin_view,
        name="OJT Assessment Admin View",
    ),
    # OJT Assessment Seacher, Validator, Updator URLS
    path(
        "search_ojt_assessment_request/",
        search_ojt_assessment_request,
        name="search_ojt_assessment_request",
    ),
    path("update_ojt_assessment/", update_ojt_assessment, name="update_ojt_assessment"),
    path("delete_ojt_assessment/", delete_ojt_assessment, name="delete_ojt_assessment"),
    path(
        "get_ojt_assessment_data/",
        get_ojt_assessment_data,
        name="get_ojt_assessment_data",
    ),
    # Individual Profile URLS
    path("individual_profile", individualProfile, name="Individual Profile"),
    path(
        "search_student_info_for_individual_profile/",
        search_student_info_for_individual,
        name="search_student_info_for_individual_profile",
    ),
    # Intake Interview URLS
    path("intake_interview/", intake_interview_view, name="Intake Interview"),
    path(
        "search_student_info_for_intake/",
        search_student_info_for_intake,
        name="search_student_info_for_intake",
    ),
    path(
        "individual_profile_sheet/<int:id>/",
        individual_profile_sheet,
        name="individual_profile_sheet",
    ),
    # Counseling App Views URLS
    path("counseling_app/", counseling_app, name="Counseling App With Scheduler"),
    path(
        "counseling_app/admin/",
        counseling_app_admin_view,
        name="Counseling App With Scheduler Admin View",
    ),
    # Counseling App Validator, Updator URLS
    path(
        "check_date_time_validity/",
        check_date_time_validity,
        name="check_date_time_validity",
    ),
    path(
        "update_counseling_schedule/",
        update_counseling_schedule,
        name="update_counseling_schedule",
    ),
    path(
        "delete_counseling_schedule/",
        delete_counseling_schedule,
        name="delete_counseling_schedule",
    ),
    # Exit Interview Views URLS
    path("exit_interview", exit_interview, name="Exit Interview"),
    path(
        "exit_interview/admin/",
        exit_interview_admin_view,
        name="Exit Interview Admin View",
    ),
    path(
        "search_exit_interview_request/",
        search_exit_interview_request,
        name="search_exit_interview_request",
    ),
    # Exit Interview Searcher, Validator,Updator URLS
    path("search_student_info/", search_student_info, name="search_student_info"),
    path(
        "check_date_time_validity_for_exit/",
        check_date_time_validity_for_exit,
        name="check_date_time_validity_for_exit",
    ),
    path(
        "update_exit_interview_status/",
        update_exit_interview_status,
        name="update_exit_interview_status",
    ),
    path(
        "delete_exit_interview_status/",
        delete_exit_interview_status,
        name="delete_exit_interview_status",
    ),
    path(
        "get_exit_interview_request/",
        get_exit_interview_request,
        name="get_exit_interview_request",
    ),
    # OJT Assessment Views URLS
    path("ojt_assessment", ojt_assessment, name="OJT Assessment"),
    path(
        "ojt_assessment/admin/",
        ojt_assessment_admin_view,
        name="OJT Assessment Admin View",
    ),
    # OJT Assessment Seacher, Validator, Updator URLS
    path(
        "search_ojt_assessment_request/",
        search_ojt_assessment_request,
        name="search_ojt_assessment_request",
    ),
    path("update_ojt_assessment/", update_ojt_assessment, name="update_ojt_assessment"),
    path("delete_ojt_assessment/", delete_ojt_assessment, name="delete_ojt_assessment"),
    path(
        "get_ojt_assessment_data/",
        get_ojt_assessment_data,
        name="get_ojt_assessment_data",
    ),
    path("guidance_transaction", guidance_transaction, name="guidance_transaction"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
