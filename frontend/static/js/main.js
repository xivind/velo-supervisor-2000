// ===== Modal components ====

// Modal for input validation
const validationModalHTML = `
    <div class="modal fade" id="validationModal" tabindex="-1" aria-labelledby="validationModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-danger text-white">
                    <h5 class="modal-title" id="validationModalLabel">⛔ Input validation error</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body" id="validationModalBody"></div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
`;

// Modal for confirmation of action
const confirmModalHTML = `
<div class="modal fade" id="confirmModal" tabindex="-1" aria-labelledby="confirmModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header bg-warning">
                <h5 class="modal-title" id="confirmModalLabel">⚠ Confirm irreversible action</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="confirmModalBody"></div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" id="cancelAction" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-secondary" id="confirmAction" data-bs-dismiss="modal">Proceed</button>
            </div>
        </div>
    </div>
</div>
`;

// Modal for loading status
const loadingModalHTML = `
<div class="modal fade" id="loadingModal" tabindex="-1" aria-labelledby="loadingModalLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content bg-warning-subtle">
            <div class="modal-body text-center">
                <div class="spinner-border text-primary mb-2" role="status"></div>
                <h5 class="mb-2" id="loadingMessage"></h5>
                <p class="mb-0">This may take a moment, hold your horses 🚴</p>
            </div>
        </div>
    </div>
</div>
`;

// ===== Functions used on multiple pages =====

// Toast handler
document.addEventListener('DOMContentLoaded', function() {
    // Get URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const message = urlParams.get('message');
    const success = urlParams.get('success');
    
    // If we have a message, show the toast
    if (message) {
        // console.log('Showing toast:', message, success);  // Debug log
        showToast(message, success === 'True');
    }
});

// Toast behaviour
function showToast(message, success = true) {
    // console.log('Toast function called:', message, success);  // Debug log
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
        delay: 6000
    });
    bsToast.show();
}

// Function to prefill data related to component types
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on either component details or component overview page
    const componentDetailsPage = document.getElementById('component-details');
    const componentOverviewPage = document.getElementById('component-overview');
    
    if (!componentDetailsPage && !componentOverviewPage) {
        // Not on either of the target pages, exit early
        return;
    }

    const typeSelect = document.getElementById('component_type');
    if (!typeSelect) {
        // Component type select not found, exit early
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
            allowInput: false,
            clickOpens: true,
            enableTime: true,
            time_24hr: true,
        });

        // Open calendar on icon click
        datePickerToggle.addEventListener('click', function() {
            flatpickrInstance.open();
        });

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
    // Add confirm modal to the page if it doesn't exist
    if (!document.getElementById('confirmModal')) {
        document.body.insertAdjacentHTML('beforeend', confirmModalHTML);
    }

    document.querySelectorAll('.delete-record').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            event.stopPropagation();
            
            // Get record details
            const recordId = button.dataset.componentType || 
                           button.dataset.componentId || 
                           button.dataset.serviceId || 
                           button.dataset.historyId;

            let tableSelector, recordType;
            
            if (button.dataset.componentType) {
                tableSelector = 'ComponentTypes';
                recordType = 'component type';
            } else if (button.dataset.componentId) {
                tableSelector = 'Components';
                recordType = 'component';
            } else if (button.dataset.serviceId) {
                tableSelector = 'Services';
                recordType = 'service record';
            } else if (button.dataset.historyId) {
                tableSelector = 'ComponentHistory';
                recordType = 'history record';
            }
            
            // Set up the modal
            const modalBody = document.getElementById('confirmModalBody');
            modalBody.innerHTML = `You are about to delete this ${recordType}. This cannot be undone. Do you want to proceed?`;
            const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
            
            // Show the modal
            confirmModal.show();
            
            // Handle confirm action
            document.getElementById('confirmAction').addEventListener('click', function handleConfirm() {
                // Remove the event listener after use
                this.removeEventListener('click', handleConfirm);
                
                // Create and submit the form
                const formData = new FormData();
                formData.append('record_id', recordId);
                formData.append('table_selector', tableSelector);

                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '/delete_record';
                
                for (let [key, value] of formData.entries()) {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = key;
                    input.value = value;
                    form.appendChild(input);
                }
                
                document.body.appendChild(form);
                form.submit();
            }, { once: true }); // Ensure the event listener is only added once
            
            // Handle cancel action (modal will close automatically)
            document.getElementById('cancelAction').addEventListener('click', function handleCancel() {
                this.removeEventListener('click', handleCancel);
            }, { once: true });
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

// Function to clear component overview form
document.addEventListener('DOMContentLoaded', function() {
    const clearFormButton = document.getElementById('clear_form_btn');
    const componentForm = document.getElementById('component_overview_form');
    
    if (!clearFormButton || !componentForm) return;
    
    clearFormButton.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent form submission
        
        // Get all form inputs
        const inputs = componentForm.querySelectorAll('input, select, textarea');
        
        // Clear each input
        inputs.forEach(input => {
            if (input.type === 'text' || input.type === 'number' || input.tagName === 'TEXTAREA') {
                input.value = '';
            } else if (input.type === 'select-one') {
                input.selectedIndex = 0;
            }
        });
        
        // If you have any flatpickr date inputs, clear those too
        const dateInputs = componentForm.querySelectorAll('.flatpickr-input');
        dateInputs.forEach(input => {
            if (input._flatpickr) {
                input._flatpickr.clear();
            }
        });
    });
});

// ===== Component details page functions =====

// Function to control installaion status and bike name
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the component details page
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

