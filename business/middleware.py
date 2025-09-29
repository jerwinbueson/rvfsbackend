from .models import CalendarYear

class CalendarYearSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and 'calendar_year_id' not in request.session:
            bu = getattr(request.user, 'business_unit', None)
            if bu:
                default_year = CalendarYear.objects.filter(business_unit=bu, default=True).first()
                if default_year:
                    request.session['calendar_year_id'] = default_year.id
        
        return self.get_response(request)             