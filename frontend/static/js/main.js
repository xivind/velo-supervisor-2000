// ===== Modal components for feedback to user ====

let validationModal;
let confirmModal;
let loadingModal;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize modal instances
    validationModal = new bootstrap.Modal(document.getElementById('validationModal'));
    confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
    loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
});


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


// Global date picker function
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
            required: true,
            // Add validation on close
            onClose: function(selectedDates, dateStr, instance) {
                if (!dateStr && dateInput.hasAttribute('required')) {
                    dateInput.classList.add('is-invalid');
                } else {
                    dateInput.classList.remove('is-invalid');
                }
            }
        });

        // Open calendar on icon click
        datePickerToggle.addEventListener('click', function() {
            flatpickrInstance.open();
        });

        // Add form validation if input is required
        if (dateInput.hasAttribute('required')) {
            const form = dateInput.closest('form');
            if (form) {
                form.addEventListener('submit', function(e) {
                    if (!dateInput.value) {
                        e.preventDefault();
                        dateInput.classList.add('is-invalid');
                        return false;
                    }
                });
            }
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
    // Add confirm modal to the page if it doesn't exist

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

// ===== Component details page functions =====

// Function to handle component form status and bike selection synchronization
function initializeComponentForm(formElement) {
    const bikeSelect = formElement.querySelector('[name="component_bike_id"]');
    const installationSelect = formElement.querySelector('[name="component_installation_status"]');
    
    if (!bikeSelect || !installationSelect) {
        console.debug('Form elements not found:', { bikeSelect, installationSelect });
        return;
    }

    // Handle bike selection changes
    bikeSelect.addEventListener('change', function() {
        if (installationSelect.value !== "Retired") {
            if (this.value !== "") {
                installationSelect.value = "Installed";
            } else {
                installationSelect.value = "Not installed";
            }
        }
    });

    // Handle installation status changes
    installationSelect.addEventListener('change', function() {
        if (this.value === "Not installed") {
            bikeSelect.value = "";
        }
    });

    // Initial state check
    if (bikeSelect.value === "" && installationSelect.value !== "Retired") {
        installationSelect.value = "Not installed";
    }
}

// Initialize forms when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Handle create component modal
    const createComponentForm = document.getElementById('component_overview_form');
    if (createComponentForm) {
        initializeComponentForm(createComponentForm);
    }

    // Handle edit status modal
    const componentStatusForm = document.getElementById('component_status_form');
    if (componentStatusForm) {
        initializeComponentForm(componentStatusForm);
    }

    // Also initialize when modals are shown (in case of dynamic content)
    const createComponentModal = document.getElementById('createComponentModal');
    if (createComponentModal) {
        createComponentModal.addEventListener('shown.bs.modal', function() {
            initializeComponentForm(createComponentForm);
        });
    }

    const editComponentStatusModal = document.getElementById('editComponentStatusModal');
    if (editComponentStatusModal) {
        editComponentStatusModal.addEventListener('shown.bs.modal', function() {
            initializeComponentForm(componentStatusForm);
        });
    }
});

