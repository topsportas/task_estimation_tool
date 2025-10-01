document.addEventListener("DOMContentLoaded", function () {

    // Card click handler
    document.querySelectorAll(".card").forEach(card => {
        card.addEventListener("click", function () {
            let value = this.dataset.value;

            fetch(submitVoteUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                credentials: "same-origin",
                body: JSON.stringify({ value: value })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Highlight selected card
                    document.querySelectorAll(".card").forEach(c => c.classList.remove("selected"));
                    document.querySelector(`.card[data-value='${data.vote}']`).classList.add("selected");
                    updateRoom(); // Immediately refresh players after vote
                } else {
                    console.error("Vote failed:", data.error);
                }
            })
            .catch(err => console.error("Fetch error:", err));
        });
    });

    // Function to refresh player list
    function updateRoom() {
        const roomData = document.getElementById("room-data");
        const roomCode = roomData.dataset.code;

        fetch(`/room/${roomCode}/state/`, { cache: "no-store" })
            .then(response => response.json())
            .then(data => {
                const list = document.getElementById("players-list");
                list.innerHTML = "";

                data.players.forEach(p => {
                    const li = document.createElement("li");
                    li.textContent = p.name + (p.vote ? " -> " + p.vote : "");
                    list.appendChild(li);
                });
            })
            .catch(err => console.error("Fetch error:", err));
    }
});
