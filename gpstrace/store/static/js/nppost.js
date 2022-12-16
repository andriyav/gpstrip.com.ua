
    const cityDataBox = document.getElementById('city-select')
    const cityInput = document.getElementById('city-select')
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

        $.ajax({
            type: "GET",
            url: '/address-json/${selectedCity}/',
            success: function (response){
                console.log(response)
            },
            error: function(error){
                console.log(error)
            }
        })
    })


