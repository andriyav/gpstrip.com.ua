
    const cityDataBox = document.getElementById('city-select')
    const cityInput = document.getElementById('city-select')

    const addressDataBox = document.getElementById('address-select')
    const addressInput = document.getElementById('address-select')
    const addressText = document.getElementById('address-text')
    const btnBox = document.getElementById('btn-box')
    const cityForm = document.getElementById('card-body')


    $.ajax({
        type: 'GET',
        url: '/city-json/',
        success: function (response){
            console.log(response.data)
            const cityData = response.data
            cityData.map(item=>{
                const option = document.createElement('option')
                option.textContent = item.name
                option.setAttribute('class', 'item')
                option.setAttribute('data', item.name)
                cityDataBox.appendChild(option)
            })
        },
        error: function(error){
            console.log(error)
        }
})

    cityInput.addEventListener('change', e=>{
        console.log(e.target.value)
        const selectedCity = e.target.value

        addressDataBox.innerHTML = ''
        addressText.textContent = 'Виберіть відділення'
        // addressText.classList.add('default')



        $.ajax({
            type: "GET",
            url: 'address-json/'+selectedCity,
            success: function (response){
                console.log(response.data)
                const addressData = response.data
                addressData.map(item=> {
                    const option = document.createElement('option')
                    option.textContent = item
                    option.setAttribute('class', 'item')
                    option.setAttribute('data', item)
                    addressDataBox.appendChild(option)
                })

            },
            error: function(error){
                console.log(error)
            }
        })

        })




cityForm.addEventListener('card-body', e=>{
    e.preventDefault()
    console.log('submited')
})

