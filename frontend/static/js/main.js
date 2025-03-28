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
    const toast = document.getElementById('messageToast');
    const toastHeader = toast.querySelector('.toast-header');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    const progressBar = document.getElementById('toastProgressBar'); // Get the progress bar

    toastTitle.textContent = success ? 'Success' : 'Error';
    toastMessage.textContent = message;

    // Reset all classes first
    toast.classList.remove('border-success', 'border-danger');
    toastHeader.classList.remove('bg-success', 'bg-danger', 'text-white');

    // Set appropriate styling based on success/error
    if (success) {
        toast.classList.add('border-success');
        toastHeader.classList.add('bg-success', 'text-white');
    } else {
        toast.classList.add('border-danger');
        toastHeader.classList.add('bg-danger', 'text-white');
    }

    const bsToast = new bootstrap.Toast(toast, {
        animation: true,
        autohide: true,
        delay: 6000
    });

    bsToast.show();

    // Progress Bar Countdown
    let remainingTime = 6000;
    const interval = 10;
    const step = (interval / remainingTime) * 100;
    let currentWidth = 100;

    const countdownInterval = setInterval(() => {
        currentWidth -= step;
        if (currentWidth <= 0) {
            clearInterval(countdownInterval);
            progressBar.style.width = '0%';
        } else {
            progressBar.style.width = `${currentWidth}%`;
        }
    }, interval);

    toast.addEventListener('hidden.bs.toast', () => {
        clearInterval(countdownInterval);
    });
}

// Function to prefill data related to component types
document.addEventListener('DOMContentLoaded', function() {
    // Get all component_type selects on the page
    const typeSelects = document.querySelectorAll('select[id^="component_type"]');
    
    if (!typeSelects.length) {
        // No component type selects found, exit early
        return;
    }

    // For each component type select, set up the change handler
    typeSelects.forEach(function(typeSelect) {
        // Find the closest form to locate related inputs
        const form = typeSelect.closest('form');
        if (!form) return;
        
        // Find the related inputs within the same form
        const serviceIntervalInput = form.querySelector('input[id^="service_interval"]');
        const expectedLifetimeInput = form.querySelector('input[id^="expected_lifetime"]');
        
        if (!serviceIntervalInput || !expectedLifetimeInput) return;
        
        // Add change event listener
        typeSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const serviceInterval = selectedOption.getAttribute('service_interval');
            const expectedLifetime = selectedOption.getAttribute('expected_lifetime');

            // Update the input fields with the selected option's data attributes
            serviceIntervalInput.value = serviceInterval;
            expectedLifetimeInput.value = expectedLifetime;
        });
    });
});


// Utility function to get Tempus Dominus instance and handle dates properly
function getDatePicker(inputElement) {
    if (!inputElement) return null;
    return inputElement._tempusDominus || null;
}

// Helper function to safely parse dates for Tempus Dominus
function parseDateForPicker(dateString) {
    if (!dateString) return null;
    
    // Handle different date formats
    let date;
    try {
        // Try parsing with native Date
        date = new Date(dateString);
        
        // Check if date is valid
        if (isNaN(date.getTime())) {
            // Try alternative formats
            if (dateString.includes(' ')) {
                // Handle "YYYY-MM-DD HH:MM" format
                const [datePart, timePart] = dateString.split(' ');
                const [year, month, day] = datePart.split('-');
                const [hour, minute] = timePart.split(':');
                
                date = new Date(
                    parseInt(year, 10),
                    parseInt(month, 10) - 1, // Month is 0-based
                    parseInt(day, 10),
                    parseInt(hour, 10),
                    parseInt(minute, 10)
                );
            }
        }
        
        return date;
    } catch (e) {
        console.error("Error parsing date:", dateString, e);
        return null;
    }
}

