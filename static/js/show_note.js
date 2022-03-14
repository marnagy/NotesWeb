const edit_button = document.querySelector('#app > button')
const cancel_button = document.querySelector('#app > button.hidden-button')

edit_button.addEventListener('click', () => {
    const input_parent = document.querySelector('.note-title-container')
    const input = document.querySelector('input')
    input.removeAttribute('readonly')
    input_parent.removeChild(input)

    const textarea_parent = document.querySelector('.note-body-container')
    const textarea = document.querySelector('textarea')
    textarea.removeAttribute('readonly')
    textarea_parent.removeChild(textarea)

    input_parent.appendChild(input)
    textarea_parent.appendChild(textarea)

    edit_button.setAttribute('hidden', true)
    cancel_button.removeAttribute('hidden')

})