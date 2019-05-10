
function fixXss(stringword) {
    if (stringword) {
        return stringword.toString().replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
    else {
        return stringword
    }
}