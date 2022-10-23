$("#hiddenDiv").hide()

$("#Menu1").on("change", async function (evt) {
    evt.preventDefault(); 
    
    let vehicle_brand_id = $(this).children(":selected").attr("id");
    console.log(vehicle_brand_id)

        await fetch(`https://www.carboninterface.com/api/v1/vehicle_makes/${vehicle_brand_id}/vehicle_models`, {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer <authKey>',
                'Content-Type': 'application/json'                   
            }
        }).then(async (res) => {
            let modelList = []
            let result = await res.json() 
            function getModelData(){
                for (let model in result){
                    const id = result[model].data.id
                    const year = result[model].data.attributes.year
                    const name = result[model].data.attributes.name
                    modelList.push([id, year, name])
                }
            return modelList;
            }
            await getModelData();
            console.log(modelList)
            async function appendHTMLModelOptions(){
                for (let vehMod in modelList) {
                    let $modelDropdown = $('#Menu2')
                    let $option = $('<option></option>').text(`${modelList[vehMod][1]} ${modelList[vehMod][2]}`)
                    $($option).attr('id', `${modelList[vehMod][0]}`)
                    $modelDropdown.append($option)
                }
            }   
            await appendHTMLModelOptions()
        
            $('#hiddenDiv').show() 
    }).catch((e) => alert('Could not get models'));
});

$("#Menu2").on("change", function (e) {
    e.preventDefault();
    let vehicle_model_id = $(this).children(":selected").attr("id");
    $("#select-brand-model").attr('action', `/add_my_car/${vehicle_model_id}`)
 
})

