page_name = "{{page_name}}"
// cookie for auntification
if(!['/accounts/login/','/accounts/register/'].includes(window.location.pathname))
    document.cookie = 'before_sign_page=' + window.location.pathname.toString()+document.location.search+';path=/'
console.log('cookies: '+document.cookie)
// group module pass
if(page_name == "group_show"){}