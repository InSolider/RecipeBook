// Get year for footer
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

// Hide or show header
let header = document.querySelector("header");

window.addEventListener("scroll", () => {
    header.classList.toggle("shadow", window.scrollY > 0)
})

$(document).ready(function () {
    $(".filter-item").click(function () {
        const value = $(this).attr("data-filter");
        if (value == "all") {
            $(".post-box").show("1000")
        } else {
            $(".post-box")
                .not("." + value)
                .hide(1000);
            $(".post-box")
                .filter("." + value)
                .show("1000")
        }
    });
    $(".filter-item").click(function () {
        $(this).addClass("active-filter").siblings().removeClass("active-filter")
    });
});

// Rate the recipe
const rate = (rating, recipe_id) => {
    fetch(`/rate/${recipe_id}/${rating}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(rest => {
        window.location.reload();
    })
}

// Sum of ingredients table if element unchecked
const ingrPrices = document.querySelectorAll('.ingr-price');

let total = 0;

ingrPrices.forEach(function (price) {

    const priceValue = parseFloat(price.textContent.match(/\d+(\.\d+)?/)[0]);

    if (!price.parentNode.querySelector('input[type="checkbox"]').checked) {
        total += priceValue;
    }

    price.parentNode.querySelector('input[type="checkbox"]').addEventListener('change', function () {

        if (this.checked) {
            total -= priceValue;
        } else {
            total += priceValue;
        }

        totalPriceElement.textContent = '≈ ' + total.toFixed(2) + ' ₴';

        const row = this.closest('tr');

        const cells = row.querySelectorAll('td');

        cells.forEach(function (cell) {
            cell.style.textDecoration = this.checked ? 'line-through' : 'none';
        }, this);
    });
});

const totalPriceElement = document.getElementById('total-price');
totalPriceElement.textContent = '≈ ' + total.toFixed(2) + ' ₴';