// Global date picker function with validation
function initializeDatePickers(container = document) {
    // Find all date picker input groups inside the provided container
    const dateInputGroups = container.querySelectorAll('.date-input-group');
    
    dateInputGroups.forEach(group => {
        const dateInput = group.querySelector('.datepicker-input');
        const datePickerToggle = group.querySelector('.datepicker-toggle');
        
        if (!dateInput || !datePickerToggle) {
            //console.log('Missing elements for date picker:', dateInput, datePickerToggle);
            return; // Skip if missing elements
        }
        
        // Store the picker instance in a data attribute
        if (dateInput._tempusDominus) {
            //console.log('Picker already initialized for:', dateInput.id || 'unnamed input');
            return;
        }

        //console.log('Initializing new picker for:', dateInput.id || 'unnamed input');

        // Initialize Tempus Dominus with the correct configuration structure
        const picker = new tempusDominus.TempusDominus(dateInput, {
            localization: {
                format: 'yyyy-MM-dd HH:mm'
            },
            display: {
                theme: 'light',
                icons: {
                    time: 'bi bi-clock',
                    date: 'bi bi-calendar',
                    up: 'bi bi-arrow-up',
                    down: 'bi bi-arrow-down',
                    previous: 'bi bi-chevron-left',
                    next: 'bi bi-chevron-right',
                    today: 'bi bi-calendar-check',
                    clear: 'bi bi-trash',
                    close: 'bi bi-x'
                },
                components: {
                    calendar: true,
                    date: true,
                    month: true,
                    year: true,
                    decades: true,
                    clock: true,
                    hours: true,
                    minutes: true,
                    seconds: false
                }
            },
            restrictions: {
                // Setting min and max dates explicitly to avoid validation errors
                minDate: new Date('1970-01-01 00:00'),
                maxDate: new Date()
            }
        });
        
        // Store the picker instance for later access
        dateInput._tempusDominus = picker;

        // Enforce picker usage
        dateInput.setAttribute('readonly', true);

        // Force the calendar picker toggle to be clickable
        datePickerToggle.style.cursor = 'pointer';
        datePickerToggle.style.pointerEvents = 'auto';
        datePickerToggle.style.zIndex = '100';
        datePickerToggle.style.position = 'relative';
        
        // Define the function to toggle the picker
        function togglePicker(e) {
            e.preventDefault();
            e.stopPropagation();
            //console.log('Toggle clicked for:', dateInput.id || 'unnamed input');
            
            try {
                // Use the stored picker instance directly 
                if (dateInput._tempusDominus) {
                    //console.log('Found picker instance, toggling...');
                    dateInput._tempusDominus.toggle();
                } else {
                    console.error('No picker instance found for', dateInput.id || 'unnamed input');
                }
            } catch (err) {
                console.error('Error toggling picker:', err);
            }
            
            return false;
        }
        
        // Remove any existing click listeners and add new one
        datePickerToggle.onclick = togglePicker;
        
        // Also make the input clickable to show picker
        dateInput.addEventListener('click', function() {
            try {
                if (dateInput._tempusDominus) {
                    dateInput._tempusDominus.show();
                }
            } catch (err) {
                console.error('Error showing picker on input click:', err);
            }
        });

        // Remove any invalid styling initially
        dateInput.classList.remove('is-invalid');

        // Only add validation on hide/close of picker (like flatpickr did)
        picker.subscribe(tempusDominus.Namespace.events.hide, (e) => {
            if (!dateInput.value && dateInput.hasAttribute('required')) {
                dateInput.classList.add('is-invalid');
            } else {
                dateInput.classList.remove('is-invalid');
            }
        });

        // Also ensure validation happens on form submit
        if (dateInput.hasAttribute('required')) {
            const form = dateInput.closest('form');
            if (form && !form.dataset.validationAdded) {
                form.addEventListener('submit', function(e) {
                    let isValid = true;
                    
                    form.querySelectorAll('input[required]').forEach(input => {
                        if (!input.value) {
                            input.classList.add('is-invalid');
                            isValid = false;
                        }
                    });
                    
                    if (!isValid) {
                        e.preventDefault();
                        return false;
                    }
                });
                form.dataset.validationAdded = 'true';
            }
            
            // Ensure each individual submit button also triggers validation
            // This ensures validation happens immediately with the Save button
            const submitButtons = form?.querySelectorAll('button[type="submit"]');
            if (submitButtons) {
                submitButtons.forEach(button => {
                    if (!button.dataset.validationAdded) {
                        button.addEventListener('click', function(e) {
                            if (!dateInput.value && dateInput.hasAttribute('required')) {
                                dateInput.classList.add('is-invalid');
                                e.preventDefault();
                                return false;
                            }
                        });
                        button.dataset.validationAdded = 'true';
                    }
                });
            }
        }
    });
}

