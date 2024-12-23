
def DetectUser(user):
    if user.role == 1 :
        redirectUrl = 'VendorDashboard'
        return redirectUrl
    elif user.role ==  2:
        redirectUrl = 'Custdashboard'
        return redirectUrl
    elif user.role == None or user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
            