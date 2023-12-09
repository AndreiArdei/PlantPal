$(document).ready(function () {
    const urlParams = new URLSearchParams(window.location.search);
    let filename = urlParams.get('name');
    console.log(filename);

    fetch('/API/classify?filename=' + filename)
        .then(r => r.json())
        .then(data => {
            console.log(data);
            if (data === 'unknown') {
                createUnknown();
                fillSelect();
            } else {
                createKnown(data[0]);
            }
        });
});


function createUnknown() {
    document.getElementById('container').style.width = 'auto';
    const form = document.getElementById('classForm');
    const h4 = document.createElement('h4');
    h4.classList.add("mb-2");
    h4.textContent = 'Sorry we were not able to identify your plant';

    document.getElementById('cardContainer').insertBefore(h4, form);

    form.innerHTML = "" +
        "<div class='card float-left'>" +
        "   <div class='card-body text-justify'>" +
        "       <p class='mb-0 text-muted'> You can select from one of our predefined plants:</p><br>" +
        "       <select name='selectUnkn' form='classForm' id='unknownSelect' class='select2-container' size='8'></select>" +
        "   </div>" +
        "</div>" +
        "<div class='card float-right'>" +
        "   <div class='card-body text-left'>" +
        "       <p class='mb-0 text-muted'>Or you could fill in the details manually</p><br>" +
        "       <label for='family'>Family of the plant</label>" +
        "       <input id='family' class='form-control' name='family' placeholder='Plant family'>" +
        "" +
        "       <div class='row'>" +
        "       <div class='col-md-9'>" +
        "            <label for='sunIntens'>Sun intensity</label>" +
        "            <input name='reqSun' id='sunIntens' type='range' class='custom-range' min='0' max='5' step='1' value='0' oninput=\"document.getElementById('vSun').value = this.value\">" +
        "           " +
        "            <label for='waterAmt'>Water Amount</label>" +
        "            <input name='reqWat' id='waterAmt' type='range' class='custom-range' min='0' max='10' step='1' value='0' oninput=\"document.getElementById('vWater').value = this.value\">" +
        "         </div>" +
        "             <div class='col-md-2'>" +
        "           <output id='vSun' class='form-control input-group-sm' style='margin: 0.5em'>0</output>" +
        "           <output id='vWater' class='form-control input-group-sm' style='margin: 0.5em'>0</output>" +
        "       </div>" +
        "</div>" +
        "   </div>" +
        "</div>";
}

function fillSelect() {
    fetch('/API/Plants')
        .then(r => r.json())
        .then(data => {
            console.log(data);
            for(let d of data) {
                let opt = document.createElement("option");
                opt.value = d.Name;
                opt.innerText = d.Name;
                opt.classList.add('select-label');
                document.getElementById('unknownSelect').append(opt);
            }
        })
}

function createKnown(classification) {
    document.getElementById('classForm').innerHTML = "" +
        "<h4 class='mb-2'>We believe that your plant is a " + classification + "</h4>" +
        "<p class='mb-0 text-muted'> Is this not the case? Then press <a onclick='createUnknown()'>here</a></p>";
}

$('')