// Initialize all date pickers on DOM load
document.addEventListener('DOMContentLoaded', function() {
    initializeDatePickers();
    
    // Initialize datepickers when any modal is shown
    document.addEventListener('shown.bs.modal', function(event) {
        initializeDatePickers(event.target);
    });
});

// Add event listeners for your modal buttons
document.addEventListener('DOMContentLoaded', function() {
    // Service record edit button
    document.querySelectorAll('.edit-service-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const serviceId = this.dataset.serviceId;
            const serviceDate = this.dataset.serviceDate;
            const serviceDescription = this.dataset.serviceDescription;
            const componentId = this.dataset.componentId;
            
            // Populate the service modal
            document.getElementById('serviceId').value = serviceId;
            document.getElementById('serviceComponentId').value = componentId || '';
            document.getElementById('serviceDescription').value = serviceDescription;
            
            // Show the modal FIRST
            const serviceModal = new bootstrap.Modal(document.getElementById('serviceRecordModal'));
            serviceModal.show();
            
            // THEN set the date value AFTER the modal is shown
            setTimeout(() => {
                document.getElementById('serviceDate').value = serviceDate;
            }, 100);
        });
    });
    
    // History record edit button
    document.querySelectorAll('.edit-history-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const historyId = this.dataset.historyId;
            const historyDate = this.dataset.updatedDate || this.dataset.historyDate;
            const componentId = this.dataset.componentId;
            
            // Populate the history modal
            document.getElementById('editHistoryId').value = historyId;
            document.getElementById('editHistoryComponentId').value = componentId;
            
            // Show the modal FIRST
            const historyModal = new bootstrap.Modal(document.getElementById('editHistoryModal'));
            historyModal.show();
            
            // THEN set the date value AFTER the modal is shown
            setTimeout(() => {
                document.getElementById('editUpdatedDate').value = historyDate;
            }, 100);
        });
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
    
    const table = document.querySelector('#componentsTable');
    const headers = table.querySelectorAll('th');
    const tableBody = table.querySelector('tbody');
    const rows = tableBody.querySelectorAll('tr');

    // Skip if there are no rows or just one "no components" message row
    if (rows.length === 0 || (rows.length === 1 && rows[0].cells.length === 1)) return;

    // Sorting function
    const sortColumn = (index, asc = true) => {
        const nodeList = Array.from(rows);
        const compare = (rowA, rowB) => {
            // Skip if td doesn't exist in row (for the "no components registered" row)
            if (!rowA.querySelectorAll('td')[index] || !rowB.querySelectorAll('td')[index]) return 0;
            
            // Get cell content and prepare for comparison
            let cellA = rowA.querySelectorAll('td')[index].innerText.trim();
            let cellB = rowB.querySelectorAll('td')[index].innerText.trim();
            
            // Different handling based on column type
            switch(index) {
                case 0: // Name column
                case 1: // Type column
                case 6: // Bike column
                    // Remove emojis and compare case-insensitively for text columns
                    cellA = cellA.replace(/[\u{1F300}-\u{1F6FF}\u{2600}-\u{26FF}⚡💤⛔🟢🟡🔴🟣⚪]/gu, '').trim().toLowerCase();
                    cellB = cellB.replace(/[\u{1F300}-\u{1F6FF}\u{2600}-\u{26FF}⚡💤⛔🟢🟡🔴🟣⚪]/gu, '').trim().toLowerCase();
                    break;
                    
                case 2: // Distance column
                    // Extract numeric value from "X km" format
                    cellA = parseFloat(cellA.replace(/[^\d.-]/g, '')) || 0;
                    cellB = parseFloat(cellB.replace(/[^\d.-]/g, '')) || 0;
                    break;
                    
                case 3: // Status column
                    // Remove emojis, then normalize status for comparison
                    cellA = cellA.replace(/[\u{1F300}-\u{1F6FF}\u{2600}-\u{26FF}⚡💤⛔🟢🟡🔴🟣⚪]/gu, '').trim();
                    cellB = cellB.replace(/[\u{1F300}-\u{1F6FF}\u{2600}-\u{26FF}⚡💤⛔🟢🟡🔴🟣⚪]/gu, '').trim();
                    
                    // Create custom order for statuses
                    const statusOrder = {
                        "Installed": 1,
                        "Not installed": 2,
                        "Retired": 3
                    };
                    
                    cellA = statusOrder[cellA] || 999;
                    cellB = statusOrder[cellB] || 999;
                    break;
                    
                case 4: // Lifetime column
                case 5: // Service column
                    // Sort by color indicator severity (already center-aligned in cells)
                    const severityOrder = {
                        "🟢": 1, // OK
                        "🟡": 2, // Approaching
                        "🔴": 3, // Due
                        "🟣": 4, // Exceeded
                        "⚪": 5  // Not defined
                    };
                    
                    // Find emoji in the cell
                    const emojiA = cellA.trim().match(/[\u{1F300}-\u{1F6FF}\u{2600}-\u{26FF}🟢🟡🔴🟣⚪]/u);
                    const emojiB = cellB.trim().match(/[\u{1F300}-\u{1F6FF}\u{2600}-\u{26FF}🟢🟡🔴🟣⚪]/u);
                    
                    cellA = emojiA ? severityOrder[emojiA[0]] || 999 : 999;
                    cellB = emojiB ? severityOrder[emojiB[0]] || 999 : 999;
                    break;
            }
            
            // Compare based on formatted values
            if (typeof cellA === 'number' && typeof cellB === 'number') {
                return asc ? cellA - cellB : cellB - cellA;
            } else {
                return asc ? (cellA > cellB ? 1 : -1) : (cellA < cellB ? 1 : -1);
            }
        };
        
        // Sort and reattach rows
        nodeList.sort(compare);
        nodeList.forEach(node => tableBody.appendChild(node));
    };

    // Add click event to table headers (skip the last column with delete button)
    headers.forEach((header, index) => {
        // Skip the last column with delete buttons
        if (index === headers.length - 1) return;
        
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

    // Initial sort by Name column (index 0) in ascending order
    if (headers.length > 0 && rows.length > 1) {
        // Add sorted-asc class to the Name column header
        headers[0].classList.add('sorted-asc');
        
        // Sort by Name column (index 0) in ascending order
        sortColumn(0, true);
    }
});

