function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

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