$("#hiddenDiv").hide()

function showSpinner() {
    $(".loading").css("visibility", "visible");
}

function hideSpinner() {
    $(".loading").css("visibility", "hidden");
}

function uniqByKeepFirst(a, key) {
    let seen = new Set();
    return a.filter(item => {
        let k = key(item);
        return seen.has(k) ? false : seen.add(k);
    });
}

$("#Menu1").on("change", async function (evt) {
    evt.preventDefault(); 

    showSpinner();

    let vehicle_brand_id = $(this).children(":selected").attr("id");
    console.log(vehicle_brand_id)

        await fetch(`https://www.carboninterface.com/api/v1/vehicle_makes/${vehicle_brand_id}/vehicle_models`, {
            method: 'GET',
            headers: {
                'Authorization': "Bearer <API_KEY>",
                'Content-Type': 'application/json'                   
            }
        }).then(async (res) => {
            let modelArray = []
            let result = await res.json() 
            function getModelData(){
                for (let model in result){
                    const id = result[model].data.id
                    let year = result[model].data.attributes.year
                    let name = result[model].data.attributes.name
                    const yearName = `${year} ${name}`;
                    modelArray.push({a: id, b: yearName})
                    modelArray = uniqByKeepFirst(modelArray, it => it.b)
                }
            return modelArray;
            }
            await getModelData();
            console.log(modelArray)
            async function appendHTMLModelOptions(){
                for (let vehMod in modelArray) {
                    let $modelDropdown = $('#Menu2')
                    let $option = $('<option></option>').text(`${modelArray[vehMod].b}`)
                    $($option).attr('id', `${modelArray[vehMod].a}`)
                    $modelDropdown.append($option)
                }
            }   
            await appendHTMLModelOptions()
            
            $('#hiddenDiv').show()

            hideSpinner();
    }).catch((e) => alert('Could not get models'));
});

$("#Menu2").on("change", function (e) {
    e.preventDefault();
    let vehicle_model_id = $(this).children(":selected").attr("id");
    $("#select-brand-model").attr('action', `/add_my_car/${vehicle_model_id}`)
 
})

