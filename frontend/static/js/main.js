// ===== Functions used on multiple pages =====

// Input valdation: accept only numbers
function validateInputNumbers(input) {
    if (input.value <= 0) {
        input.value = null;
    }
}

// Date picker
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('component_updated_date');
    const datePickerToggle = document.getElementById('date-picker-toggle');

    // Initialize Flatpickr with strict formatting
    const flatpickrInstance = flatpickr(dateInput, {
        dateFormat: "Y-m-d H:i",
        allowInput: true,
        clickOpens: false,
        enableTime: true,
        time_24hr: true,
        onClose: function(selectedDates, dateStr) {
            validateDateFormat(dateStr);
        }
    });

    // Open calendar on icon click
    datePickerToggle.addEventListener('click', function() {
        flatpickrInstance.open();
    });

    // Validate manual input
    dateInput.addEventListener('blur', function() {
        validateDateFormat(this.value);
    });

    function validateDateFormat(dateStr) {
        const regex = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/;
        if (!regex.test(dateStr)) {
            alert("Error: Invalid date format. Please use YYYY-MM-DD HH:MM");
            dateInput.value = ''; // Clear the invalid input
            flatpickrInstance.clear(); // Clear Flatpickr's internal date
        }
    }
});


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

// ===== Component overview page functions =====

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the component overview page by looking for the specific element
    const typeSelect = document.getElementById('component_type');
    if (!typeSelect) {
        // Not on component overview page, exit early
        return;
    }

    const serviceIntervalInput = document.getElementById('service_interval');
    const expectedLifetimeInput = document.getElementById('expected_lifetime');

    typeSelect.addEventListener('change', function() {
        const selectedOption = typeSelect.options[typeSelect.selectedIndex];
        const serviceInterval = selectedOption.getAttribute('service_interval');
        const expectedLifetime = selectedOption.getAttribute('expected_lifetime');

        // Update the input fields with the selected option's data attributes
        serviceIntervalInput.value = serviceInterval;
        expectedLifetimeInput.value = expectedLifetime;
    });
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

// Update all page functions to only run when on correct page

