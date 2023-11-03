const textarea = document.getElementById("textar")
const fileButton = document.querySelector("input[type='file']")

if (fileButton) {
fileButton.addEventListener('change', function() {
    if(this.value){
        textarea.disabled = true
    } else {
        textarea.disabled = false
    }})
}

// window.addEventListener('contextmenu', (e) => {
//     e.preventDefault()
//     console.log(window.getSelection().toString())
//     return false
// })