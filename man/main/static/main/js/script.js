const textarea = document.getElementById("textar")
const fileButton = document.getElementById("filear")
const para = document.querySelector('.file-info')

try {
    para.textContent = localStorage.getItem('is_chosen')
} catch (SyntaxError) {
    console.log('catched')
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
        localStorage.setItem('is_chosen', 'Файл не обрано')
    } else {
        localStorage.setItem('is_chosen', `Обрано файл ${curFiles[0].name}`)
    }
    para.textContent = localStorage.getItem('is_chosen')
})}
// window.addEventListener('contextmenu', (e) => {
//     e.preventDefault()
//     console.log(window.getSelection().toString())
//     return false
// })