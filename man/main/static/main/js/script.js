const textarea = document.getElementById("textar")
const fileButton = document.getElementById("filear")
const para = document.querySelector('.file-info')

para.textContent = 'Файл не обрано'

if (textarea) {
textarea.addEventListener('input', function() {
    if (this.value) {
        fileButton.disabled = true
    } else {
        fileButton.disabled = false
    }
})
}

if (fileButton) {
fileButton.addEventListener('change', function() {
    if (this.value) {
        textarea.disabled = true
    } else {
        textarea.disabled = false
    }
    
    const curFiles = fileButton.files

    if (curFiles.length === 0) {
        para.textContent = 'Файл не обрано'
    } else {
        para.textContent = `Обрано файл ${curFiles[0].name}`
    }
})}
// window.addEventListener('contextmenu', (e) => {
//     e.preventDefault()
//     console.log(window.getSelection().toString())
//     return false
// })