const form = document.getElementById('registerForm')

form.addEventListener('submit', (e)=>{
    e.preventDefault()

    const formData = new FormData(form)
    const data = Object.fromEntries(formData)

    fetch('/auth/register', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data =>{
        if (data.status == "success") {
            alert(data.message)

            location.href = '/dashboard'
        }
        else{
            throw new Error(data.message);
            
        }
    })
    .catch(err =>{
        alert(err)
    })
})