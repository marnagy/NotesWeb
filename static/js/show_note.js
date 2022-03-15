const edit_cancel_button = document.querySelector('#edit-cancel-button')
let is_button_edit = true

const update_button = document.querySelector('#update-button')

const control_title = document.querySelector('input.control-data').getAttribute('value')
const control_body = document.querySelector('textarea.control-data').text

const input_parent = document.querySelector('.note-title-container')
const input = document.querySelector('input')
const readonly_input = document.querySelector('.note-title-container > h2')

const textarea_parent = document.querySelector('.note-body-container')
const textarea = document.querySelector('textarea')
const readonly_textarea = document.querySelector('.note-body-container > p')

edit_cancel_button.addEventListener('click', () => {
    // update button state
    is_button_edit = !is_button_edit
    edit_cancel_button.innerHTML = is_button_edit === true ? 'Edit' : 'Cancel'

    if (is_button_edit){
        readonly_input.removeAttribute('hidden')
        readonly_textarea.removeAttribute('hidden')

        input.setAttribute('hidden', true)
        textarea.setAttribute('hidden', true)

        update_button.setAttribute('hidden', true)
        update_button.setAttribute('disabled', true)
    }
    else {
        readonly_input.setAttribute('hidden', true)
        readonly_textarea.setAttribute('hidden', true)

        input.removeAttribute('hidden')
        input.setAttribute('value', control_title)
        textarea.removeAttribute('hidden')
        textarea.setAttribute('value', control_body)

        update_button.removeAttribute('hidden')
        update_button.removeAttribute('disabled')
    }
    // remove and add back HTML nodes to update
    input_parent.removeChild(input)
    textarea_parent.removeChild(textarea)
    input_parent.appendChild(input)
    textarea_parent.appendChild(textarea)
})

function getBaseUrl(){
    return window.location.host
}

// update_button.addEventListener('click', async () => {
//     update_button.setAttribute('disabled', true)

//     const new_title = document.querySelector('.note-title-container > input:not(.control-data)')
//     const new_body = document.querySelector('.note-body-container > textarea:not(.control-data)')

//     resp = await fetch(window.location.href, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             'title': new_title,
//             'body': new_body
//         })
//     })

//     update_button.removeAttribute('disabled')
// })
