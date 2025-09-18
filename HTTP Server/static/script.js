const lstPlayer = document.getElementById("lstPlayers");
const addPlayer = document.getElementById("btn");
const txtPlayer = document.getElementById("txtPlayer");

fetch("/playersList")
  .then(response => response.json())
  .then(jsonResponse => {
    lstPlayer.innerHTML = ""; 
    jsonResponse.forEach(player => {
      let option = document.createElement("option");
      option.textContent = player;
      lstPlayer.appendChild(option);
    });
  });

addPlayer.addEventListener("click", () => {
    let player = txtPlayer.value.trim();
    if (player === "") return alert("Enter a valid player name");

    fetch("/playersList", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `addPlayer=${encodeURIComponent(player)}`
    })
    .then(response => response.json())
    .then(jsonResponse => {
        alert(jsonResponse.massage); 
        txtPlayer.value = "";        
        loadPlayers();               
    });
});