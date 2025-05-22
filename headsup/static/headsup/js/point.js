function update_score(winner) {
    let elements = [document.getElementById("server"), document.getElementById("receiver")];
    let scores = [elements[0].innerHTML, elements[1].innerHTML];
    let loser = 1 - winner;
    let servingElem = document.getElementById("serving_display")

    if (scores[winner] === "0") {
        scores[winner] = "15";
    } 
    else if (scores[winner] === "15") {
        scores[winner] = "30";
    }
    else if (scores[winner] === "30") {
        if (scores[loser] !== "40") {
            scores[winner] = "40";
        }
        else {
            scores[winner] = "Duece";
            scores[loser] = "Duece";
        }
    }
    else if (scores[winner] === "40") {
        if (scores[loser] !== "40") {
            // Game won
            scores[winner] = "0";
            scores[loser] = "0";
            update_game(winner)
            // Swap server and receiver
            let temp = serving;
            serving = receiving;
            receiving = temp;
            servingElem.innerHTML = players[serving];
            updateServingIcon(serving)
        }
        else {
            scores[winner] = "Duece";
            scores[loser] = "Duece";
        }
    }
    else if (scores[winner] === "Duece") {
        if (scores[loser] !== "Adv") {
            scores[winner] = "Adv";
        }
        else {
            scores[loser] = "Duece";
        }
    }
    else if (scores[winner] === "Adv") {
        // Game won
        scores[winner] = "0";
        scores[loser] = "0";
        update_game(winner)
        // Swap server and receiver
        let temp = serving;
        serving = receiving;
        receiving = temp;
        servingElem.innerHTML = players[serving];
        updateServingIcon
    }

    // Update the DOM
    elements[0].innerHTML = scores[0];
    elements[1].innerHTML = scores[1];
}

function update_game(winner) {
    let elements = [
        document.getElementById("player1_game"),
        document.getElementById("player2_game")
    ];
    let scores = [
        parseInt(elements[0].innerHTML.trim()),
        parseInt(elements[1].innerHTML.trim())
    ];
    let loser = 1 - winner
    
    scores[winner] += 1;

    elements[0].innerHTML = scores[0];
    elements[1].innerHTML = scores[1];
    
    if ((scores[winner] === 6) && (scores[loser] < 5)) {
        // Set won
        scores[winner] = "0";
        scores[loser] = "0";
        update_set(winner)
    }
    else if ((scores[winner] === 7) && (scores[loser] === 5)) {
        // Set won
        scores[winner] = "0";
        scores[loser] = "0";
        update_set(winner)
    }

   
}

function update_set(winner) {
    let elements = [
        document.getElementById("player1_set"),
        document.getElementById("player2_set")
    ];
    let scores = [
        parseInt(elements[0].innerHTML.trim()),
        parseInt(elements[1].innerHTML.trim())
    ];
    scores[winner] += 1;
    elements[winner].innerHTML = scores[winner];

    if (matchFormat === 1 && scores[winner] === 1) {
        // Single Set (match is won when a player wins 1 set)
        update_match(winner);
    } else if (matchFormat === 3 && scores[winner] === 2) {
        // Best of 3 (match is won when a player wins 2 sets)
        update_match(winner);
    } else if (matchFormat === 5 && scores[winner] === 3) {
        // Best of 5 (match is won when a player wins 3 sets)
        update_match(winner);
    }
}



function tiebreaker() {

}

function updateServingIcon(serving) {
    document.getElementById("serving_icon_0").style.display = serving === 0 ? "inline" : "none";
    document.getElementById("serving_icon_1").style.display = serving === 1 ? "inline" : "none";
}
