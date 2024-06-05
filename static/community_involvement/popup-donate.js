    let donates = document.querySelectorAll('.show-donate');

$.each(donates, function (index, element) {
    element.addEventListener('click', () => {
        $('.donate-popup').removeClass('none');
        console.log(element.value)
        $('.title').val(element.value)
    })
})

$('.close-popup').click(function () {
    $('.donate-popup').addClass('none');
})

let mode = document.querySelectorAll('#mode');

function loadMode() {
    $('.mode1').css("display", "grid");
}

loadMode()

$.each(mode, function (index, element) {
    element.addEventListener('click', () => {
        if (element.value == "mode1") {
            $('.mode1').css("display", "grid");
            $('.mode2').css("display", "none");
            $('.mode3').css("display", "none");
        }

        if (element.value == "mode2") {
            $('.mode1').css("display", "none");
            $('.mode2').css("display", "grid");
            $('.mode3').css("display", "none");
        }

        if (element.value == "mode3") {
            $('.mode1').css("display", "none");
            $('.mode2').css("display", "none");
            $('.mode3').css("display", "grid");
        }
    })
})

let amount_gcash = 0

$('.amount_gcash').on('change', function() {
    amount_gcash = $(this).find(":selected").val()
});


// Gcash
let gcash_number = document.querySelectorAll('#gcash_number');
let gcash_name = document.querySelectorAll('#gcash_name');

let gcash_num = 0
let gcash_n = ""

$.each(gcash_number, function (index, element) {
    element.addEventListener('keyup', () => {
        gcash_num = element.value
    })
})

$.each(gcash_name, function (index, element) {
    element.addEventListener('keyup', () => {
        gcash_n = element.value
    })
})

$('.nextGcash').click(function () {
    // console.log(amount_gcash)
    // console.log(gcash_num)
    // console.log(gcash_n)

    if (gcash_n == "" || amount_gcash == "" || gcash_num  == "") {
        alert("Please fill in all the required fields");
    } else {
        $('.paymaya_mode').css("display", "none")
        $('.volunteer_mode').css("display", "none")
        
        $('.gcash-form').css("display", "none");        
        $('.gcash-img').css("display", "grid");


    //     // $('.donate-popup h4').css("display", "none");
    //     // $('.mode').css("display", "none");

    //     // $('.donate-popup h1').css("display", "none");
    }
})

$('.close').click(function () {
    window.location.reload();
})