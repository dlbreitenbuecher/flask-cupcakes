'use strict';
// Collect all cupcake instances from cupcakes api
async function getCupcakes() {
    let response = await axios.get('/api/cupcakes');
    return response.data;
}

// Create list elements to display each cupcake instance

async function listCupcakes() {
    let response = await getCupcakes();
    console.log('response', response)

    // cupcakes = JSON.parse(response.data)
}

getCupcakes();


// $(document).ready(function(){
//     console.log('ready!');
// })

$(document).ready(listCupcakes);
