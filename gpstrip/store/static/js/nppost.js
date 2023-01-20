
    const cityDataBox = document.getElementById('city-select') // ініціалізація змінної за елементом id="city-select" checkout.html
    const cityInput = document.getElementById('city-select') // ініціалізація змінної за елементом id="city-select" checkout.html

    const addressDataBox = document.getElementById('address-select')
    const addressInput = document.getElementById('address-select')
    const addressText = document.getElementById('address-text')
    const btnBox = document.getElementById('btn-box')
    const cityForm = document.getElementById('card-body')


    $.ajax({                                                          // функція виводу переліку міст першого випадаючого списку на сторінці checkout.html
        type: 'GET',
        url: '/city-json/',                                             // отримання переліку міст для виводу у випадаючому списку
        success: function (response){
            console.log(response.data)
            console.log('hello1')
            const cityData = response.data
            cityData.map(item=>{                                           // ініціалізація перемінної із переліком міст
                const option = document.createElement('option')   // ініціалізація перемінної блоку html для формування видачі переліку міст у випадаючому списку
                option.textContent = item.name
                option.setAttribute('class', 'item')     // формування блоку html  коду
                option.setAttribute('data', item.name)        // формування випадаючого блоку
                cityDataBox.appendChild(option)
            })
        },
        error: function(error){
            console.log(error)
        }
})

    cityInput.addEventListener('change', e=>{

        console.log(e.target.value)
        const selectedCity = e.target.value                // ініціалізація перемінної із вибраним містом

        addressDataBox.innerHTML = ''
        addressText.textContent = 'Виберіть відділення'
        // addressText.classList.add('default')


        $.ajax({                                         // функція формування переліку вулиць випадаючого списку
            type: "GET",
            url: 'address-json/'+selectedCity,           // GET запит для отримання переліку вулиць відповідно до вибраного місті
            success: function (response){
                console.log(response.data)
                console.log('hello2', 'address-json/'+selectedCity)
                const addressData = response.data
                addressData.map(item=> {
                    const option = document.createElement('option')
                    option.textContent = item
                    option.setAttribute('class', 'item')
                    option.setAttribute('data', item)           // формування другого випадаючого блоку із переліком вулиць
                    addressDataBox.appendChild(option)
                })
            },
            error: function(error){
                console.log(error)
            }
        })

        })

