document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  form.addEventListener("submit", (e) => {
    const checkIn = new Date(form.check_in.value);
    const checkOut = new Date(form.check_out.value);
    if (checkOut <= checkIn) {
      alert("Check-out must be after check-in");
      e.preventDefault();
    }
  });
});
