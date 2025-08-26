document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".card").forEach(card => {
        card.addEventListener("click", function () {
            let value = this.dataset.value;

            fetch(submitVoteUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken  // Django needs this
                },
                body: JSON.stringify({ value: value })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.querySelectorAll(".card").forEach(c => c.classList.remove("selected"));
                    document.querySelector(`.card[data-value='${data.vote}']`).classList.add("selected");
                } else {
                    console.error("Vote failed:", data.error);
                }
            })
            .catch(err => console.error("Fetch error:", err));
        });
    });
});