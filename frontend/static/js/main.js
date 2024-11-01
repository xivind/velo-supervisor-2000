// ===== Functions used on multiple pages =====

// Input valdation: accept only numbers
function validateInputNumbers(input) {
    if (input.value <= 0) {
        input.value = null;
    }
}

// ===== Bike overview page functions =====

// Function to update visibility
document.addEventListener('DOMContentLoaded', function() {
    const showRetiredBikesSwitch = document.getElementById('showRetiredBikes');
    const bikeCards = document.querySelectorAll('.card[data-bike-status]');

    function updateVisibility() {
        bikeCards.forEach(card => {
            if (card.dataset.bikeStatus === 'True') {
                card.closest('.col-md-4').style.display = showRetiredBikesSwitch.checked ? '' : 'none';
            }
        });
    }

    // Initial state: hide retired bikes
    updateVisibility();

    // Update visibility when switch is toggled
    showRetiredBikesSwitch.addEventListener('change', updateVisibility);
});

// ===== Component types page functions =====

// Modify record function: Wait for the page to load before initiating modify button
window.addEventListener('DOMContentLoaded', function() {
    // Modify record function: get all modify record buttons
    const modifyRecordButtons = document.querySelectorAll('.modify-record');

    // Modify record function: add a click event listener to each button
    modifyRecordButtons.forEach(button => {
        button.addEventListener('click', () => {
            const rowId = button.dataset.rowId;
            modifyRecord(rowId);
        });
    });

    // Modify record function: define the modifyRecord function
    function modifyRecord(rowId) {
        const row = document.querySelector(`tr[data-row-id="${rowId}"]`);
        if (row) {
            const componentType = row.cells[0].textContent;
            const expectedLifetime = row.cells[1].textContent;
            const serviceInterval = row.cells[2].textContent;

            document.getElementById('component_type').value = componentType;
            document.getElementById('expected_lifetime').value = expectedLifetime;
            document.getElementById('service_interval').value = serviceInterval;
        } else {
            console.error(`Row with ID ${rowId} not found.`);
        }
    }
});

// Script to delete records MIGHT MOVE THIS TO GENERAL, BUT NEEDS TO BE GENERIC
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-record').forEach(button => {
        button.addEventListener('click', () => {
            const formData = new FormData();
            formData.append('record_id', button.dataset.componentType);
            formData.append('table_selector', 'ComponentTypes');

            fetch('/delete_record', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    console.log('Backend received data');
                    window.location.reload();
                }
            })
            .catch(error => console.error('Backend error:', error));
        });
    });
});

// ===== Configuration page functions =====

// Log Fetching Functions
document.addEventListener('DOMContentLoaded', function() {
    // First check if we're on the page with logs
    const logList = document.getElementById('log-entries');
    if (!logList) {
        // If the log-entries element doesn't exist, just return
        return;
    }

    function fetchLogs() {
        fetch('/get_filtered_log')
            .then(response => response.json())
            .then(data => {
                logList.innerHTML = '';
                data.logs.reverse().forEach(log => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item';
                    if (log.includes('WARNING')) {
                        li.classList.add('list-group-item-warning');
                    } else if (log.includes('ERROR')) {
                        li.classList.add('list-group-item-danger');
                    } else {
                        li.classList.add('list-group-item-light');
                    }
                    li.textContent = log;
                    logList.appendChild(li);
                });
            })
            .catch(error => console.error('Error fetching logs:', error));
    }

    fetchLogs();
});