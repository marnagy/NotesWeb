// const delete_buttons = document.querySelectorAll('.note-container > div > button')

// delete_buttons.forEach((button) => {
//     const note_id = parseInt( button.getAttribute('data-reference') )
//     button.addEventListener('click', async () => {
//         button.setAttribute('disabled', true)

//         const target_url = `${window.location.host}/note/delete/${note_id}`
//         alert(`Target url: ${target_url}`)
//         const resp = await fetch(target_url, {
//             method: 'DELETE',
//             headers: {
//                 'Content-Type': 'application/json'
//             }
//         })

//         button.removeAttribute('disabled')
//     })
// })