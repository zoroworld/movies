document.addEventListener("DOMContentLoaded", function () {
    const seatButtons = document.querySelectorAll(".seat-btn");
    const seatsContainer = document.getElementById("seatsBookedListContainer");

    let selectedSeats = [];

    seatButtons.forEach((btn) => {
        btn.addEventListener("click", function () {
            const seatId = this.getAttribute("data-seat");

            if (selectedSeats.includes(seatId)) {
                selectedSeats = selectedSeats.filter(id => id !== seatId);
                this.classList.remove("btn-success");
                this.classList.add("btn-outline-primary");
            } else {
                selectedSeats.push(seatId);
                this.classList.remove("btn-outline-primary");
                this.classList.add("btn-success");
            }

            // Clear old hidden inputs
            seatsContainer.innerHTML = "";

            // Create one hidden input per seat
            selectedSeats.forEach(id => {
                const input = document.createElement("input");
                input.type = "hidden";
                input.name = "seats_booked";
                input.value = id;
                seatsContainer.appendChild(input);
            });
        });
    });
});
