// Get year for footer
function getYear() {
  var currentDate = new Date();
  var currentYear = currentDate.getFullYear();
  document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

// Max height for card body
const cardBodies = document.querySelectorAll('.card-body');
let maxHeight = 0;

cardBodies.forEach(cardBody => {
  const height = cardBody.clientHeight;
  if (height > maxHeight) {
    maxHeight = height;
  }
});

cardBodies.forEach(cardBody => {
  cardBody.style.height = `${maxHeight}px`;
});

// Form submit by Enter
const form = document.getElementById('search-form');
const input = document.getElementById('search-input');

input.addEventListener('keydown', function (event) {
  if (event.key === 'Enter') {
    event.preventDefault();
    form.submit();
  }
});

// Filtering by Shuffle JS
var $recipeContainer = $('.recipe-container');
var shuffleInstance = new Shuffle($recipeContainer[0], {
  itemSelector: '.recipe-item'
});

$('.sort-item').on('click', function (e) {
  e.preventDefault();
  var sortByValue;
  sortByValue = $(this).data('sort-by');
  var sortAscending;

  if (sortByValue === 'worth-asc') {
    sortByValue = 'worth';
    sortAscending = false;
  } else if (sortByValue === 'rating-desc') {
    sortByValue = 'rating';
    sortAscending = true;
  } else if (sortByValue === 'new') {
    sortByValue = 'id';
    sortAscending = true;
  } else {
    sortByValue = 'id';
    sortAscending = false;
  }

  shuffleInstance.sort({
    reverse: sortAscending,
    by: function (element) {
      var value = element.getAttribute('data-' + sortByValue);
      if (sortByValue === 'worth') {
        value = parseFloat(value.replace(',', '.'));
      }
      else {
        value = element.getAttribute('data-' + sortByValue);
      }
      return value;
    }
  });
});