// Function for input validation of component details
document.addEventListener('DOMContentLoaded', function() {
    // Get form by ID
    const componentDetailsForm = document.getElementById('component_details_form');
    if (!componentDetailsForm) return;

    // Add validation modal to the page
    document.body.insertAdjacentHTML('beforeend', validationModalHTML);

    // Form submit handler with validation
    componentDetailsForm.addEventListener('submit', function(e) {
        const statusSelect = this.querySelector('#component_installation_status');
        const installationStatus = statusSelect.value;
        const bikeId = this.querySelector('#component_bike_id').value;
        const initialSelectedStatus = statusSelect.options[statusSelect.selectedIndex].defaultSelected ? statusSelect.value : null;
        const dateInput = this.querySelector('#component_updated_date');
        const initialDate = dateInput.defaultValue;
        
        let errorMessage = null;
        if (installationStatus === 'Installed' && !bikeId) {
            errorMessage = 'Status cannot be set to "Installed" if no bike is selected';
            } else if (installationStatus === initialSelectedStatus && dateInput.value !== initialDate) {
                errorMessage = `Status cannot be changed to "${statusSelect.value}" since status is already "${installationStatus}"`;
            } else if (installationStatus !== initialSelectedStatus && dateInput.value === initialDate) {
                errorMessage = `Status cannot be changed unless you also update record date`;
            }

        if (errorMessage) {
            e.preventDefault();
            const modalBody = document.getElementById('validationModalBody');
            modalBody.innerHTML = errorMessage;
            const validationModal = new bootstrap.Modal(document.getElementById('validationModal'));
            validationModal.show();
        }
    });
});

// Function to handle component retirement confirmation
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the component details page
    const componentDetailsPage = document.getElementById('component-details');
    if (!componentDetailsPage) return;

    // Get installation status select
    const installationSelect = document.getElementById('component_installation_status');
    if (!installationSelect) return;

    // Add confirm modal to the page
    document.body.insertAdjacentHTML('beforeend', confirmModalHTML);

    // Initialize modal and tracking variables
    const modalBody = document.getElementById('confirmModalBody');
    modalBody.innerHTML = "You are about to retire this component. This cannot be undone. Do you want to proceed? You still need to save.";
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
    let previousValue = installationSelect.value;

    // Add change event listener to installation status select
    installationSelect.addEventListener('change', function(e) {
        if (this.value === 'Retired') {
            confirmModal.show();
            
            // Handle cancel
            document.getElementById('cancelAction').addEventListener('click', function() {
                installationSelect.value = previousValue;
            }, { once: true });  // Remove listener after first use
            
            // Handle confirm
            document.getElementById('confirmAction').addEventListener('click', function() {
                previousValue = 'Retired';
            }, { once: true });  // Remove listener after first use
        } else {
            previousValue = this.value;
        }
    });
});

// Function to handle editing of service and history records
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the component details page
    if (document.querySelector('h1#component-details') === null) return;

    // Initialize edit modals
    const editServiceModal = new bootstrap.Modal(document.getElementById('editServiceModal'));
    const editHistoryModal = new bootstrap.Modal(document.getElementById('editHistoryModal'));

    // Initialize Flatpickr for edit modals
    const serviceEditDatepicker = flatpickr("#editServiceDate", {
        dateFormat: "Y-m-d H:i",
        enableTime: true,
        time_24hr: true,
        allowInput: false
    });

    const historyEditDatepicker = flatpickr("#editUpdatedDate", {
        dateFormat: "Y-m-d H:i",
        enableTime: true,
        time_24hr: true,
        allowInput: false
    });

    // Handle service record edit button clicks
    document.querySelectorAll('.edit-service-btn').forEach(button => {
        button.addEventListener('click', function() {
            const serviceId = this.dataset.serviceId;
            const serviceDate = this.dataset.serviceDate;
            const serviceDescription = this.dataset.serviceDescription;

            document.getElementById('editServiceId').value = serviceId;
            serviceEditDatepicker.setDate(serviceDate);
            document.getElementById('editServiceDescription').value = serviceDescription;

            editServiceModal.show();
        });
    });

    // Handle history record edit button clicks
    document.querySelectorAll('.edit-history-btn').forEach(button => {
        button.addEventListener('click', function() {
            const historyId = this.dataset.historyId;
            const updatedDate = this.dataset.updatedDate;
            const updateReason = this.dataset.updateReason;

            document.getElementById('editHistoryId').value = historyId;
            historyEditDatepicker.setDate(updatedDate);
            document.getElementById('editUpdateReason').value = updateReason;

            editHistoryModal.show();
        });
    });

    // Calendar icon click handlers
    document.getElementById('edit-service-date-picker-toggle').addEventListener('click', () => {
        serviceEditDatepicker.open();
    });

    document.getElementById('edit-history-date-picker-toggle').addEventListener('click', () => {
        historyEditDatepicker.open();
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

// Function to show spinner while executing API call
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the config page
    if (document.querySelector('h1#config') === null) return;

    // Add loading modal to the page if it doesn't exist
    if (!document.getElementById('loadingModal')) {
        document.body.insertAdjacentHTML('beforeend', loadingModalHTML);
    }

    // Add click handlers to all update buttons
    document.querySelectorAll('.update-button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const endpoint = this.dataset.endpoint;
            const message = this.dataset.message;
            handleUpdate(endpoint, message);
        });
    });
});

function handleUpdate(endpoint, message) {
    // Check if we're on the config page
    if (document.querySelector('h1#config') === null) return;
    
    // Show the loading modal with custom message
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    document.getElementById('loadingMessage').textContent = message;
    loadingModal.show();

    // Make the API call
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            loadingModal.hide();
            showToast(data.message, data.success);
        })
        .catch(error => {
            loadingModal.hide();
            showToast('An error occurred during the update', false);
        });
}