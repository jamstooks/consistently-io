export const getCookie = name => {
    let match = "(?:(?:^|.*;\\s*)"
    match += name
    match += "\\s*\\=\\s*([^;]*).*$)|^.*$"
    return document.cookie.replace(RegExp(match), "$1")
}
