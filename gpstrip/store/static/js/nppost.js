
    const cityInput = document.getElementById('city-select') // ініціалізація змінної за елементом id="city-select" checkout.html
    const addressDataBox = document.getElementById('address-select')
    const addressInput = document.getElementById('address-select')
    const addressText = document.getElementById('address-text')

    $.ajax({                                                          // функція виводу переліку міст першого випадаючого списку на сторінці checkout.html
        type: 'GET',
        url: '/city-json/',                                             // отримання переліку міст для виводу у випадаючому списку
        success: function (response){
            const cityData = response.data                               // інінціалізація перемінної отриманого масиву переліку міст та  ref номера
            cityData.map(item=>{                                           // ініціалізація перемінної із переліком міст
                const option = document.createElement('option')   // ініціалізація перемінної блоку html для формування видачі переліку міст у випадаючому списку
                option.textContent = item.name                              // формування блоку випадаючого списку із назвами міст
                option.setAttribute('value', item.ref)     // формування блоку атрибуту HTML блоку із велииною ref номера
                cityInput.appendChild(option)
            })
        },
        error: function(error){
            console.log(error)
        }
})
    cityInput.addEventListener('change', e=>{
        const selectedCity = e.target.value                // ініціалізація перемінної із вибраним містом, та атримбутом ref номера
        addressDataBox.innerHTML = ''
        addressText.textContent = 'Виберіть відділення'
        $.ajax({                                         // функція формування переліку вулиць випадаючого списку
            type: "GET",
            url: '/address-json/'+selectedCity,           // GET запит для дачі вибраного міста для фомування запиту отримання переліку вулиць відповідно до вибраного місті
            success: function (response){
                const addressData = response.data         // інінціалізація перемінної із отриманими даними від запиту вулиць відповідно до міста
                addressData.map(item=> {                   // формування блоку HTML коду
                    const option = document.createElement('option')  // ініціалізація перемінної блоку html для формування видачі переліку вулиць
                    option.textContent = item            // ініціалізація перемінної блоку html для формування видачі переліку вулиць по назві
                    option.setAttribute('class', 'item')
                    option.setAttribute('data', item)           // формування  випадаючого блоку із переліком вулиць
                    addressDataBox.appendChild(option)
                })
            },
            error: function(error){
                console.log(error)
            }
        })
        })