// Function for validating component status changes
function addFormValidation(form) {
    if (!form) return;

    form.addEventListener('submit', function(e) {
        const statusSelect = this.querySelector('[name="component_installation_status"]');
        const installationStatus = statusSelect.value;
        const bikeId = this.querySelector('[name="component_bike_id"]').value;
        
        // For status update modal, we need to check additional conditions
        if (form.id === 'component_status_form') {
            const initialSelectedStatus = statusSelect.options[statusSelect.selectedIndex].defaultSelected ? statusSelect.value : null;
            const dateInput = this.querySelector('#component_updated_date');
            const initialDate = dateInput.defaultValue;
            
            if (installationStatus === initialSelectedStatus && dateInput.value !== initialDate) {
                e.preventDefault();
                const modalBody = document.getElementById('validationModalBody');
                modalBody.innerHTML = `Status cannot be changed to "${statusSelect.value}" since status is already "${installationStatus}"`;
                validationModal.show();
                return;
            } else if (installationStatus !== initialSelectedStatus && dateInput.value === initialDate) {
                e.preventDefault();
                const modalBody = document.getElementById('validationModalBody');
                modalBody.innerHTML = `Status cannot be changed unless you also update record date`;
                validationModal.show();
                return;
            }
        }

        // Common validation for both forms
        if (installationStatus === 'Installed' && !bikeId) {
            e.preventDefault();
            const modalBody = document.getElementById('validationModalBody');
            modalBody.innerHTML = 'Status cannot be set to "Installed" if no bike is selected';
            validationModal.show();
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Add validation to both forms
    const componentStatusForm = document.getElementById('component_status_form');
    const componentOverviewForm = document.getElementById('component_overview_form');
    
    addFormValidation(componentStatusForm);
    addFormValidation(componentOverviewForm);

    // Keep the existing retirement confirmation code for the status form
    if (componentStatusForm) {
        const installationSelect = componentStatusForm.querySelector('#component_installation_status');
        let previousValue = installationSelect.value;

        installationSelect.addEventListener('change', function() {
            if (this.value === 'Retired') {
                const modalBody = document.getElementById('confirmModalBody');
                modalBody.innerHTML = "You are about to retire this component. This will lock the component and prevent further editing. Delete the most recent installation record if you wish to unlock the component. Do you want to proceed? You still need to save.";
                confirmModal.show();
                
                document.getElementById('cancelAction').addEventListener('click', function() {
                    installationSelect.value = previousValue;
                }, { once: true });
                
                document.getElementById('confirmAction').addEventListener('click', function() {
                    previousValue = 'Retired';
                }, { once: true });
            } else {
                previousValue = this.value;
            }
        });
    }
});

// Function to handle service records and history records
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the component details page
    if (document.querySelector('h1#component-details') === null) return;

    // Initialize modals
    const serviceRecordModal = new bootstrap.Modal(document.getElementById('serviceRecordModal'));
    const editHistoryModal = new bootstrap.Modal(document.getElementById('editHistoryModal'));

    // Get component ID from the page context
    const currentComponentId = document.getElementById('serviceComponentId').value;

    // Initialize Flatpickr for service modal
    const serviceDatepicker = flatpickr("#serviceDate", {
        dateFormat: "Y-m-d H:i",
        enableTime: true,
        time_24hr: true,
        allowInput: false
    });

    // Initialize Flatpickr for history modal
    const historyEditDatepicker = flatpickr("#editUpdatedDate", {
        dateFormat: "Y-m-d H:i",
        enableTime: true,
        time_24hr: true,
        allowInput: false
    });

    // Handle "New Service" button click
    document.querySelector('[data-bs-target="#serviceRecordModal"]').addEventListener('click', function() {
        // Set up modal for creating new service
        document.getElementById('serviceRecordModalLabel').textContent = 'New Service Record';
        document.getElementById('serviceRecordForm').action = '/add_service_record';
        
        // Ensure component_id is set for new service
        document.getElementById('serviceComponentId').value = currentComponentId;
        
        // Clear other form fields
        document.getElementById('serviceId').value = '';
        serviceDatepicker.clear();
        document.getElementById('serviceDescription').value = '';
        
        serviceRecordModal.show();
    });

    // Handle service record edit button clicks
    document.querySelectorAll('.edit-service-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Set up modal for editing service
            document.getElementById('serviceRecordModalLabel').textContent = 'Edit Service Record';
            document.getElementById('serviceRecordForm').action = '/update_service_record';
            
            // Fill in the form with existing data
            document.getElementById('serviceComponentId').value = this.dataset.componentId;
            document.getElementById('serviceId').value = this.dataset.serviceId;
            serviceDatepicker.setDate(this.dataset.serviceDate);
            document.getElementById('serviceDescription').value = this.dataset.serviceDescription;

            serviceRecordModal.show();
        });
    });

    // Handle history record edit button clicks
    document.querySelectorAll('.edit-history-btn').forEach(button => {
        button.addEventListener('click', function() {
            const historyId = this.dataset.historyId;
            const updatedDate = this.dataset.updatedDate;
            const componentId = this.dataset.componentId;

            document.getElementById('editHistoryComponentId').value = componentId;
            document.getElementById('editHistoryId').value = historyId;
            historyEditDatepicker.setDate(updatedDate);

            editHistoryModal.show();
        });
    });

    // Calendar icon click handlers
    document.getElementById('service-date-picker-toggle').addEventListener('click', () => {
        serviceDatepicker.open();
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

// ===== Footer page functions =====

// Modern performance timing code
window.addEventListener('load', () => {
    function getDetailedTiming() {
        const perf = performance.getEntriesByType('navigation')[0];
        
        // Calculate all the phases using modern API
        const timings = {
            total: perf.loadEventEnd / 1000,
            network: perf.responseEnd / 1000,
            serverResponse: (perf.responseEnd - perf.requestStart) / 1000,
            domProcessing: (perf.domComplete - perf.responseEnd) / 1000,
            loadEvent: (perf.loadEventEnd - perf.loadEventStart) / 1000
        };

        // Validate timings
        for (let phase in timings) {
            if (timings[phase] < 0) {
                console.warn(`Negative timing for ${phase}: ${timings[phase]}`);
                return null;
            }
        }

        return timings;
    }

    // Get the timing element
    const timeElement = document.getElementById('log-fetch-time');
    
    // Check if the Performance API is available and has navigation timing
    if (performance.getEntriesByType && performance.getEntriesByType('navigation').length > 0) {
        // Wait a short moment to ensure timing data is available
        setTimeout(() => {
            const timings = getDetailedTiming();
            
            if (timings) {
                // Log detailed timings for debugging
                console.debug('Page Load Timings:', timings);
                
                // Display the total time with 2 decimals
                timeElement.textContent = timings.total.toFixed(2);
            } else {
                console.error('Invalid timing data received');
                timeElement.textContent = 'Timing unavailable';
            }
        }, 0);
    } else {
        console.error('Modern Performance API not supported');
        timeElement.textContent = 'Timing unavailable';
    }
});