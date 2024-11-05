// ===== Functions used on multiple pages =====

// Toast handler
document.addEventListener('DOMContentLoaded', function() {
    // Get URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const message = urlParams.get('message');
    const success = urlParams.get('success');
    
    // If we have a message, show the toast
    if (message) {
        console.log('Showing toast:', message, success);  // Debug log
        showToast(message, success === 'True');
    }
});

// Toast behaviour
function showToast(message, success = true) {
    console.log('Toast function called:', message, success);  // Debug log
    const toast = document.getElementById('messageToast');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    
    // Set title and message
    toastTitle.textContent = success ? 'Success' : 'Error';
    toastMessage.textContent = message;
    
    // Set bootstrap classes based on success/error
    toast.classList.remove('bg-danger', 'text-white', 'bg-success');
    if (!success) {
        toast.classList.add('bg-danger', 'text-white');
    } else {
        toast.classList.add('bg-success', 'text-white');
    }
    
    // Create and show the toast
    const bsToast = new bootstrap.Toast(toast, {
        animation: true,
        autohide: true,
        delay: 5000
    });
    bsToast.show();
}

// Input valdation function: accept only numbers
function validateInputNumbers(input) {
    if (input.value <= 0) {
        input.value = null;
    }
}

// Function to prefill data related to component types
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on page that need automatic prefill of component types
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

// Date picker function
document.addEventListener('DOMContentLoaded', function() {
    // Function to initialize a single date picker
    function initializeDatePicker(inputId, toggleId) {
        const dateInput = document.getElementById(inputId);
        const datePickerToggle = document.getElementById(toggleId);
        
        if (!dateInput || !datePickerToggle) {
            return;
        }

        // Initialize Flatpickr with strict formatting
        const flatpickrInstance = flatpickr(dateInput, {
            dateFormat: "Y-m-d H:i",
            allowInput: true,
            clickOpens: false,
            enableTime: true,
            time_24hr: true,
            onClose: function(selectedDates, dateStr) {
                validateDateFormat(dateStr, dateInput, flatpickrInstance);
            }
        });

        // Open calendar on icon click
        datePickerToggle.addEventListener('click', function() {
            flatpickrInstance.open();
        });

        // Validate manual input
        dateInput.addEventListener('blur', function() {
            validateDateFormat(this.value, dateInput, flatpickrInstance);
        });
    }

    function validateDateFormat(dateStr, input, picker) {
        const regex = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/;
        if (!regex.test(dateStr)) {
            alert("Error: Invalid date format. Please use YYYY-MM-DD HH:MM");
            input.value = ''; // Clear the invalid input
            picker.clear(); // Clear Flatpickr's internal date
        }
    }

    // Initialize all date pickers
    const datePickerConfigs = [
        { inputId: 'component_updated_date', toggleId: 'update-date-picker-toggle' },
        { inputId: 'service_date', toggleId: 'service-date-picker-toggle' }
    ];

    datePickerConfigs.forEach(config => {
        initializeDatePicker(config.inputId, config.toggleId);
    });
});

// Function to delete records
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-record').forEach(button => {
        button.addEventListener('click', (event) => {
            // Prevent any form submission and default button behavior
            event.preventDefault();
            event.stopPropagation();
            
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
                    // Redirect based on what was deleted
                    const redirectUrl = tableSelector === 'ComponentTypes' 
                        ? '/component_types_overview' 
                        : '/component_overview';
                    window.location.href = redirectUrl;
                }
            })
            .catch(error => console.error('Backend error:', error));
        });
    });
});

// Function for component table filtering
document.addEventListener('DOMContentLoaded', function() {
    const componentsTable = document.getElementById('componentsTable');
    if (!componentsTable) return;

    const filterSwitches = document.querySelectorAll('.filter-switch');
    const componentRows = componentsTable.querySelectorAll('tbody tr');

    function updateComponentRowVisibility() {
        // Get switch states
        const showInstalled = document.getElementById('showInstalledComponents').checked;
        const showRetired = document.getElementById('showRetiredComponents').checked;
        const notInstalledSwitch = document.getElementById('showNotInstalledComponents');
        const showNotInstalled = notInstalledSwitch ? notInstalledSwitch.checked : false;

        componentRows.forEach(row => {
            const statusCell = row.querySelector('td:nth-child(4)');
            if (statusCell) {
                const status = statusCell.textContent.trim();
                const shouldShow = (
                    (status.includes('⚡') && showInstalled) ||
                    (status.includes('💤') && showNotInstalled) ||
                    (status.includes('⛔') && showRetired)
                );
                row.style.display = shouldShow ? '' : 'none';
            }
        });
    }

    // Add event listeners
    filterSwitches.forEach(switchElement => {
        switchElement.addEventListener('change', updateComponentRowVisibility);
    });

    // Initial visibility update
    updateComponentRowVisibility();
});


// ===== Bike overview page functions =====

// Function to update visibility of bike cards
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the bike overview page
    if (document.querySelector('h1#bike-overview') === null) return;
    
    const showRetiredBikesSwitch = document.getElementById('showRetiredBikes');
    const bikeCards = document.querySelectorAll('.card[data-bike-status]');

    function updateBikeVisibility() {
        bikeCards.forEach(card => {
            if (card.dataset.bikeStatus === 'True') {
                card.closest('.col-md-4').style.display = showRetiredBikesSwitch.checked ? '' : 'none';
            }
        });
    }

    // Initial state: hide retired bikes
    updateBikeVisibility();

    // Update visibility when switch is toggled
    showRetiredBikesSwitch.addEventListener('change', updateBikeVisibility);
});


// ===== Component overview page functions =====

// Script to sort component table
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the component overview page
    if (document.querySelector('h1#component-overview') === null) return;
    
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

// ===== Component details page functions =====

// Function to validate input
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the bike overview page
    if (document.querySelector('h1#component-details') === null) return;
    
    const bikeSelect = document.getElementById('component_bike_id');
    const installationSelect = document.getElementById('component_installation_status');

    bikeSelect.addEventListener('change', function() {
        if (installationSelect.value !== "Retired") {
            if (this.value !== "") {
                installationSelect.value = "Installed";
            } else {
                installationSelect.value = "Not installed";
            }
        }
    });

    installationSelect.addEventListener('change', function() {
        if (this.value === "Not installed") {
            bikeSelect.value = "";
        }
    });

    // Initial check on page load
    if (bikeSelect.value === "" && installationSelect.value !== "Retired") {
        installationSelect.value = "Not installed";
    }
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



