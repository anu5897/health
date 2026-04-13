// GLOBAL
let selectedSymptoms = [];

const container = document.getElementById("symptomTags");
const selectedInput = document.getElementById("selectedSymptoms");
const searchInput = document.getElementById("searchInput");
const suggestionsBox = document.getElementById("suggestions");

// SAFETY CHECK
console.log("Symptoms loaded:", typeof symptomsList !== "undefined");

// RENDER TAGS
function renderTags(list) {
    container.innerHTML = "";

    list.forEach(symptom => {
        const div = document.createElement("div");
        div.className = "tag";
        div.innerText = symptom;

        if (selectedSymptoms.includes(symptom)) {
            div.classList.add("selected");
        }

        div.onclick = () => toggleSymptom(symptom, div);
        container.appendChild(div);
    });

    container.style.opacity = "1";
}

// TOGGLE
function toggleSymptom(symptom, div) {
    if (selectedSymptoms.includes(symptom)) {
        selectedSymptoms = selectedSymptoms.filter(s => s !== symptom);
        div.classList.remove("selected");
    } else {
        selectedSymptoms.push(symptom);
        div.classList.add("selected");
    }

    selectedInput.value = selectedSymptoms.join(", ");
}

// SEARCH
searchInput.addEventListener("input", function () {
    const value = this.value.toLowerCase();

    const filtered = symptomsList.filter(s =>
        s.toLowerCase().includes(value)
    );

    renderTags(filtered);
});

// PREDICT
document.querySelector(".predict-btn").addEventListener("click", function () {
    if (selectedSymptoms.length === 0) {
        alert("Please select at least one symptom!");
        return;
    }

    const encoded = encodeURIComponent(JSON.stringify(selectedSymptoms));
    window.location.href = "/pred?symptoms=" + encoded;
});

// INITIAL LOAD
window.onload = function () {
    if (typeof symptomsList === "undefined") {
        alert("symptoms.js not loaded!");
        return;
    }
    renderTags(symptomsList);
};