// Function for filtering table all components
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the component overview page
    if (document.querySelector('h1#component-overview') === null) return;
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

// Add search filtering functionality for all components table
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the component overview page
    if (document.querySelector('h1#component-overview') === null) return;
    
    const searchInput = document.getElementById('allComponentsSearchInput');
    if (!searchInput) return;
    
    const table = document.querySelector('#componentsTable');
    const rows = table.querySelectorAll('tbody tr');
    const filterSwitches = document.querySelectorAll('.filter-switch');
    
    // Skip if there are no rows or just one "no components" message row
    if (rows.length === 0 || (rows.length === 1 && rows[0].cells.length === 1)) return;
    
    // Function to update row visibility based on both filters and search
    function updateRowVisibility() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        
        // Get current filter states
        const showInstalled = document.getElementById('showInstalledComponents').checked;
        const showRetired = document.getElementById('showRetiredComponents').checked;
        const notInstalledSwitch = document.getElementById('showNotInstalledComponents');
        const showNotInstalled = notInstalledSwitch ? notInstalledSwitch.checked : false;
        
        rows.forEach(row => {
            // Skip the "no components registered" row
            if (row.cells.length === 1 && row.cells[0].colSpan) {
                return;
            }
            
            // Check if row should be visible based on status filter
            let visibleByFilter = false;
            const status = row.getAttribute('data-status');
            
            if ((status === 'Installed' && showInstalled) ||
                (status === 'Not installed' && showNotInstalled) ||
                (status === 'Retired' && showRetired)) {
                visibleByFilter = true;
            }
            
            // Check if row matches search term
            const name = row.cells[0].textContent.toLowerCase();
            const type = row.cells[1].textContent.toLowerCase();
            const bike = row.cells[6].textContent.toLowerCase();
            const rowText = `${name} ${type} ${bike}`;
            const matchesSearch = searchTerm === '' || rowText.includes(searchTerm);
            
            // Show row only if it matches both filter and search criteria
            row.style.display = (visibleByFilter && matchesSearch) ? '' : 'none';
        });
        
        // Show a message if no results found
        const visibleRows = Array.from(rows).filter(row => row.style.display !== 'none');
        const noResultsRow = table.querySelector('.no-results-row');
        
        if (visibleRows.length === 0 && (searchTerm !== '' || showInstalled || showNotInstalled || showRetired)) {
            if (!noResultsRow) {
                const tbody = table.querySelector('tbody');
                const newRow = document.createElement('tr');
                newRow.className = 'no-results-row';
                newRow.innerHTML = '<td colspan="8" class="text-center">No components match your criteria</td>';
                tbody.appendChild(newRow);
            } else {
                noResultsRow.style.display = '';
            }
        } else if (noResultsRow) {
            noResultsRow.style.display = 'none';
        }
    }
    
    // Listen for search input changes
    searchInput.addEventListener('input', updateRowVisibility);
    
    // Listen for filter changes
    filterSwitches.forEach(switchElement => {
        switchElement.addEventListener('change', updateRowVisibility);
    });
    
    // Clear search button
    searchInput.addEventListener('keyup', function(event) {
        if (event.key === 'Escape') {
            this.value = '';
            // Update visibility after clearing
            updateRowVisibility();
        }
    });
});

