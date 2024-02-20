
function fetchTimelineData() {
    return fetch('/fetch_timeline_data') 
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch timeline data');
            }
            return response.json();
        })
        .catch(error => {
            console.error('Error fetching timeline data:', error);
            return [];
        });
}

function displayTimelineData(data) {
    const timelineContainer = document.getElementById('timeline-container');

    timelineContainer.innerHTML = '';

    data.forEach(event => {
        const eventElement = document.createElement('div');
        eventElement.classList.add('event');
        eventElement.innerHTML = `
            <div class="date">${event.date}</div>
            <div class="description">${event.description}</div>
        `;
        timelineContainer.appendChild(eventElement);
    });
}


fetchTimelineData()
    .then(data => {
        displayTimelineData(data);
    });
