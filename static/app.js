'use strict';

// Collect all cupcake instances from cupcakes api
async function getCupcakes() {
    let response = await axios.get('/api/cupcakes');
    return response.data;
}

// Create linked-list that displays each cupcake instance
async function listCupcakes() {
    $('#cupcake-list').empty();

    let response = await getCupcakes();
    let cupcakes = response.cupcakes;
    console.log('response', response.cupcakes);

    for (let cupcake of cupcakes) {
        let $link = $('<a>').attr('href', `/cupcake/${cupcake.id}`).text(`${cupcake.flavor}`);
        let $listElement = $('<li>').append($link);
        $('#cupcake-list').append($listElement);
    }
}

$(document).ready(listCupcakes());


// Creates a new cupcake after form submission
async function bakeCupcake() {

    let flavor = $('#flavor').val();
    let size = $('#size').val();
    let rating = $('#rating').val();
    let image = $('#image').val();
    // console.log('form object', { flavor, size, rating, image });

    await axios.post('/api/cupcakes', { flavor, size, rating, image });
    await listCupcakes();
}

// Event handler for backCupcake
$('#create-cupcake-form').on('click', 'button', function(evt){
    evt.preventDefault();
    bakeCupcake();
})
