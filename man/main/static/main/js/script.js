const textarea = document.getElementById("textar")
const fileButton = document.getElementById("filear")
const submitButton = document.getElementById("submit")
const para = document.querySelector('.file-info')

if (textarea) {
textarea.addEventListener('input', function() {
    if (this.value) {
        fileButton.disabled = true
    } else {
        fileButton.disabled = false
    }
})
}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

if (fileButton) {
fileButton.addEventListener('change', function() {
    if (this.value) {
        textarea.disabled = true
    } else {
        textarea.disabled = false
    }

    const curFiles = fileButton.files

    if (curFiles.length) {
        para.textContent = `Обрано файл ${curFiles[0].name}`
    }
})}

if (submitButton) {
submitButton.addEventListener('click', function() {
    const curFiles = fileButton.files

    if (curFiles.length) {
        document.cookie = `filename=${curFiles[0].name};max-age=3600`
    }
})
}

if (para) {
    let filename = getCookie("filename")
    if (filename) {
        para.textContent = `Обрано файл ${filename}`
    } else {
        para.textContent = "Файл не обрано"
    }
}
