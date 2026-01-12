"use strict";

(function ($) {

    $("#country").change(function () {
        const countryId = $(this).val();
        $.ajax({
            url: ajaxUrls.loadStates, // ✅ dynamic URL
            data: { country_id: countryId },
            success: function (data) {
                $("#state").html('<option value="">Select State</option>');
                $("#city").html('<option value="">Select City</option>');
                data.forEach(function (state) {
                    $("#state").append(`<option value="${state.id}">${state.name}</option>`);
                });
            }
        });
    });

    $("#state").change(function () {
        const stateId = $(this).val();
        $.ajax({
            url: ajaxUrls.loadCities,
            data: { state_id: stateId },
            success: function (data) {
                $("#city").html('<option value="">Select City</option>');
                data.forEach(function (city) {
                    $("#city").append(`<option value="${city.id}">${city.name}</option>`);
                });
            }
        });
    });

})(jQuery);


document.addEventListener('DOMContentLoaded', function() {
    const dateIcon = document.querySelector('.date-icon');
    const dateInput = document.querySelector('.date');

    if (dateIcon && dateInput) {
        dateIcon.addEventListener('click', function() {
            // Modern browsers
            if (typeof dateInput.showPicker === 'function') {
                dateInput.showPicker();
            } else {
                // Fallback: focus the input (works in most browsers)
                dateInput.focus();
            }
        });
    }
});

// for toogle sidebar btn

let sidebarBtn = document.getElementById("toggleSidebarBtn");
let sidebar = document.querySelector(".sidebar");
let content = document.querySelector(".content-container");

sidebarBtn.addEventListener('click', function() {
    // Check computed style in case inline style is not set yet
    let sidebarDisplay = window.getComputedStyle(sidebar).display;

    if (sidebarDisplay === "none") {
        // Show sidebar
        sidebar.style.display = "block";
        content.style.marginLeft = "306px"; // adjust to your sidebar width
    } else {
        // Hide sidebar
        sidebar.style.display = "none";
        content.style.marginLeft = "0";
    }
});



// chart.js

if(document.getElementById('myChart'))
{
    const ctx = document.getElementById('myChart');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Tickets Sold',
                data: [120, 180, 95, 150, 220, 300, 270],
                borderColor: 'blue',
                backgroundColor: 'rgba(0,0,255,0.2)',
                borderWidth: 2,
                tension: 0.3
            }]
        }
    });
}


/*  for the start and end time of movie in theatre
 also crud operation on it */
document.addEventListener('click', function (e) {
    // ADD TIME
    if (e.target.closest('.add-time-btn')) {
        const button = e.target.closest('.add-time-btn');
        const row = button.closest('tr');               // same movie row
        const timeContainer = row.querySelector('.time-container'); // The container where new time inputs will go

        // Create the time row div with start and end time inputs
        const timeRow = document.createElement('div');
        timeRow.classList.add('time-contain', 'd-flex', 'align-items-center', 'justify-content-center');

        // Create the start time input div
        const startTimeDiv = document.createElement('div');
        startTimeDiv.classList.add('start_time_contain');
        const startTimeInput = document.createElement('input');
        startTimeInput.type = 'time';
        startTimeInput.name = 'start_times[]';
        startTimeInput.classList.add('form-control');
        startTimeInput.required = true;
        startTimeDiv.appendChild(startTimeInput);

        // Create the end time input div
        const endTimeDiv = document.createElement('div');
        endTimeDiv.classList.add('end_time_contain');
        const endTimeInput = document.createElement('input');
        endTimeInput.type = 'time';
        endTimeInput.name = 'end_times[]';
        endTimeInput.classList.add('form-control');
        endTimeInput.required = true;
        endTimeDiv.appendChild(endTimeInput);

        // Create the delete button
        const deleteDiv = document.createElement('div');
        deleteDiv.classList.add('time_action');
        const deleteButton = document.createElement('button');
        deleteButton.type = 'button'; // Set to 'button' to prevent form submission
        deleteButton.classList.add('btn', 'btn-sm', 'btn-danger', 'rounded-0');
        deleteButton.innerHTML = '<i class="bi bi-x-lg"></i>';
        deleteButton.addEventListener('click', function() {
            timeContainer.removeChild(timeRow); // Remove the specific time row when clicked
        });
        deleteDiv.appendChild(deleteButton);

        // Append the div elements into the time row
        timeRow.appendChild(startTimeDiv);
        timeRow.appendChild(endTimeDiv);
        timeRow.appendChild(deleteDiv);

        // Append the new time row to the time container
        timeContainer.appendChild(timeRow);
    }

    // REMOVE TIME (Already handled with delete button event above)
});