// ===== Bike details page functions =====

// Function for filtering table components for single bike
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the component overview page
    if (document.querySelector('h1#bike-details') === null) return;
    
    const componentsBikeTable = document.getElementById('componentsBikeTable');
    if (!componentsBikeTable) return;

    const filterSwitches = document.querySelectorAll('.filter-switch');
    const componentRows = componentsBikeTable.querySelectorAll('tbody tr');

    function updateComponentRowVisibility() {
        // Get switch states
        const showInstalled = document.getElementById('showInstalledComponents').checked;
        const showRetired = document.getElementById('showRetiredComponents').checked;
        const notInstalledSwitch = document.getElementById('showNotInstalledComponents');
        const showNotInstalled = notInstalledSwitch ? notInstalledSwitch.checked : false;

        componentRows.forEach(row => {
            // Check if this is the "no components" message row
            if (row.cells.length === 1 && row.cells[0].colSpan) {
                // Always keep the "no components" message visible
                return;
            }
            
            const statusCell = row.querySelector('td:nth-child(1)');
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

// Script to sort bike component table
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the bike details page with the components table
    const componentsBikeTable = document.getElementById('componentsBikeTable');
    if (!componentsBikeTable) return;
    
    const headers = componentsBikeTable.querySelectorAll('th');
    const tableBody = componentsBikeTable.querySelector('tbody');
    const rows = tableBody.querySelectorAll('tr');

    // Sorting function
    const sortColumn = (index, asc = true) => {
        // Skip sorting if the table is empty or has the "no components" message row
        if (rows.length === 0 || (rows.length === 1 && rows[0].cells.length === 1)) return;
        
        const nodeList = Array.from(rows);
        const compare = (rowA, rowB) => {
            // Get text content from cells
            let cellA = rowA.querySelectorAll('td')[index].innerText.trim();
            let cellB = rowB.querySelectorAll('td')[index].innerText.trim();
            
            // Special handling for name column (remove emojis)
            // Special handling for name column (remove emojis and normalize case)
            if (index === 0) { // Name column
                // Remove emoji characters, trim whitespace, and convert to lowercase
                cellA = cellA.replace(/[\u{1F300}-\u{1F6FF}\u{2600}-\u{26FF}⚡⛔]/gu, '').trim().toLowerCase();
                cellB = cellB.replace(/[\u{1F300}-\u{1F6FF}\u{2600}-\u{26FF}⚡⛔]/gu, '').trim().toLowerCase();
            }
            
            // Special handling for distance column (extract numeric value)
            if (index === 2) { // Distance column
                cellA = parseFloat(cellA.replace(' km', '')) || 0;
                cellB = parseFloat(cellB.replace(' km', '')) || 0;
            } 
            // Special handling for next life/srv column (numeric values)
            else if (index === 4) { // Next life/srv column
                cellA = cellA === '-' ? Infinity : parseFloat(cellA) || 0;
                cellB = cellB === '-' ? Infinity : parseFloat(cellB) || 0;
            }
            // Special handling for cost column (extract numeric value)
            else if (index === 5) { // Cost column
                cellA = cellA === '-' ? 0 : parseFloat(cellA.replace(' kr', '')) || 0;
                cellB = cellB === '-' ? 0 : parseFloat(cellB.replace(' kr', '')) || 0;
            }
            
            // Compare based on parsed values or text
            if (typeof cellA === 'number' && typeof cellB === 'number') {
                return asc ? cellA - cellB : cellB - cellA;
            } else {
                return asc ? (cellA > cellB ? 1 : -1) : (cellA < cellB ? 1 : -1);
            }
        };
        
        // Sort and reattach rows
        nodeList.sort(compare);
        nodeList.forEach(node => tableBody.appendChild(node));
    };

    // Add data-sort attribute and sort indicators to headers (except Life / srv column)
    headers.forEach((header, index) => {
        // Skip the "Life / srv" column (index 3)
        if (index === 3) return;
        
        // Add data-sort attribute to make headers sortable
        header.setAttribute('data-sort', '');
        
        // Add sort indicator span if it doesn't exist
        if (!header.querySelector('.sort-indicator')) {
            const indicator = document.createElement('span');
            indicator.className = 'sort-indicator';
            header.appendChild(indicator);
        }

        // Add click event to headers
        header.addEventListener('click', () => {
            const columnIndex = header.cellIndex;
            const isAscending = !header.classList.contains('sorted-asc');
            
            // Remove sorted classes from all headers
            headers.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
            
            // Add appropriate class to clicked header
            header.classList.add(isAscending ? 'sorted-asc' : 'sorted-desc');
            
            // Sort the column
            sortColumn(columnIndex, isAscending);
        });
    });

    // Initial sort by Next service column (index 4) in ascending order
    if (headers.length > 0 && rows.length > 1) {
        // Add sorted-asc class to the Next service column header
        headers[4].classList.add('sorted-asc');
        
        // Sort by Next service column (index 4) in ascending order
        sortColumn(4, true);
    }
});

// Add search filtering functionality for bike details component table
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the bike details page
    if (document.querySelector('h1#bike-details') === null) return;
    
    const componentsBikeTable = document.getElementById('componentsBikeTable');
    if (!componentsBikeTable) return;
    
    const searchInput = document.getElementById('singleBikeComponentsSearchInput');
    if (!searchInput) return;
    
    const rows = componentsBikeTable.querySelectorAll('tbody tr');
    const filterSwitches = document.querySelectorAll('.filter-switch');
    
    // Skip if there are no rows or just one "no components" message row
    if (rows.length === 0 || (rows.length === 1 && rows[0].cells.length === 1)) return;
    
    // Function to update row visibility based on both filters and search
    function updateRowVisibility() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        
        // Get current filter states
        const showInstalled = document.getElementById('showInstalledComponents').checked;
        const showRetired = document.getElementById('showRetiredComponents').checked;
        
        rows.forEach(row => {
            // Skip the "no components registered" row
            if (row.cells.length === 1 && row.cells[0].colSpan) {
                return;
            }
            
            // Check if row should be visible based on existing filter
            let visibleByFilter = true;
            const statusCell = row.querySelector('td:nth-child(1)');
            
            if (statusCell) {
                const statusText = statusCell.textContent.trim();
                visibleByFilter = (
                    (statusText.includes('⚡') && showInstalled) ||
                    (statusText.includes('⛔') && showRetired)
                );
            }
            
            // Check if row matches search term
            const name = row.cells[0].textContent.toLowerCase();
            const type = row.cells[1].textContent.toLowerCase();
            const rowText = `${name} ${type}`;
            const matchesSearch = searchTerm === '' || rowText.includes(searchTerm);
            
            // Show row only if it matches both filter and search criteria
            row.style.display = (visibleByFilter && matchesSearch) ? '' : 'none';
        });
        
        // Show a message if no results found
        const visibleRows = Array.from(rows).filter(row => row.style.display !== 'none');
        let noResultsRow = componentsBikeTable.querySelector('.no-results-row');
        
        if (visibleRows.length === 0 && rows.length > 0) {
            if (!noResultsRow) {
                const tbody = componentsBikeTable.querySelector('tbody');
                const newRow = document.createElement('tr');
                newRow.className = 'no-results-row';
                newRow.innerHTML = '<td colspan="6" class="text-center">No components match your criteria</td>';
                tbody.appendChild(newRow);
            } else {
                noResultsRow.style.display = '';
            }
        } else if (noResultsRow) {
            noResultsRow.style.display = 'none';
        }
    }
    
    // Listen for search input changes
    searchInput.addEventListener('input', updateRowVisibility);
    
    // Listen for filter changes
    filterSwitches.forEach(switchElement => {
        switchElement.addEventListener('change', updateRowVisibility);
    });
    
    // Clear search button
    searchInput.addEventListener('keyup', function(event) {
        if (event.key === 'Escape') {
            this.value = '';
            // Update visibility after clearing
            updateRowVisibility();
        }
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
        const bikeIdSelect = this.querySelector('[name="component_bike_id"]');
        const bikeId = bikeIdSelect.value;
        //Switch for debugging to prevent form to submit
        //e.preventDefault();
        
        // For status update modal, we need to check additional conditions
        if (form.id === 'component_status_form') {
            const initialSelectedStatus = statusSelect.options[statusSelect.selectedIndex].defaultSelected ? statusSelect.value : null;
            const initialBikeId = form.dataset.initialBikeId; 
            const dateInput = this.querySelector('#component_updated_date');
            const initialDate = dateInput.defaultValue;

            if (installationStatus === initialSelectedStatus && dateInput.value !== initialDate) {
                e.preventDefault();
                const modalBody = document.getElementById('validationModalBody');
                modalBody.innerHTML = `Status cannot be changed to "${statusSelect.value}" since status is already "${installationStatus}"`;
                validationModal.show();
                return;
            
            } else if (dateInput.value === initialDate) {
                e.preventDefault();
                const modalBody = document.getElementById('validationModalBody');
                modalBody.innerHTML = `Updated date must be changed when updating status. Last updated date is ${initialDate}. Select a date after this date`;
                validationModal.show();
                return;

            } else if (installationStatus !== initialSelectedStatus && dateInput.value === initialDate) {
                e.preventDefault();
                const modalBody = document.getElementById('validationModalBody');
                modalBody.innerHTML = `Status cannot be changed unless you also update record date`;
                validationModal.show();
                return;
                // This rule is kept for fallback, but is not triggered due to rule above

            } else if (installationStatus === 'Retired' && initialBikeId !== bikeId) {
                e.preventDefault();
                const modalBody = document.getElementById('validationModalBody');
                modalBody.innerHTML = `Bike assignment cannot be changed at time of retirement. If you need to unassign or change bike prior to retiring, uninstall or install component first`;
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
                modalBody.innerHTML = "You are about to retire this component. This will lock the component and prevent further editing. Delete the most recent installation record if you wish to unlock the component. Do you want to proceed? You still need to save";
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
    const currentComponentId = document.getElementById('serviceComponentId')?.value;

    // Handle "New Service" button click
    document.querySelector('[data-bs-target="#serviceRecordModal"]')?.addEventListener('click', function() {
        // Set up modal for creating new service
        document.getElementById('serviceRecordModalLabel').textContent = 'New Service Record';
        document.getElementById('serviceRecordForm').action = '/add_service_record';
        
        // Ensure component_id is set for new service
        document.getElementById('serviceComponentId').value = currentComponentId;
        
        // Clear other form fields
        document.getElementById('serviceId').value = '';
        document.getElementById('serviceDate').value = '';
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
            document.getElementById('serviceDescription').value = this.dataset.serviceDescription;
            
            // Simply set the input value directly and avoid using the API
            document.getElementById('serviceDate').value = this.dataset.serviceDate;
            
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
            
            // Simply set the input value directly and avoid using the API
            document.getElementById('editUpdatedDate').value = updatedDate;
            
            editHistoryModal.show();
        });
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