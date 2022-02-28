page_name = "{{page_name}}"
// warn if page name not given
console.log(!['/accounts/login/','/accounts/register/'].includes(window.location.pathname))
console.log(window.location.pathname)
console.log(document.cookie, document.location.search)
// cookie for auntification
if(!['/accounts/login/','/accounts/register/'].includes(window.location.pathname))
    document.cookie = 'before_sign_page=' + window.location.pathname.toString()+';path=/'
// cookie for group task pass
if(!['/accounts/login/','/accounts/register/'].includes(window.location.pathname))
document.cookie = 'before_sign_page=' + window.location.pathname.toString()+document.location.search+';path=/'
console.log(document.cookie)
// group module pass
if(page_name == "group_show"){}