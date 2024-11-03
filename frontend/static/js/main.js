// ===== Functions used on multiple pages =====

// Input valdation function: accept only numbers
function validateInputNumbers(input) {
    if (input.value <= 0) {
        input.value = null;
    }
}

// Date picker function
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a page with either of the date inputs
    const updateDateInput = document.getElementById('component_updated_date');
    const serviceDateInput = document.getElementById('service_date');
    
    // Exit if neither element exists
    if (!updateDateInput && !serviceDateInput) {
        return;
    }

    // Use whichever date input exists
    const dateInput = updateDateInput || serviceDateInput;
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

// Function to delete records
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-record').forEach(button => {
        button.addEventListener('click', () => {
            const formData = new FormData();
            const recordId = button.dataset.componentType || button.dataset.componentId;
            const tableSelector = button.dataset.componentType ? 'ComponentTypes' : 'Components';
            
            formData.append('record_id', recordId);
            formData.append('table_selector', tableSelector);

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

// Function to filter component tables
document.addEventListener('DOMContentLoaded', function() {
    const componentsTable = document.getElementById('componentsTable');
    if (!componentsTable) return; // Exit if the components table doesn't exist

    const filterSwitches = document.querySelectorAll('.filter-switch');
    const componentRows = componentsTable.querySelectorAll('tbody tr');

    function updateVisibility() {
        const showInstalled = document.getElementById('showInstalledComponents').checked;
        const showNotInstalled = document.getElementById('showNotInstalledComponents').checked;
        const showRetired = document.getElementById('showRetiredComponents').checked;

        componentRows.forEach(row => {
            const statusCell = row.querySelector('td:nth-child(4)'); // Assuming status is in the 4th column
            if (statusCell) {
                const status = statusCell.textContent.trim();
                if (
                    (status.includes('⚡') && showInstalled) ||
                    (status.includes('💤') && showNotInstalled) ||
                    (status.includes('⛔') && showRetired) 
                ) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            }
        });
    }

    filterSwitches.forEach(switchElement => {
        switchElement.addEventListener('change', updateVisibility);
    });

    // Initial visibility update
    updateVisibility();
});

// Script to sort component table
document.addEventListener('DOMContentLoaded', function() {
    const table = document.querySelector('table');
    const headers = table.querySelectorAll('th');
    const tableBody = table.querySelector('tbody');
    const rows = tableBody.querySelectorAll('tr');

    // Sorting function
    const sortColumn = (index, asc = true) => {
        const nodeList = Array.from(rows);
        const compare = (rowA, rowB) => {
            const cellA = rowA.querySelectorAll('td')[index].innerText;
            const cellB = rowB.querySelectorAll('td')[index].innerText;
            return asc ? (cellA > cellB ? 1 : -1) : (cellA < cellB ? 1 : -1);
        };
        nodeList.sort(compare);
        nodeList.forEach(node => tableBody.appendChild(node));
    }

    // Add click event to table headers
    headers.forEach(header => {
        header.addEventListener('click', () => {
            const columnIndex = header.cellIndex;
            const isAscending = !header.classList.contains('sorted-asc');
            
            // Remove sorted classes from all headers
            headers.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
            
            // Add appropriate class to clicked header
            header.classList.add(isAscending ? 'sorted-asc' : 'sorted-desc');
            
            sortColumn(columnIndex, isAscending);
        });
    });
});

// ===== Bike overview page functions =====

// Function to update visibility of bike cards
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

// Function to prefill data related to component types
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

// Function to modify component types
window.addEventListener('DOMContentLoaded', function() {
    // Modify record function: get all modify record buttons
    const modifyRecordButtons = document.querySelectorAll('.modify-record');

    // Add a click event listener to each button
    modifyRecordButtons.forEach(button => {
        button.addEventListener('click', () => {
            const rowId = button.dataset.rowId;
            modifyRecord(rowId);
        });
    });

    // Define the modifyRecord function
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

// ===== Configuration page functions =====

// Function for fetching logs
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



