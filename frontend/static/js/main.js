// ===== Modal components for feedback to user ====

let validationModal;
let confirmModal;
let loadingModal;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize modal instances with their specific options
    validationModal = new bootstrap.Modal(document.getElementById('validationModal'), {
        backdrop: 'static',  // Prevent closing when clicking outside
        keyboard: false      // Prevent closing with keyboard
    });
    
    // These should behave normally
    confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
    loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));

    // Function to remove backdrop on some modals
    const removeBackdropModals = [
        'workplanRecordModal',
        'incidentRecordModal', 
        'serviceRecordModal',
        'editHistoryModal',
        'collectionModal'
    ];
    
    removeBackdropModals.forEach(modalId => {
        const modal = document.getElementById(modalId);
        if (!modal) return;
        
        // Add handler for when the modal is hidden
        modal.addEventListener('hidden.bs.modal', function() {
            // Check if there are any other visible modals
            const visibleModals = document.querySelectorAll('.modal.show').length;
            
            // If no visible modals but backdrop exists, remove it
            if (visibleModals === 0 && document.querySelector('.modal-backdrop')) {
                document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
                    backdrop.remove();
                });
                document.body.classList.remove('modal-open');
                document.body.style.removeProperty('overflow');
                document.body.style.removeProperty('padding-right');
            }
        });
    });
    
    // Add validation to all forms with date picker inputs
    document.querySelectorAll('form').forEach(form => {
        const dateInputs = form.querySelectorAll('.datepicker-input');
        
        if (dateInputs.length > 0) {
            form.addEventListener('submit', function(e) {
                let hasDateError = false;
                
                // Check all date inputs in this form
                dateInputs.forEach(input => {
                    if (input.hasAttribute('required') && !input.value) {
                        input.classList.add('is-invalid');
                        hasDateError = true;
                    } else if (input.value) {
                        // Validate date format (YYYY-MM-DD HH:MM)
                        const datePattern = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/;
                        if (!datePattern.test(input.value)) {
                            input.classList.add('is-invalid');
                            hasDateError = true;
                        } else {
                            input.classList.remove('is-invalid');
                        }
                    }
                });
                
                // If any date error, prevent form submission and show validation message
                if (hasDateError) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    const modalBody = document.getElementById('validationModalBody');
                    modalBody.innerHTML = 'Please enter valid dates in the format YYYY-MM-DD HH:MM';
                    validationModal.show();
                    return false;
                }
            }, true); // Use capturing phase to ensure this runs before other handlers
        }
    });

    // Markdown toggle functionality for workplan descriptions
    const workplanModal = document.getElementById('workplanRecordModal');
    if (workplanModal) {
        const toggleBtn = document.getElementById('workplan_markdown_toggle');
        const editMode = document.getElementById('workplan_edit_mode');
        const previewMode = document.getElementById('workplan_preview_mode');
        const textarea = document.getElementById('workplan_description');
        const previewContent = document.getElementById('workplan_preview_content');
        
        let isPreviewMode = false;
        let md = null;
        
        if (toggleBtn && editMode && previewMode && textarea && previewContent) {
            
            // Initialize markdown-it with task lists
            md = window.markdownit({
                html: false,
                breaks: true,
                linkify: true
            }).use(window.markdownitTaskLists, {
                enabled: true,
                lineNumber: true,
                label: true
            });
            
            function containsMarkdown(text) {
                if (!text || !text.trim()) return false;
                
                const patterns = [
                    /\*\*.*\*\*/,           // Bold
                    /\*.*\*/,               // Italic  
                    /^#+\s/m,               // Headers
                    /- \[[x ]\]/,           // Checkboxes
                    /^\s*[-*+]\s/m,         // Lists
                    /^\s*\d+\.\s/m,         // Numbered lists
                    /`.*`/,                 // Inline code
                    /```[\s\S]*```/,        // Code blocks
                    /\[.*\]\(.*\)/,         // Links
                    /^\|.*\|/m              // Tables
                ];
                
                return patterns.some(pattern => pattern.test(text));
            }
            
            function setInitialMode() {
                const text = textarea.value;
                
                if (containsMarkdown(text)) {
                    // Start in preview mode
                    renderPreview();
                    editMode.style.display = 'none';
                    previewMode.style.display = 'block';
                    toggleBtn.innerHTML = '✏️ Edit description';
                    isPreviewMode = true;
                } else {
                    // Start in edit mode
                    editMode.style.display = 'block';
                    previewMode.style.display = 'none';
                    toggleBtn.innerHTML = '👁️ Preview';
                    isPreviewMode = false;
                    textarea.focus();
                }
            }
            
            function renderPreview() {
                const markdownText = textarea.value.trim();
                if (markdownText) {
                    previewContent.innerHTML = md.render(markdownText);
                    
                    // Make checkboxes interactive
                    const checkboxes = previewContent.querySelectorAll('input.task-list-item-checkbox');
                    checkboxes.forEach((checkbox, index) => {
                        checkbox.removeAttribute('disabled');
                        checkbox.addEventListener('change', function() {
                            updateCheckboxInText(index, this.checked);
                        });
                    });
                } else {
                    previewContent.innerHTML = '<em class="text-muted">No content to preview...</em>';
                }
            }
            
            function updateCheckboxInText(checkboxIndex, isChecked) {
                const lines = textarea.value.split('\n');
                let currentCheckboxIndex = 0;
                
                for (let i = 0; i < lines.length; i++) {
                    if (lines[i].match(/^\s*-\s*\[([ x])\]/)) {
                        if (currentCheckboxIndex === checkboxIndex) {
                            if (isChecked) {
                                lines[i] = lines[i].replace(/\[ \]/, '[x]');
                            } else {
                                lines[i] = lines[i].replace(/\[x\]/, '[ ]');
                            }
                            break;
                        }
                        currentCheckboxIndex++;
                    }
                }
                
                textarea.value = lines.join('\n');
                renderPreview();
            }
            
            // Set initial mode when modal is shown (after content is loaded)
            workplanModal.addEventListener('shown.bs.modal', function() {
                // Small delay to ensure content is populated
                setTimeout(setInitialMode, 100);
            });
            
            toggleBtn.addEventListener('click', function() {
                if (!isPreviewMode) {
                    renderPreview();
                    editMode.style.display = 'none';
                    previewMode.style.display = 'block';
                    toggleBtn.innerHTML = '✏️ Edit description';
                    isPreviewMode = true;
                } else {
                    editMode.style.display = 'block';
                    previewMode.style.display = 'none';
                    toggleBtn.innerHTML = '👁️ Preview';
                    isPreviewMode = false;
                    textarea.focus();
                }
            });
        }
    }
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
        // console.log("Success parameter:", success, typeof success);
        showToast(message, success);
    }
});

// Toast behaviour
function showToast(message, success = true) {
    // console.log("Success value:", success, typeof success); // Debug log
    
    const toast = document.getElementById('messageToast');
    const toastHeader = toast.querySelector('.toast-header');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    const progressBar = document.getElementById('toastProgressBar');

    // Reset all classes first
    toast.classList.remove('border-success', 'border-danger', 'border-warning');
    toastHeader.classList.remove('bg-success', 'bg-danger', 'bg-warning', 'text-white');

    // Set the appropriate title and styling based on status
    if (success === "warning") {
        toastTitle.textContent = 'Warning';
        toast.classList.add('border-warning');
        toastHeader.classList.add('bg-warning', 'text-white');
    }
    else if (success === "True" || success === "true" || success === true) {
        toastTitle.textContent = 'Success';
        toast.classList.add('border-success');
        toastHeader.classList.add('bg-success', 'text-white');
    }
    else {
        toastTitle.textContent = 'Error';
        toast.classList.add('border-danger'); 
        toastHeader.classList.add('bg-danger', 'text-white');
    }
    
    toastMessage.textContent = message;

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

// Global configuration of date pickers, including helper functions
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

// Function to validate date format (YYYY-MM-DD HH:MM)
function validateDateInput(input) {
    if (!input.value && input.hasAttribute('required')) {
        input.classList.add('is-invalid');
        return false;
    }
    
    if (!input.value) {
        // Empty but not required is valid
        input.classList.remove('is-invalid');
        return true;
    }
    
    // Validate format (YYYY-MM-DD HH:MM)
    const datePattern = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/;
    if (!datePattern.test(input.value)) {
        input.classList.add('is-invalid');
        return false;
    }
    
    // Validate that the date is real
    try {
        const parts = input.value.split(/[- :]/);
        const year = parseInt(parts[0], 10);
        const month = parseInt(parts[1], 10) - 1; // JS months are 0-based
        const day = parseInt(parts[2], 10);
        const hour = parseInt(parts[3], 10);
        const minute = parseInt(parts[4], 10);
        
        // Check ranges
        if (month < 0 || month > 11) {
            input.classList.add('is-invalid');
            return false;
        }
        
        if (day < 1 || day > 31) {
            input.classList.add('is-invalid');
            return false;
        }
        
        if (hour < 0 || hour > 23) {
            input.classList.add('is-invalid');
            return false;
        }
        
        if (minute < 0 || minute > 59) {
            input.classList.add('is-invalid');
            return false;
        }
        
        // Check for valid date (e.g., no February 31)
        const date = new Date(year, month, day, hour, minute);
        if (
            date.getFullYear() !== year ||
            date.getMonth() !== month ||
            date.getDate() !== day ||
            date.getHours() !== hour ||
            date.getMinutes() !== minute
        ) {
            input.classList.add('is-invalid');
            return false;
        }
        
        input.classList.remove('is-invalid');
        return true;
    } catch (err) {
        console.error('Date validation error:', err);
        input.classList.add('is-invalid');
        return false;
    }
}

// Updated date picker initialization with improved validation
function initializeDatePickers(container = document) {
    // Find all date picker input groups inside the provided container
    const dateInputGroups = container.querySelectorAll('.date-input-group');

    dateInputGroups.forEach(group => {
        const dateInput = group.querySelector('.datepicker-input');
        const datePickerToggle = group.querySelector('.datepicker-toggle');
        
        if (!dateInput || !datePickerToggle) {
            return; // Skip if missing elements
        }
        
        // Store the picker instance in a data attribute
        if (dateInput._tempusDominus) {
            return; // Already initialized
        }

        // Set current date/time by default for new forms
        // We only do this for empty inputs, not for pre-filled ones
        if (!dateInput.value) {
            const now = new Date();
            // Format as YYYY-MM-DD HH:MM
            const formattedDate = now.getFullYear() + '-' + 
                String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                String(now.getDate()).padStart(2, '0') + ' ' + 
                String(now.getHours()).padStart(2, '0') + ':' + 
                String(now.getMinutes()).padStart(2, '0');
            
            dateInput.value = formattedDate;
        }

        // Determine if this is a due date field (which should allow future dates)
        const isDueDateField = dateInput.id === 'due_date';
        
        // Initialize Tempus Dominus with improved configuration
        const picker = new tempusDominus.TempusDominus(dateInput, {
            localization: {
                format: 'yyyy-MM-dd HH:mm'
            },
            display: {
                theme: 'light',
                buttons: {
                    today: true,
                    clear: true,
                    close: true
                },
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
                minDate: new Date('1970-01-01 00:00'),
                // Only set maxDate for non-due date fields
                ...(isDueDateField ? {} : { maxDate: new Date() })
            },
            // Allow viewing the calendar without selecting anything
            useCurrent: false
        });

        // Subscribe to the show event to sync with input value  
        picker.subscribe(tempusDominus.Namespace.events.show, () => {
            if (dateInput.value) {
                try {
                    // Just trigger a change event to make picker re-read the input
                    dateInput.dispatchEvent(new Event('change'));
                } catch (e) {
                    console.warn('Could not sync picker with input:', e);
                }
            }
        });
        
        // Store the picker instance for later access
        dateInput._tempusDominus = picker;

        // IMPORTANT: Remove readonly - allow manual typing
        dateInput.removeAttribute('readonly');

        // Style the toggle for better visibility
        datePickerToggle.classList.add('date-toggle-clickable');
        
        // ONLY open the date picker when the calendar icon is clicked
        dateInput.removeEventListener('click', () => {
            picker.show();
        });
        
        // Define the function to toggle the picker
        function togglePicker(e) {
            e.preventDefault();
            e.stopPropagation();
            
            try {
                if (dateInput._tempusDominus) {
                    dateInput._tempusDominus.toggle();
                }
            } catch (err) {
                console.error('Error toggling picker:', err);
            }
            
            return false;
        }
        
        // Remove any existing click listeners and add new one
        datePickerToggle.onclick = togglePicker;

        // Add validation for manually typed dates
        dateInput.addEventListener('blur', function() {
            validateDateInput(this);
        });

        // Also validate on input change
        dateInput.addEventListener('input', function() {
            // Don't add invalid class while typing,
            // but do remove it if it becomes valid
            if (validateDateInput(this)) {
                this.classList.remove('is-invalid');
            }
        });

        // Ensure validation happens when the picker sets a date
        picker.subscribe(tempusDominus.Namespace.events.change, (e) => {
            validateDateInput(dateInput);
        });

        // Remove any invalid styling initially
        dateInput.classList.remove('is-invalid');

        // Add validation to the form
        const form = dateInput.closest('form');
        if (form && !form.dataset.dateValidationAdded) {
            // Store original submit handler if it exists
            const originalSubmit = form.onsubmit;
            
            // Replace with our enhanced submit handler
            form.onsubmit = function(e) {
                // First, prevent default and stop propagation immediately
                e.preventDefault();
                e.stopPropagation();
                
                let isValid = true;
                
                // Validate all date inputs in this form
                form.querySelectorAll('.datepicker-input').forEach(input => {
                    if (!validateDateInput(input)) {
                        isValid = false;
                    }
                });
                
                // Also validate other required inputs
                form.querySelectorAll('input[required]:not(.datepicker-input)').forEach(input => {
                    if (!input.value) {
                        input.classList.add('is-invalid');
                        isValid = false;
                    }
                });
                
                // Prevent submission if invalid
                if (!isValid) {
                    // Show validation modal with message
                    const validationModal = document.getElementById('validationModal');
                    if (validationModal) {
                        document.getElementById('validationModalBody').textContent = 
                            'Please correct the invalid date format. Required format: YYYY-MM-DD HH:MM';
                        new bootstrap.Modal(validationModal).show();
                    }
                    
                    return false;
                }
                
                // If we're valid, submit the form manually
                if (originalSubmit && typeof originalSubmit === 'function') {
                    // Call original handler
                    const result = originalSubmit.call(this, e);
                    if (result !== false) {
                        form.submit();
                    }
                } else {
                    // No original handler, just submit
                    form.submit();
                }
                
                // Always return false to prevent default form submission
                return false;
            };
            
            form.dataset.dateValidationAdded = 'true';
        }

        // Ensure each submit button also triggers validation
        const submitButtons = form?.querySelectorAll('button[type="submit"]');
        if (submitButtons) {
            submitButtons.forEach(button => {
                if (!button.dataset.dateValidationAdded) {
                    const originalClick = button.onclick;
                    
                    button.onclick = function(e) {
                        const dateInputs = form.querySelectorAll('.datepicker-input');
                        let isValid = true;
                        
                        dateInputs.forEach(input => {
                            if (!validateDateInput(input)) {
                                isValid = false;
                            }
                        });
                        
                        if (!isValid) {
                            e.preventDefault();
                            e.stopPropagation();
                            
                            // Show validation modal with message
                            const validationModal = document.getElementById('validationModal');
                            if (validationModal) {
                                document.getElementById('validationModalBody').textContent = 
                                    'Invalid date format. Required format: YYYY-MM-DD HH:MM';
                                new bootstrap.Modal(validationModal).show();
                            }
                            
                            return false;
                        }
                        
                        if (originalClick && typeof originalClick === 'function') {
                            return originalClick.call(this, e);
                        }
                        
                        return true;
                    };
                    
                    button.dataset.dateValidationAdded = 'true';
                }
            });
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
                           button.dataset.historyId ||
                           button.dataset.incidentId ||
                           button.dataset.workplanId;

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
            } else if (button.dataset.incidentId) {
                tableSelector = 'Incidents';
                recordType = 'incident report';
            } else if (button.dataset.workplanId) {
                tableSelector = 'Workplans';
                recordType = 'workplan';
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
        
        // Enhanced version that stores original values and sets current date
        editComponentStatusModal.addEventListener('show.bs.modal', function() {
            // Set current date/time
            const now = new Date();
            const formattedDate = now.getFullYear() + '-' + 
                String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                String(now.getDate()).padStart(2, '0') + ' ' + 
                String(now.getHours()).padStart(2, '0') + ':' + 
                String(now.getMinutes()).padStart(2, '0');
            
            // Find the form elements
            const dateInput = document.querySelector('#editComponentStatusModal #component_updated_date');
            const statusSelect = document.querySelector('#editComponentStatusModal #component_installation_status');
            const bikeSelect = document.querySelector('#editComponentStatusModal #component_bike_id');
            
            // Store original values before changing anything
            if (dateInput) {
                dateInput.dataset.originalValue = dateInput.value;
                dateInput.value = formattedDate;
            }
            
            if (statusSelect) {
                statusSelect.dataset.originalValue = statusSelect.value;
            }
            
            if (bikeSelect) {
                bikeSelect.dataset.originalValue = bikeSelect.value;
            }
        });
    }
});

// Function for validating component status changes
function addFormValidation(form) {
    if (!form) return;

    // Replace the submit event listener with a more robust approach
    form.onsubmit = function(e) {
        // Immediately prevent the default action
        e.preventDefault();
        
        const statusSelect = this.querySelector('[name="component_installation_status"]');
        const installationStatus = statusSelect.value;
        const bikeIdSelect = this.querySelector('[name="component_bike_id"]');
        const bikeId = bikeIdSelect.value;
        
        // For status update modal, we need to check additional conditions
        if (form.id === 'component_status_form') {
            // Use the stored original values from data attributes
            const originalStatus = statusSelect.dataset.originalValue;
            const originalBikeId = bikeIdSelect.dataset.originalValue || form.dataset.initialBikeId;
            const dateInput = this.querySelector('#component_updated_date');
            const originalDate = dateInput.dataset.originalValue;

            // Rule 1: Can't keep the same status
            if (installationStatus === originalStatus) {
                const modalBody = document.getElementById('validationModalBody');
                modalBody.innerHTML = `Status cannot be changed to "${statusSelect.value}" since status is already "${originalStatus}"`;
                validationModal.show();
                return false;
            }
            
            // Rule 2: Date must change from original
            if (dateInput.value === originalDate) {
                const modalBody = document.getElementById('validationModalBody');
                modalBody.innerHTML = `Updated date must be changed when updating status. Last updated date is ${originalDate}. Select a date after this date`;
                validationModal.show();
                return false;
            }

            // Rule 3: Status change requires date change (keeping this as fallback)
            if (installationStatus !== originalStatus && dateInput.value === originalDate) {
                const modalBody = document.getElementById('validationModalBody');
                modalBody.innerHTML = `Status cannot be changed unless you also update record date`;
                validationModal.show();
                return false;
            }

            // Rule 4: Can't change bike assignment during retirement
            if (installationStatus === 'Retired' && originalBikeId !== bikeId) {
                const modalBody = document.getElementById('validationModalBody');
                modalBody.innerHTML = `Bike assignment cannot be changed at time of retirement. If you need to unassign or change bike prior to retiring, uninstall or install component first`;
                validationModal.show();
                return false;
            }
        }

        // Common validation for both forms
        if (installationStatus === 'Installed' && !bikeId) {
            const modalBody = document.getElementById('validationModalBody');
            modalBody.innerHTML = 'Status cannot be set to "Installed" if no bike is selected';
            validationModal.show();
            return false;
        }
        
        // If we got here, validation passed - manually submit the form
        this.submit();
    };
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
        document.getElementById('serviceRecordModalLabel').textContent = 'New service record';
        document.getElementById('serviceRecordForm').action = '/add_service_record';
        
        // Ensure component_id is set for new service
        document.getElementById('serviceComponentId').value = currentComponentId;
        
        // Clear other form fields
        document.getElementById('serviceId').value = '';
        document.getElementById('serviceDescription').value = '';

        // Set current date/time by default
        const now = new Date();
        const formattedDate = now.getFullYear() + '-' + 
        String(now.getMonth() + 1).padStart(2, '0') + '-' + 
        String(now.getDate()).padStart(2, '0') + ' ' + 
        String(now.getHours()).padStart(2, '0') + ':' + 
        String(now.getMinutes()).padStart(2, '0');

        // Set this using setTimeout to ensure the value sticks
        setTimeout(() => {
            document.getElementById('serviceDate').value = formattedDate;
        }, 100);
        
        serviceRecordModal.show();
    });

    // Handle service record edit button clicks
    document.querySelectorAll('.edit-service-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Set up modal for editing service
            document.getElementById('serviceRecordModalLabel').textContent = 'Edit service record';
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

// ===== Incident reports page functions =====

// Function to initialize incident features
(function() {
    // Only run this code if the incident modal is present
    if (!document.getElementById('incidentRecordModal')) {
        return;
    }
    
    // Local variables
    let pendingComponentData = null;
    let isNewIncident = false;
    let originalIncidentOptions = null;
    
    // Initialize when the DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        const incidentModal = document.getElementById('incidentRecordModal');
        if (incidentModal) {
            // Setup modal shown event
            incidentModal.addEventListener('shown.bs.modal', function() {
                // console.log("Incident modal shown, isNewIncident:", isNewIncident);
                initializeDatePickers(incidentModal);
                
                // If it's a new incident, we need special handling
                if (isNewIncident) {
                    initializeComponentSelector(null);
                    
                    // Set current date after pickers are initialized
                    setTimeout(() => {
                        const now = new Date();
                        const formattedDate = now.getFullYear() + '-' + 
                            String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                            String(now.getDate()).padStart(2, '0') + ' ' + 
                            String(now.getHours()).padStart(2, '0') + ':' + 
                            String(now.getMinutes()).padStart(2, '0');
                        
                        document.getElementById('incident_date').value = formattedDate;
                    }, 100);
                } else {
                    // For editing incidents
                    initializeComponentSelector(pendingComponentData);
                }
                
                // Call the existing form initialization function
                initializeIncidentForm();
            });
            
            // Clean up when modal is hidden
            incidentModal.addEventListener('hidden.bs.modal', function() {
                // console.log("Incident modal hidden - resetting flags");
                pendingComponentData = null;
                isNewIncident = false; // This should reset the flag
                
                // Also clear any TomSelect instances to prevent memory leaks
                const componentSelect = document.getElementById('incident_affected_component_ids');
                if (componentSelect && (componentSelect.tomSelect || componentSelect.tomselect)) {
                    const ts = componentSelect.tomSelect || componentSelect.tomselect;
                    ts.destroy();
                    componentSelect.tomSelect = null;
                    componentSelect.tomselect = null;
                }
            });
        }
        
        // Setup edit button click handlers
        document.querySelectorAll('.edit-incident-btn').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                isNewIncident = false;
                
                // Configure modal for editing
                document.getElementById('incidentRecordModalLabel').textContent = 'Edit incident report';
                document.getElementById('incident_form').action = '/update_incident_record';
                
                // Get data from the button
                const incidentId = this.dataset.incidentId;
                const incidentDate = this.dataset.incidentDate;
                const incidentStatus = this.dataset.incidentStatus;
                const incidentSeverity = this.dataset.incidentSeverity;
                const incidentAffectedComponents = this.dataset.incidentAffectedComponents;
                const incidentAffectedBikeId = this.dataset.incidentAffectedBikeId;
                const description = this.dataset.description?.replace(/&#10;/g, '\n')?.replace(/&quot;/g, '"') || '';
                const resolutionDate = this.dataset.resolutionDate;
                const resolutionNotes = this.dataset.resolutionNotes?.replace(/&#10;/g, '\n')?.replace(/&quot;/g, '"') || '';

                // Prepare component data
                const componentList = [];
                let hasComponents = false;
                if (incidentAffectedComponents && incidentAffectedComponents !== 'Not assigned') {
                    console.log("Processing components:", incidentAffectedComponents);
                    hasComponents = true;
                    
                    // Parse the JSON-like string back into an array
                    const componentIds = JSON.parse(incidentAffectedComponents);
                    componentIds.forEach(id => {
                        if (id) {
                            componentList.push(id);
                            console.log("Added component ID:", id);
                        }
                    });
                }
                
                // Store data for use by the modal
                pendingComponentData = {
                    hasComponents: hasComponents,
                    componentIds: componentList,
                    formData: {
                        incidentId: incidentId,
                        incidentDate: incidentDate,
                        incidentStatus: incidentStatus,
                        incidentSeverity: incidentSeverity,
                        incidentAffectedBikeId: incidentAffectedBikeId,
                        description: description,
                        resolutionDate: resolutionDate,
                        resolutionNotes: resolutionNotes
                    }
                };
                
                // Show the modal (which will trigger the shown.bs.modal event)
                const modal = new bootstrap.Modal(incidentModal);
                modal.show();
            });
        });
        
        // Initialize incident table functionality (sorting, filtering, searching and more)
        initializeIncidentTable();
        
        // Setup new incident button
        document.querySelectorAll('[data-bs-target="#incidentRecordModal"]').forEach(button => {
            button.addEventListener('click', function() {
                // Flag as new incident
                isNewIncident = true;
                pendingComponentData = null;
                
                // Reset the form
                document.getElementById('incidentRecordModalLabel').textContent = 'New incident report';
                document.getElementById('incident_form').action = '/add_incident_record';
                document.getElementById('incident_form').reset();
                document.getElementById('incident_id').value = '';
                document.getElementById('status_open').checked = true;

                // Reset ID display to placeholder text
                document.getElementById('incident-id-display').textContent = 'Not created yet';
                
                // Clear TomSelect if it's already initialized
                const componentSelect = document.getElementById('incident_affected_component_ids');
                if (componentSelect && (componentSelect.tomSelect || componentSelect.tomselect)) {
                    const ts = componentSelect.tomSelect || componentSelect.tomselect;
                    ts.clear();
                }
                
                // Show the modal
                const modal = new bootstrap.Modal(document.getElementById('incidentRecordModal'));
                modal.show();
            });
        });
    });
    
    // Initialize the component selector with delayed data loading
    function initializeComponentSelector(pendingData) {
        const componentSelect = document.getElementById('incident_affected_component_ids');
        if (!componentSelect) return;
        
        // Backup original options on first run
        if (!originalIncidentOptions) {
            originalIncidentOptions = componentSelect.innerHTML;
        }
        
        // Always start fresh with all options
        componentSelect.innerHTML = originalIncidentOptions;
        
        // Remove retired options if this is a new incident (before TomSelect sees them)
        if (isNewIncident) {
            const retiredOptions = componentSelect.querySelectorAll('option[data-status="Retired"]');
            retiredOptions.forEach(option => option.remove());
        }
        
        // Destroy existing TomSelect if it exists
        if (componentSelect.tomSelect || componentSelect.tomselect) {
            const ts = componentSelect.tomSelect || componentSelect.tomselect;
            ts.destroy();
        }
        
        // Initialize TomSelect with the current option set
        try {
            const ts = new TomSelect(componentSelect, {
                plugins: ['remove_button'],
                maxItems: null,
                valueField: 'value',
                labelField: 'text',
                searchField: ['text'],
                create: false,
                placeholder: 'Search to add more components...',
                shouldOpen: function() {
                    return this.isFocused && this.inputValue.length > 0;
                },
                openOnFocus: false,
                closeAfterSelect: true,
                onInitialize: function() {                    
                    // Handle initial component selection for new incidents
                    const initialComponentId = document.getElementById('initial_incident_component_id')?.value;
                    if (initialComponentId && isNewIncident) {
                        setTimeout(() => {
                            this.setValue([initialComponentId]);
                        }, 100);
                    }
                    // Handle edit mode data
                    else if (!isNewIncident && pendingData && pendingData.hasComponents && pendingData.componentIds.length > 0) {
                        setTimeout(() => {
                            this.clear();
                            this.setValue(pendingData.componentIds);
                        }, 50);
                    }
                    
                    if (!isNewIncident && pendingData && pendingData.formData) {
                        updateFormFields(pendingData.formData);
                    }
                }
            });
            
            // Store the new instance
            componentSelect.tomSelect = ts;
            
            // Add change handler for validation
            ts.on('change', function() {
                const tomSelectControl = document.querySelector('.ts-control');
                if (tomSelectControl) {
                    tomSelectControl.style.borderColor = '';
                }
                
                const bikeSelect = document.getElementById('incident_affected_bike_id');
                if (bikeSelect && ts.getValue().length > 0) {
                    bikeSelect.classList.remove('is-invalid');
                }
            });
            
        } catch (e) {
            console.error('TomSelect initialization error:', e);
        }
    }
    
    // Update form fields with data
    function updateFormFields(data) {
        // console.log("Form data received:", data);
        
        // Set basic form fields
        document.getElementById('incident_id').value = data.incidentId || '';
        document.getElementById('incident-id-display').textContent = data.incidentId || 'Not created yet';
        
        // Set status radio buttons
        if (data.incidentStatus === 'Resolved') {
            document.getElementById('status_resolved').checked = true;
        } else {
            document.getElementById('status_open').checked = true;
        }
        
        // Set other fields, checking for any variation of 'none' (case-insensitive)
        document.getElementById('incident_severity').value = data.incidentSeverity || 'Monitor';
        
        // Clean description
        const description = data.description || '';
        document.getElementById('incident_description').value = 
            description.toLowerCase() === 'none' ? '' : description;
        
        document.getElementById('incident_affected_bike_id').value = data.incidentAffectedBikeId || '';
        
        // Clean resolution notes
        const resolutionNotes = data.resolutionNotes || '';
        document.getElementById('resolution_notes').value = 
            resolutionNotes.toLowerCase() === 'none' ? '' : resolutionNotes;
        
        // Set date fields with a slight delay to ensure pickers are initialized
        setTimeout(() => {
            if (data.incidentDate) {
                document.getElementById('incident_date').value = data.incidentDate;
            }
            
            const resolutionDate = data.resolutionDate || '';
            if (resolutionDate && 
                resolutionDate !== '-' && 
                resolutionDate.toLowerCase() !== 'none') {
                document.getElementById('resolution_date').value = resolutionDate;
            } else {
                document.getElementById('resolution_date').value = '';
            }
        }, 100);
    }
})();

// Initialize the incident form and set up validation
function initializeIncidentForm() {
    const incidentForm = document.getElementById('incident_form');
    if (!incidentForm) return;

    // Clear the resolution date field
    const resolutionDateInput = document.getElementById('resolution_date');
    if (resolutionDateInput) {
        // Force resolution date to be empty on form initialization
        resolutionDateInput.value = '';
        
        // If the date picker has been initialized, try to update its value
        if (resolutionDateInput._tempusDominus) {
            try {
                resolutionDateInput._tempusDominus.clear();
            } catch (e) {
                console.warn('Error clearing date picker:', e);
            }
        }
    }

    // Set up form validation that works with the global validation
    if (incidentForm.getAttribute('data-incident-validation-initialized') !== 'true') {
        // Store original submit handler
        const originalSubmit = incidentForm.onsubmit;
        
        // Add our enhanced submit handler
        incidentForm.onsubmit = function(e) {
            // Always prevent default submission first
            e.preventDefault();
            e.stopPropagation();
            
            // Validate all date inputs in this form
            let dateValid = true;
            incidentForm.querySelectorAll('.datepicker-input').forEach(input => {
                if (!validateDateInput(input)) {
                    dateValid = false;
                }
            });
            
            // If dates are valid, check incident-specific validation
            if (dateValid && validateIncidentForm(this)) {
                // Use regular form submission (not bypassing handlers)
                // Wrap in timeout to ensure other handlers have run
                setTimeout(() => {
                    this.submit();
                }, 10);
            }
            
            // Always return false to prevent default submission
            return false;
        };
        
        // Mark form as initialized with our enhanced handler
        incidentForm.setAttribute('data-incident-validation-initialized', 'true');
    }

    // Add listener for status change to handle resolution date
    const statusRadios = incidentForm.querySelectorAll('input[name="incident_status"]');
    statusRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'Resolved') {
                // If status is resolved, make resolution date required
                resolutionDateInput.setAttribute('required', '');
                
                // Only set current date if the field is empty
                if (!resolutionDateInput.value) {
                    const now = new Date();
                    const formattedDate = now.getFullYear() + '-' + 
                        String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                        String(now.getDate()).padStart(2, '0') + ' ' + 
                        String(now.getHours()).padStart(2, '0') + ':' + 
                        String(now.getMinutes()).padStart(2, '0');
                    
                    resolutionDateInput.value = formattedDate;
                }
            } else {
                // If status is Open, resolution date is not required AND should be cleared
                resolutionDateInput.removeAttribute('required');
                resolutionDateInput.value = '';
                
                // If date picker is initialized, clear it too
                if (resolutionDateInput._tempusDominus) {
                    try {
                        resolutionDateInput._tempusDominus.clear();
                    } catch (e) {
                        console.warn('Error clearing date picker:', e);
                    }
                }
            }
        });
    });

    // Add handler for bike select validation
    const bikeSelect = document.getElementById('incident_affected_bike_id');
    if (bikeSelect) {
        bikeSelect.addEventListener('change', function() {
            this.classList.remove('is-invalid');
            
            // Also remove error styling from component select if bike is selected
            if (this.value) {
                const componentSelect = document.getElementById('incident_affected_component_ids');
                if (componentSelect && componentSelect.tomSelect) {
                    const tomSelectControl = document.querySelector('.ts-control');
                    if (tomSelectControl) {
                        tomSelectControl.style.borderColor = '';
                    }
                } else if (componentSelect) {
                    componentSelect.classList.remove('is-invalid');
                }
            }
        });
    }
}

// Function to validate the incident form
function validateIncidentForm(form) {
    // Reset any previous validation errors
    form.querySelectorAll('.is-invalid').forEach(input => {
        input.classList.remove('is-invalid');
    });
    
    let isValid = true;
    let errorMessage = "";
    
    // Get form values
    const incidentStatus = form.querySelector('input[name="incident_status"]:checked').value;
    const incidentDate = form.querySelector('#incident_date').value;
    const resolutionDate = form.querySelector('#resolution_date').value;
    
    let incidentAffectedComponents = [];
    const componentSelect = form.querySelector('#incident_affected_component_ids');
    if (componentSelect) {
        if (componentSelect.tomSelect) {
            incidentAffectedComponents = componentSelect.tomSelect.getValue();
        } else {
            incidentAffectedComponents = Array.from(componentSelect.selectedOptions).map(opt => opt.value);
        }
    }
    
    const incidentAffectedBikeId = form.querySelector('#incident_affected_bike_id').value;
    const now = new Date();

    // Validation rules

    // Incident date cannot be in the future
    if (incidentDate) {
        const incidentDateObj = new Date(incidentDate);
        if (incidentDateObj > now) {
            form.querySelector('#incident_date').classList.add('is-invalid');
            errorMessage = "Incident date cannot be in the future";
            isValid = false;
        }
    }

    // Resolution date cannot be in the future
    if (resolutionDate) {
        const resolutionDateObj = new Date(resolutionDate);
        if (resolutionDateObj > now) {
            form.querySelector('#resolution_date').classList.add('is-invalid');
            errorMessage = "Resolution date cannot be in the future";
            isValid = false;
        }
    }
    // If status is Resolved, resolution date must be provided
    if (incidentStatus === "Resolved" && !resolutionDate) {
        form.querySelector('#resolution_date').classList.add('is-invalid');
        errorMessage = "Resolution date is required when status is 'Resolved'";
        isValid = false;
    }
    
    // If status is Open, resolution date should be empty
    if (incidentStatus === "Open" && resolutionDate) {
        form.querySelector('#resolution_date').classList.add('is-invalid');
        errorMessage = "Resolution date should be empty when status is 'Open'";
        isValid = false;
    }
    
    // Resolution date cannot be at or before incident date
    if (resolutionDate && incidentDate) {
        const incidentDateObj = new Date(incidentDate);
        const resolutionDateObj = new Date(resolutionDate);
        
        if (resolutionDateObj <= incidentDateObj) {
            form.querySelector('#resolution_date').classList.add('is-invalid');
            errorMessage = "Resolution date must be after the incident date";
            isValid = false;
        }
    }
    
    // Either affected components or affected bike must be selected
    if ((!incidentAffectedComponents || incidentAffectedComponents.length === 0) && !incidentAffectedBikeId) {
        if (componentSelect && componentSelect.tomSelect) {
            // Add red border to TomSelect control
            const tomSelectControl = document.querySelector('.ts-control');
            if (tomSelectControl) {
                tomSelectControl.style.borderColor = '#dc3545';
            }
        } else if (componentSelect) {
            componentSelect.classList.add('is-invalid');
        }
        
        if (form.querySelector('#incident_affected_bike_id')) {
            form.querySelector('#incident_affected_bike_id').classList.add('is-invalid');
        }
        
        errorMessage = "Either affected components or an affected bike must be selected";
        isValid = false;
    }
    
    // Show validation modal if there are errors
    if (!isValid && errorMessage) {
        const modalBody = document.getElementById('validationModalBody');
        if (modalBody) {
            modalBody.innerHTML = errorMessage;
            if (typeof validationModal !== 'undefined' && validationModal) {
                validationModal.show();
            } else {
                // Fallback if the global validation modal isn't available
                const validationModalElement = document.getElementById('validationModal');
                if (validationModalElement) {
                    const bsValidationModal = new bootstrap.Modal(validationModalElement);
                    bsValidationModal.show();
                } else {
                    // Last resort - alert
                    alert(errorMessage);
                }
            }
        }
    }
    
    return isValid;
}

// Function to initialize the incident table with sorting, filtering and search
function initializeIncidentTable() {
    // Check if incidents table is available
    const table = document.getElementById('incidentsTable');
    if (!table) return;
    
    // Check for specific table types and initialize accordingly
    if (document.querySelector('h1#incident-reports')) {
        // Full incident page - use all functionality
        
        // Set up table sorting
        setupIncidentTableSorting();
        
        // Set up search functionality
        setupIncidentSearch();

        // Set up status filtering
        setupIncidentStatusFiltering();

    } else {
        // Simplified table on other pages - use simpler initialization
        // Add table functions here as needed
    }
}

// Function to set up incident table sorting
function setupIncidentTableSorting() {
    const table = document.getElementById('incidentsTable');
    if (!table) return;
    
    const headers = table.querySelectorAll('th[data-sort]');
    const tableBody = table.querySelector('tbody');
    const rows = tableBody.querySelectorAll('tr');
    
    // Skip if there are no rows or just one "no incidents" message row
    if (rows.length === 0 || (rows.length === 1 && rows[0].cells.length === 1)) return;
    
    // Sorting function
    const sortColumn = (index, asc = true) => {
        const nodeList = Array.from(rows);
        const compare = (rowA, rowB) => {
            // Skip if td doesn't exist in row
            if (!rowA.querySelectorAll('td')[index] || !rowB.querySelectorAll('td')[index]) return 0;
            
            // Get cell content and prepare for comparison
            let cellA = rowA.querySelectorAll('td')[index].innerText.trim();
            let cellB = rowB.querySelectorAll('td')[index].innerText.trim();
            
            // Different handling based on column type
            switch(index) {
                case 0: // Status column
                    // Sort by status - Open comes before Resolved
                    cellA = cellA.includes('Open') ? 0 : 1;
                    cellB = cellB.includes('Open') ? 0 : 1;
                    break;
                    
                case 1: // Bike column
                case 2: // Components column
                    // Simple text comparison, case-insensitive
                    cellA = cellA.toLowerCase();
                    cellB = cellB.toLowerCase();
                    break;
                    
                case 3: // Severity column
                    // Custom order: Critical > Priority > Monitor
                    const severityOrder = {
                        "Critical": 0,
                        "Priority": 1,
                        "Monitor": 2
                    };
                    cellA = severityOrder[cellA] !== undefined ? severityOrder[cellA] : 999;
                    cellB = severityOrder[cellB] !== undefined ? severityOrder[cellB] : 999;
                    break;
                    
                case 4: // Incident date column
                case 5: // Resolution date column
                    // Parse dates, handling "-" for empty dates
                    if (cellA === "-") cellA = asc ? "9999-12-31" : "0000-01-01";
                    if (cellB === "-") cellB = asc ? "9999-12-31" : "0000-01-01";
                    
                    // Compare as strings (YYYY-MM-DD format sorts correctly)
                    break;
                    
                case 6: // Days open column
                    // Parse as number
                    cellA = parseInt(cellA) || 0;
                    cellB = parseInt(cellB) || 0;
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

    // Add click event to table headers
    headers.forEach((header, index) => {
        header.addEventListener('click', () => {
            const isAscending = !header.classList.contains('sorted-asc');
            
            // Remove sorted classes from all headers
            headers.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
            
            // Add appropriate class to clicked header
            header.classList.add(isAscending ? 'sorted-asc' : 'sorted-desc');
            
            // Sort the column
            sortColumn(header.cellIndex, isAscending);
        });
    });

    // Initial sort by Incident Date (index 4) in descending order
    if (headers.length > 4 && rows.length > 1) {
        const dateHeader = Array.from(headers).find(h => h.getAttribute('data-sort') === 'incident_date');
        if (dateHeader) {
            dateHeader.classList.add('sorted-desc');
            sortColumn(dateHeader.cellIndex, false);
        }
    }
}

// Shared function to update incident visibility
function updateIncidentVisibility() {
    const incidentsTable = document.getElementById('incidentsTable');
    if (!incidentsTable) return;
    
    const rows = incidentsTable.querySelectorAll('tbody tr');
    const searchInput = document.getElementById('allIncidentsSearchInput');
    const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';
    
    // Get current filter states
    const showOpen = document.getElementById('showOpenIncidents').checked;
    const showResolved = document.getElementById('showResolvedIncidents').checked;
    
    rows.forEach(row => {
        // Skip the "no incidents" message row
        if (row.cells.length === 1 && row.cells[0].colSpan) {
            return;
        }
        
        // Check if row should be visible based on status filter
        let visibleByFilter = false;
        const statusCell = row.querySelector('td:nth-child(1)');
        if (statusCell) {
            const status = statusCell.textContent.trim();
            visibleByFilter = (
                (status.includes('Open') && showOpen) ||
                (status.includes('Resolved') && showResolved)
            );
        }
        
        // Check if row matches search term
        let matchesSearch = true;
        if (searchTerm) {
            const bikeText = row.cells[1].textContent.toLowerCase();
            const componentsText = row.cells[2].textContent.toLowerCase();
            const severityText = row.cells[3].textContent.toLowerCase();
            
            // Get hidden content from data attributes
            const descriptionText = (row.dataset.description || '').toLowerCase();
            const notesText = (row.dataset.notes || '').toLowerCase();
            
            // Include all text fields in the search
            const rowText = `${bikeText} ${componentsText} ${severityText} ${descriptionText} ${notesText}`;
            matchesSearch = rowText.includes(searchTerm);
        }
        
        // Show row only if it matches both filter and search criteria
        row.style.display = (visibleByFilter && matchesSearch) ? '' : 'none';
    });
    
    // Show a message if no results found
    const visibleRows = Array.from(rows).filter(row => row.style.display !== 'none');
    const noResultsRow = incidentsTable.querySelector('.no-results-row');
    
    if (visibleRows.length === 0 && (searchTerm !== '' || showOpen || showResolved)) {
        if (!noResultsRow) {
            const tbody = incidentsTable.querySelector('tbody');
            const newRow = document.createElement('tr');
            newRow.className = 'no-results-row';
            newRow.innerHTML = '<td colspan="8" class="text-center">No incidents match your criteria</td>';
            tbody.appendChild(newRow);
        } else {
            noResultsRow.style.display = '';
        }
    } else if (noResultsRow) {
        noResultsRow.style.display = 'none';
    }
}

// Function for filtering incident table by status
function setupIncidentStatusFiltering() {
    // Check if the incidents table is available
    const incidentsTable = document.getElementById('incidentsTable');
    if (!incidentsTable) return;

    const filterSwitches = document.querySelectorAll('.filter-switch');

    // Add event listeners to filter switches
    filterSwitches.forEach(switchElement => {
        switchElement.addEventListener('change', updateIncidentVisibility);
    });

    // Initial visibility update
    updateIncidentVisibility();
}

// Function to handle search across incidents
function setupIncidentSearch() {
    // Check if we're on the incidents page
    const searchInput = document.getElementById('allIncidentsSearchInput');
    if (!searchInput) return;
    
    // Listen for search input changes
    searchInput.addEventListener('input', updateIncidentVisibility);
    
    // Clear search button with Escape key
    searchInput.addEventListener('keyup', function(event) {
        if (event.key === 'Escape') {
            this.value = '';
            // Update visibility after clearing
            updateIncidentVisibility();
        }
    });
}

// ===== Workplan page functions =====

// Function to initialize workplan features
(function() {
    // Only run this code if the workplan modal is present
    if (!document.getElementById('workplanRecordModal')) {
        return;
    }
    
    // Local variables
    let pendingComponentData = null;
    let isNewWorkplan = false;
    let originalWorkplanOptions = null;
    
    // Initialize when the DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        const workplanModal = document.getElementById('workplanRecordModal');
        if (workplanModal) {
            // Setup modal shown event
            workplanModal.addEventListener('shown.bs.modal', function() {
                // console.log("Workplan modal shown, isNewWorkplan:", isNewWorkplan);
                initializeDatePickers(workplanModal);
                
                // If it's a new workplan, we need special handling
                if (isNewWorkplan) {
                    initializeComponentSelector(null);
                    
                    // Set current date after pickers are initialized
                    setTimeout(() => {
                        const now = new Date();
                        const formattedDate = now.getFullYear() + '-' + 
                            String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                            String(now.getDate()).padStart(2, '0') + ' ' + 
                            String(now.getHours()).padStart(2, '0') + ':' + 
                            String(now.getMinutes()).padStart(2, '0');
                        
                        document.getElementById('due_date').value = formattedDate;
                    }, 100);
                } else {
                    // For editing workplans
                    initializeComponentSelector(pendingComponentData);
                }
                
                // Call the existing form initialization function
                initializeWorkplanForm();
            });
            
            // Clean up when modal is hidden
            workplanModal.addEventListener('hidden.bs.modal', function() {
                // console.log("Workplan modal hidden - resetting flags");
                pendingComponentData = null;
                isNewWorkplan = false; // This should reset the flag
                
                // Also clear any TomSelect instances to prevent memory leaks
                const componentSelect = document.getElementById('workplan_affected_component_ids');
                if (componentSelect && (componentSelect.tomSelect || componentSelect.tomselect)) {
                    const ts = componentSelect.tomSelect || componentSelect.tomselect;
                    ts.destroy();
                    componentSelect.tomSelect = null;
                    componentSelect.tomselect = null;
                }
            });
        }
        
        // Setup edit button click handlers
        document.querySelectorAll('.edit-workplan-btn').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                isNewWorkplan = false;
                
                // Configure modal for editing
                document.getElementById('workplanRecordModalLabel').textContent = 'Edit workplan';
                document.getElementById('workplan_form').action = '/update_workplan';
                
                // Get data from the button
                const workplanId = this.dataset.workplanId;
                const dueDate = this.dataset.dueDate;
                const workplanStatus = this.dataset.workplanStatus;
                const workplanSize = this.dataset.workplanSize;
                const workplanAffectedComponents = this.dataset.workplanAffectedComponents;
                const workplanAffectedBikeId = this.dataset.workplanAffectedBikeId;
                const description = this.dataset.description?.replace(/&#10;/g, '\n')?.replace(/&quot;/g, '"') || '';
                const completionDate = this.dataset.completionDate;
                const completionNotes = this.dataset.completionNotes?.replace(/&#10;/g, '\n')?.replace(/&quot;/g, '"') || '';

                // Prepare component data
                const componentList = [];
                let hasComponents = false;
                if (workplanAffectedComponents && workplanAffectedComponents !== 'Not assigned') {
                    console.log("Processing components:", workplanAffectedComponents);
                    hasComponents = true;
                    
                    // Parse the JSON-like string back into an array
                    const componentIds = JSON.parse(workplanAffectedComponents);
                    componentIds.forEach(id => {
                        if (id) {
                            componentList.push(id);
                            console.log("Added component ID:", id);
                        }
                    });
                }
                
                // Store data for use by the modal
                pendingComponentData = {
                    hasComponents: hasComponents,
                    componentIds: componentList,
                    formData: {
                        workplanId: workplanId,
                        dueDate: dueDate,
                        workplanStatus: workplanStatus,
                        workplanSize: workplanSize,
                        workplanAffectedBikeId: workplanAffectedBikeId,
                        description: description,
                        completionDate: completionDate,
                        completionNotes: completionNotes
                    }
                };
                
                // Show the modal (which will trigger the shown.bs.modal event)
                const modal = new bootstrap.Modal(workplanModal);
                modal.show();
            });
        });
        
        // Initialize workplan table functionality (sorting, filtering, searching and more)
        initializeWorkplanTable();
        
        // Setup new workplan button
        document.querySelectorAll('[data-bs-target="#workplanRecordModal"]').forEach(button => {
            button.addEventListener('click', function() {
                // Flag as new workplan
                isNewWorkplan = true;
                pendingComponentData = null;
                
                // Reset the form
                document.getElementById('workplanRecordModalLabel').textContent = 'New workplan';
                document.getElementById('workplan_form').action = '/add_workplan';
                document.getElementById('workplan_form').reset();
                document.getElementById('workplan_id').value = '';
                document.getElementById('status_planned').checked = true;

                // Reset ID display to placeholder text
                document.getElementById('workplan-id-display').textContent = 'Not created yet';
                
                // Clear TomSelect if it's already initialized
                const componentSelect = document.getElementById('workplan_affected_component_ids');
                if (componentSelect && (componentSelect.tomSelect || componentSelect.tomselect)) {
                    const ts = componentSelect.tomSelect || componentSelect.tomselect;
                    ts.clear();
                }
                
                // Show the modal
                const modal = new bootstrap.Modal(document.getElementById('workplanRecordModal'));
                modal.show();
            });
        });
    });
    
    // Initialize the component selector with delayed data loading
    function initializeComponentSelector(pendingData) {
        const componentSelect = document.getElementById('workplan_affected_component_ids');
        if (!componentSelect) return;
        
        // Backup original options on first run
        if (!originalWorkplanOptions) {
            originalWorkplanOptions = componentSelect.innerHTML;
        }
        
        // Always start fresh with all options
        componentSelect.innerHTML = originalWorkplanOptions;
        
        // Remove retired options if this is a new workplan (before TomSelect sees them)
        if (isNewWorkplan) {
            const retiredOptions = componentSelect.querySelectorAll('option[data-status="Retired"]');
            retiredOptions.forEach(option => option.remove());
        }
        
        // Destroy existing TomSelect if it exists
        if (componentSelect.tomSelect || componentSelect.tomselect) {
            const ts = componentSelect.tomSelect || componentSelect.tomselect;
            ts.destroy();
        }
        
        // Initialize TomSelect with the current option set
        try {
            const ts = new TomSelect(componentSelect, {
                plugins: ['remove_button'],
                maxItems: null,
                valueField: 'value',
                labelField: 'text',
                searchField: ['text'],
                create: false,
                placeholder: 'Search to add more components...',
                shouldOpen: function() {
                    return this.isFocused && this.inputValue.length > 0;
                },
                openOnFocus: false,
                closeAfterSelect: true,
                onInitialize: function() {                    
                    // Handle initial component selection for new workplans
                    const initialComponentId = document.getElementById('initial_workplan_component_id')?.value;
                    if (initialComponentId && isNewWorkplan) {
                        setTimeout(() => {
                            this.setValue([initialComponentId]);
                        }, 100);
                    }
                    // Handle edit mode data
                    else if (!isNewWorkplan && pendingData && pendingData.hasComponents && pendingData.componentIds.length > 0) {
                        setTimeout(() => {
                            this.clear();
                            this.setValue(pendingData.componentIds);
                        }, 50);
                    }
                    
                    if (!isNewWorkplan && pendingData && pendingData.formData) {
                        updateFormFields(pendingData.formData);
                    }
                }
            });
            
            // Store the new instance
            componentSelect.tomSelect = ts;
            
            // Add change handler for validation
            ts.on('change', function() {
                const tomSelectControl = document.querySelector('.ts-control');
                if (tomSelectControl) {
                    tomSelectControl.style.borderColor = '';
                }
                
                const bikeSelect = document.getElementById('workplan_affected_bike_id');
                if (bikeSelect && ts.getValue().length > 0) {
                    bikeSelect.classList.remove('is-invalid');
                }
            });
            
        } catch (e) {
            console.error('TomSelect initialization error:', e);
        }
    }
    
    // Update form fields with data
    function updateFormFields(data) {
        // console.log("Form data received:", data);
        
        // Set basic form fields
        document.getElementById('workplan_id').value = data.workplanId || '';
        document.getElementById('workplan-id-display').textContent = data.workplanId || 'Not created yet';
        
        // Set status radio buttons
        if (data.workplanStatus === 'Done') {
            document.getElementById('status_done').checked = true;
        } else {
            document.getElementById('status_planned').checked = true;
        }
        
        // Set other fields, checking for any variation of 'none' (case-insensitive)
        document.getElementById('workplan_size').value = data.workplanSize || 'Small';
        
        // Clean description
        const description = data.description || '';
        document.getElementById('workplan_description').value = 
            description.toLowerCase() === 'none' ? '' : description;
        
        document.getElementById('workplan_affected_bike_id').value = data.workplanAffectedBikeId || '';
        
        // Clean completion notes
        const completionNotes = data.completionNotes || '';
        document.getElementById('completion_notes').value = 
            completionNotes.toLowerCase() === 'none' ? '' : completionNotes;
        
        // Set date fields with a slight delay to ensure pickers are initialized
        setTimeout(() => {
            if (data.dueDate) {
                document.getElementById('due_date').value = data.dueDate;
            }
            
            const completionDate = data.completionDate || '';
            if (completionDate && 
                completionDate !== '-' && 
                completionDate.toLowerCase() !== 'none') {
                document.getElementById('completion_date').value = completionDate;
            } else {
                document.getElementById('completion_date').value = '';
            }
        }, 100);
    }
})();

// Initialize the workplan form and set up validation
function initializeWorkplanForm() {
    const workplanForm = document.getElementById('workplan_form');
    if (!workplanForm) return;

    // Clear the completion date field
    const completionDateInput = document.getElementById('completion_date');
    if (completionDateInput) {
        // Force completion date to be empty on form initialization
        completionDateInput.value = '';
        
        // If the date picker has been initialized, try to update its value
        if (completionDateInput._tempusDominus) {
            try {
                completionDateInput._tempusDominus.clear();
            } catch (e) {
                console.warn('Error clearing date picker:', e);
            }
        }
    }

    // Set up form validation that works with the global validation
    if (workplanForm.getAttribute('data-workplan-validation-initialized') !== 'true') {
        // Store original submit handler
        const originalSubmit = workplanForm.onsubmit; // Can this be delete?
        
        // Add our enhanced submit handler
        workplanForm.onsubmit = function(e) {
            // Always prevent default submission first
            e.preventDefault();
            e.stopPropagation();
            
            // Validate all date inputs in this form
            let dateValid = true;
            workplanForm.querySelectorAll('.datepicker-input').forEach(input => {
                if (!validateDateInput(input)) {
                    dateValid = false;
                }
            });
            
            // If dates are valid, check workplan-specific validation
            if (dateValid && validateWorkplanForm(this)) {
                // Use regular form submission (not bypassing handlers)
                // Wrap in timeout to ensure other handlers have run
                setTimeout(() => {
                    this.submit();
                }, 10);
            }
            
            // Always return false to prevent default submission
            return false;
        };
        
        // Mark form as initialized with our enhanced handler
        workplanForm.setAttribute('data-workplan-validation-initialized', 'true');
    }

    // Add listener for status change to handle completion date
    const statusRadios = workplanForm.querySelectorAll('input[name="workplan_status"]');
    statusRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'Done') {
                // If status is Done, make completion date required
                completionDateInput.setAttribute('required', '');
                
                // Only set current date if the field is empty
                if (!completionDateInput.value) {
                    const now = new Date();
                    const formattedDate = now.getFullYear() + '-' + 
                        String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                        String(now.getDate()).padStart(2, '0') + ' ' + 
                        String(now.getHours()).padStart(2, '0') + ':' + 
                        String(now.getMinutes()).padStart(2, '0');
                    
                    completionDateInput.value = formattedDate;
                }
            } else {
                // If status is Planned, completion date is not required AND should be cleared
                completionDateInput.removeAttribute('required');
                completionDateInput.value = '';
                
                // If date picker is initialized, clear it too
                if (completionDateInput._tempusDominus) {
                    try {
                        completionDateInput._tempusDominus.clear();
                    } catch (e) {
                        console.warn('Error clearing date picker:', e);
                    }
                }
            }
        });
    });

    // Add handler for bike select validation
    const bikeSelect = document.getElementById('workplan_affected_bike_id');
    if (bikeSelect) {
        bikeSelect.addEventListener('change', function() {
            this.classList.remove('is-invalid');
            
            // Also remove error styling from component select if bike is selected
            if (this.value) {
                const componentSelect = document.getElementById('workplan_affected_component_ids');
                if (componentSelect && componentSelect.tomSelect) {
                    const tomSelectControl = document.querySelector('.ts-control');
                    if (tomSelectControl) {
                        tomSelectControl.style.borderColor = '';
                    }
                } else if (componentSelect) {
                    componentSelect.classList.remove('is-invalid');
                }
            }
        });
    }
}

// Function to validate the workplan form
function validateWorkplanForm(form) {
    // Reset any previous validation errors
    form.querySelectorAll('.is-invalid').forEach(input => {
        input.classList.remove('is-invalid');
    });
    
    let isValid = true;
    let errorMessage = "";
    
    // Get form values
    const workplanStatus = form.querySelector('input[name="workplan_status"]:checked').value;
    const dueDate = form.querySelector('#due_date').value;
    const completionDate = form.querySelector('#completion_date').value;
    
    let workplanAffectedComponents = [];
    const componentSelect = form.querySelector('#workplan_affected_component_ids');
    if (componentSelect) {
        if (componentSelect.tomSelect) {
            workplanAffectedComponents = componentSelect.tomSelect.getValue();
        } else {
            workplanAffectedComponents = Array.from(componentSelect.selectedOptions).map(opt => opt.value);
        }
    }
    
    const workplanAffectedBikeId = form.querySelector('#workplan_affected_bike_id').value;
    const now = new Date();
    
    // Validation rules

    // Completion date cannot be in the future (due date CAN be in the future)
    if (completionDate) {
        const completionDateObj = new Date(completionDate);
        if (completionDateObj > now) {
            form.querySelector('#completion_date').classList.add('is-invalid');
            errorMessage = "Completion date cannot be in the future";
            isValid = false;
        }
    }

    // If status is Done, completion date must be provided
    if (workplanStatus === "Done" && !completionDate) {
        form.querySelector('#completion_date').classList.add('is-invalid');
        errorMessage = "Completion date is required when status is 'Done'";
        isValid = false;
    }
    
    // If status is Planned, completion date should be empty
    if (workplanStatus === "Planned" && completionDate) {
        form.querySelector('#completion_date').classList.add('is-invalid');
        errorMessage = "Completion date should be empty when status is 'Planned'";
        isValid = false;
    }
    
    // Either affected components or affected bike must be selected
    if ((!workplanAffectedComponents || workplanAffectedComponents.length === 0) && !workplanAffectedBikeId) {
        if (componentSelect && componentSelect.tomSelect) {
            // Add red border to TomSelect control
            const tomSelectControl = document.querySelector('.ts-control');
            if (tomSelectControl) {
                tomSelectControl.style.borderColor = '#dc3545';
            }
        } else if (componentSelect) {
            componentSelect.classList.add('is-invalid');
        }
        
        if (form.querySelector('#workplan_affected_bike_id')) {
            form.querySelector('#workplan_affected_bike_id').classList.add('is-invalid');
        }
        
        errorMessage = "Either affected components or an affected bike must be selected";
        isValid = false;
    }
    
    // Show validation modal if there are errors
    if (!isValid && errorMessage) {
        const modalBody = document.getElementById('validationModalBody');
        if (modalBody) {
            modalBody.innerHTML = errorMessage;
            if (typeof validationModal !== 'undefined' && validationModal) {
                validationModal.show();
            } else {
                // Fallback if the global validation modal isn't available
                const validationModalElement = document.getElementById('validationModal');
                if (validationModalElement) {
                    const bsValidationModal = new bootstrap.Modal(validationModalElement);
                    bsValidationModal.show();
                } else {
                    // Last resort - alert
                    alert(errorMessage);
                }
            }
        }
    }
    
    return isValid;
}

// Function to initialize the workplan table with sorting, filtering and search
function initializeWorkplanTable() {
    // Check if workplans table is available
    const table = document.getElementById('workplansTable');
    if (!table) return;
    
    // Check for specific table types and initialize accordingly
    if (document.querySelector('h1#workplans')) {
        // Full workplan page - use all functionality
        
        // Set up table sorting
        setupWorkplanTableSorting();
        
        // Set up search functionality
        setupWorkplanSearch();

        // Set up status filtering
        setupWorkplanStatusFiltering();

    } else {
        // Simplified table on other pages - use simpler initialization
        // Add table functions here as needed
    }
}

// Function to set up workplan table sorting
function setupWorkplanTableSorting() {
    const table = document.getElementById('workplansTable');
    if (!table) return;
    
    const headers = table.querySelectorAll('th[data-sort]');
    const tableBody = table.querySelector('tbody');
    const rows = tableBody.querySelectorAll('tr');
    
    // Skip if there are no rows or just one "no workplans" message row
    if (rows.length === 0 || (rows.length === 1 && rows[0].cells.length === 1)) return;
    
    // Sorting function
    const sortColumn = (index, asc = true) => {
        const nodeList = Array.from(rows);
        const compare = (rowA, rowB) => {
            // Skip if td doesn't exist in row
            if (!rowA.querySelectorAll('td')[index] || !rowB.querySelectorAll('td')[index]) return 0;
            
            // Get cell content and prepare for comparison
            let cellA = rowA.querySelectorAll('td')[index].innerText.trim();
            let cellB = rowB.querySelectorAll('td')[index].innerText.trim();
            
            // Different handling based on column type
            switch(index) {
                case 0: // Status column
                // Sort by status - custom order for statuses
                const statusOrder = {
                    "Overdue": 0,
                    "Planned": 1,
                    "Done": 2
                };
                // Extract status text from the badge
                const statusTextA = cellA.includes('Overdue') ? 'Overdue' : 
                                (cellA.includes('Planned') ? 'Planned' : 'Done');
                const statusTextB = cellB.includes('Overdue') ? 'Overdue' : 
                                (cellB.includes('Planned') ? 'Planned' : 'Done');
                
                cellA = statusOrder[statusTextA] !== undefined ? statusOrder[statusTextA] : 999;
                cellB = statusOrder[statusTextB] !== undefined ? statusOrder[statusTextB] : 999;
                break;
                    
                case 4: // Due date column
                case 5: // Completion date column
                    // Parse dates, handling "-" for empty dates
                    if (cellA === "-") cellA = asc ? "9999-12-31" : "0000-01-01";
                    if (cellB === "-") cellB = asc ? "9999-12-31" : "0000-01-01";
                    
                    // Compare as strings (YYYY-MM-DD format sorts correctly)
                    break;
                    
                case 6: // Days open column
                    // Parse as number
                    cellA = parseInt(cellA) || 0;
                    cellB = parseInt(cellB) || 0;
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

    // Add click event to table headers
    headers.forEach((header, index) => {
        header.addEventListener('click', () => {
            const isAscending = !header.classList.contains('sorted-asc');
            
            // Remove sorted classes from all headers
            headers.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
            
            // Add appropriate class to clicked header
            header.classList.add(isAscending ? 'sorted-asc' : 'sorted-desc');
            
            // Sort the column
            sortColumn(header.cellIndex, isAscending);
        });
    });

    // Initial sort by due date (index 4) in ascending order
    if (headers.length > 4 && rows.length > 1) {
        const dateHeader = Array.from(headers).find(h => h.getAttribute('data-sort') === 'due_date');
        if (dateHeader) {
            dateHeader.classList.add('sorted-asc');
            sortColumn(dateHeader.cellIndex, true);
        }
    }
}

// Shared function to update workplan visibility
function updateWorkplansVisibility() {
    const workplansTable = document.getElementById('workplansTable');
    if (!workplansTable) return;
    
    const rows = workplansTable.querySelectorAll('tbody tr');
    const searchInput = document.getElementById('allWorkplansSearchInput');
    const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';
    
    // Get current filter states
    const showPlanned = document.getElementById('showPlannedWorkplans').checked;
    const showDone = document.getElementById('showDoneWorkplans').checked;
    
    rows.forEach(row => {
        // Skip the "no workplans" message row
        if (row.cells.length === 1 && row.cells[0].colSpan) {
            return;
        }
        
        // Check if row should be visible based on status filter
        let visibleByFilter = false;
        const statusCell = row.querySelector('td:nth-child(1)');
        if (statusCell) {
            const statusText = statusCell.textContent.trim();
            visibleByFilter = (
                // Show "Overdue" when "Planned" is checked
                ((statusText.includes('Planned') || statusText.includes('Overdue')) && showPlanned) ||
                (statusText.includes('Done') && showDone)
            );
        }
        
        // Check if row matches search term
        let matchesSearch = true;
        if (searchTerm) {
            const bikeText = row.cells[1].textContent.toLowerCase();
            const componentsText = row.cells[2].textContent.toLowerCase();
            const severityText = row.cells[3].textContent.toLowerCase();
            
            // Get hidden content from data attributes
            const descriptionText = (row.dataset.description || '').toLowerCase();
            const notesText = (row.dataset.notes || '').toLowerCase();
            
            // Include all text fields in the search
            const rowText = `${bikeText} ${componentsText} ${severityText} ${descriptionText} ${notesText}`;
            matchesSearch = rowText.includes(searchTerm);
        }
        
        // Show row only if it matches both filter and search criteria
        row.style.display = (visibleByFilter && matchesSearch) ? '' : 'none';
    });
    
    // Show a message if no results found
    const visibleRows = Array.from(rows).filter(row => row.style.display !== 'none');
    const noResultsRow = workplansTable.querySelector('.no-results-row');
    
    if (visibleRows.length === 0 && (searchTerm !== '' || showPlanned || showDone)) {
        if (!noResultsRow) {
            const tbody = workplansTable.querySelector('tbody');
            const newRow = document.createElement('tr');
            newRow.className = 'no-results-row';
            newRow.innerHTML = '<td colspan="8" class="text-center">No workplans match your criteria</td>';
            tbody.appendChild(newRow);
        } else {
            noResultsRow.style.display = '';
        }
    } else if (noResultsRow) {
        noResultsRow.style.display = 'none';
    }
}

// Function for filtering workplan table by status
function setupWorkplanStatusFiltering() {
    // Check if the workplans table is available
    const workplansTable = document.getElementById('workplansTable');
    if (!workplansTable) return;

    const filterSwitches = document.querySelectorAll('.filter-switch');

    // Add event listeners to filter switches
    filterSwitches.forEach(switchElement => {
        switchElement.addEventListener('change', updateWorkplansVisibility);
    });

    // Initial visibility update
    updateWorkplansVisibility();
}

// Function to handle search across workplans
function setupWorkplanSearch() {
    // Check if we're on the workplans page
    const searchInput = document.getElementById('allWorkplansSearchInput');
    if (!searchInput) return;
    
    // Listen for search input changes
    searchInput.addEventListener('input', updateWorkplansVisibility);
    
    // Clear search button with Escape key
    searchInput.addEventListener('keyup', function(event) {
        if (event.key === 'Escape') {
            this.value = '';
            // Update visibility after clearing
            updateWorkplansVisibility();
        }
    });
}

// ===== Component types page functions =====

// Function to modify component types
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the component types page
    if (document.querySelector('h1#component-types') === null) return;
    
    // Get the component type modal
    const componentTypeModal = new bootstrap.Modal(document.getElementById('componentTypeModal'));
    
    // Modify record function: get all modify record buttons
    const modifyRecordButtons = document.querySelectorAll('.modify-record');

    // Add a click event listener to each button
    modifyRecordButtons.forEach(button => {
        button.addEventListener('click', () => {
            const rowId = button.dataset.rowId;
            const componentType = button.getAttribute('component_type');
            modifyRecord(rowId, componentType);
            
            // Update modal title to indicate editing
            document.getElementById('componentTypeModalLabel').textContent = 'Edit component type';

            // Set mode to "update" when editing
            document.getElementById('mode').value = "update";

            // Disable the component_type field since it's a primary key
            const componentTypeInput = document.getElementById('component_type');
            componentTypeInput.readOnly = true;
            componentTypeInput.classList.add('bg-light');
            
            // Show the modal after data is populated
            componentTypeModal.show();
        });
    });

    // Define the modifyRecord function
    function modifyRecord(rowId, componentType) {
        const row = document.querySelector(`tr[data-row-id="${rowId}"]`);
        if (row) {
            // Set component type (from column 1)
            document.getElementById('component_type').value = componentType;
            
            // Set max quantity (from column 2)
            const maxQuantityCell = row.cells[2].textContent.trim();
            document.getElementById('max_quantity').value = maxQuantityCell !== 'Not defined' ? 
                maxQuantityCell : '';
            
            // Set mandatory radio buttons (from column 0)
            const hasStar = row.cells[0].textContent.includes('⭐');
            document.getElementById('mandatory_yes').checked = hasStar;
            document.getElementById('mandatory_no').checked = !hasStar;
            
            // Set expected lifetime (from column 4)
            const expectedLifetimeCell = row.cells[4].textContent.trim();
            document.getElementById('expected_lifetime').value = expectedLifetimeCell !== 'Not defined' ? 
                expectedLifetimeCell : '';
            
            // Set service interval (from column 5)
            const serviceIntervalCell = row.cells[5].textContent.trim();
            document.getElementById('service_interval').value = serviceIntervalCell !== 'Not defined' ? 
                serviceIntervalCell : '';
            
            // No need to set service_interval_days since it's currently only a a placeholder
        } else {
            console.error(`Row with ID ${rowId} not found.`);
        }
    }
    
    // Add handler for the "New component type" button
    document.querySelector('[data-bs-toggle="modal"][data-bs-target="#componentTypeModal"]')?.addEventListener('click', function() {
        // Reset the form
        document.getElementById('component_type_form').reset();
        
        // Reset modal title to indicate creating new type
        document.getElementById('componentTypeModalLabel').textContent = 'New component type';

        // Enable the component_type field for new records
        const componentTypeInput = document.getElementById('component_type');
        componentTypeInput.readOnly = false;
        componentTypeInput.classList.remove('bg-light');
    });
});

// Add search filtering and sorting for component types table
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the component types page
    if (document.querySelector('h1#component-types') === null) return;
    
    const searchInput = document.getElementById('componentTypeSearchInput');
    if (!searchInput) return;
    
    const table = document.querySelector('.card-body .table');
    const headers = table.querySelectorAll('thead th');
    const tableBody = table.querySelector('tbody');
    const rows = tableBody.querySelectorAll('tr');
    
    // Skip if there are no rows or just one "no component types" message row
    if (rows.length === 0 || (rows.length === 1 && rows[0].cells.length === 1)) return;
    
    // Add data-sort attribute and sort indicators to headers
    headers.forEach((header, index) => {
        // Skip only the last column (with action buttons)
        if (index === headers.length - 1) return;
        
        // Add data-sort attribute to make headers sortable
        header.setAttribute('data-sort', '');
        
        // Add sort indicator span if it doesn't exist
        if (!header.querySelector('.sort-indicator')) {
            const indicator = document.createElement('span');
            indicator.className = 'sort-indicator';
            header.appendChild(indicator);
        }
    });
    
    // Sorting function
    const sortColumn = (index, asc = true) => {
        const nodeList = Array.from(rows);
        const compare = (rowA, rowB) => {
            // Skip if td doesn't exist in row (for the "no component types defined" row)
            if (!rowA.querySelectorAll('td')[index] || !rowB.querySelectorAll('td')[index]) return 0;
            
            // Get cell content and prepare for comparison
            let cellA = rowA.querySelectorAll('td')[index].innerText.trim();
            let cellB = rowB.querySelectorAll('td')[index].innerText.trim();
            
            // Different handling based on column type
            switch(index) {
                case 0: // Star (mandatory) column
                    // Sort by presence of star (⭐)
                    cellA = cellA.includes('⭐') ? 1 : 0;
                    cellB = cellB.includes('⭐') ? 1 : 0;
                    break;
                    
                case 1: // Type column
                    // Compare case-insensitively for text
                    cellA = cellA.toLowerCase();
                    cellB = cellB.toLowerCase();
                    break;
                    
                case 2: // Max per bike column
                    // Extract numeric value or set to Infinity if "Not defined"
                    cellA = cellA === 'Not defined' ? Infinity : parseInt(cellA, 10) || 0;
                    cellB = cellB === 'Not defined' ? Infinity : parseInt(cellB, 10) || 0;
                    break;
                    
                case 3: // Status use column
                    // Extract number of components or set to 0 if none
                    const numA = cellA.match(/(\d+) components/);
                    const numB = cellB.match(/(\d+) components/);
                    cellA = numA ? parseInt(numA[1], 10) : 0;
                    cellB = numB ? parseInt(numB[1], 10) : 0;
                    break;
                    
                case 4: // Expected life column
                case 5: // Service interval (km) column
                case 6: // Service interval (days) column
                    // Extract numeric value or set to Infinity if "Not defined"
                    cellA = cellA === 'Not defined' || cellA === 'N/A' ? Infinity : parseInt(cellA, 10) || 0;
                    cellB = cellB === 'Not defined' || cellB === 'N/A' ? Infinity : parseInt(cellB, 10) || 0;
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
    
    // Add click event to table headers
    headers.forEach((header, index) => {
        // Skip the last column (with action buttons)
        if (index === headers.length - 1) return;
        
        header.addEventListener('click', () => {
            const isAscending = !header.classList.contains('sorted-asc');
            
            // Remove sorted classes from all headers
            headers.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
            
            // Add appropriate class to clicked header
            header.classList.add(isAscending ? 'sorted-asc' : 'sorted-desc');
            
            sortColumn(index, isAscending);
        });
    });
    
    // Function to update row visibility based on search
    function updateRowVisibility() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        
        rows.forEach(row => {
            // Skip the "no component types defined" row
            if (row.cells.length === 1 && row.cells[0].colSpan) {
                return;
            }
            
            // Get text from type column (column 1)
            const type = row.cells[1].textContent.toLowerCase();
            const matchesSearch = searchTerm === '' || type.includes(searchTerm);
            
            // Show/hide row based on search match
            row.style.display = matchesSearch ? '' : 'none';
        });
        
        // Show a message if no results found
        const visibleRows = Array.from(rows).filter(row => row.style.display !== 'none');
        const noResultsRow = table.querySelector('.no-results-row');
        
        if (visibleRows.length === 0 && searchTerm !== '') {
            if (!noResultsRow) {
                const tbody = table.querySelector('tbody');
                const newRow = document.createElement('tr');
                newRow.className = 'no-results-row';
                newRow.innerHTML = '<td colspan="8" class="text-center">No component types match your search</td>';
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
    
    // Clear search with Escape key
    searchInput.addEventListener('keyup', function(event) {
        if (event.key === 'Escape') {
            this.value = '';
            updateRowVisibility();
        }
    });
    
    // Initial sort by Type column (index 1) in ascending order
    if (headers.length > 1 && rows.length > 1) {
        // Add sorted-asc class to the Type column header
        headers[1].classList.add('sorted-asc');
        
        // Sort by Type column (index 1) in ascending order
        sortColumn(1, true);
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

// ===== Collections page functions =====

// Function to initialize collection features
(function() {
    // Only run this code if the collection modal is present
    if (!document.getElementById('collectionModal')) {
        return;
    }
    
    // Local variables
    let pendingComponentData = null;
    let isNewCollection = false;
    let originalCollectionOptions = null;
    
    // Initialize when the DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        const collectionModal = document.getElementById('collectionModal');
        if (collectionModal) {
            // Setup modal shown event
            collectionModal.addEventListener('shown.bs.modal', function() {
                // Initialize date picker (this will auto-set current date for empty inputs)
                initializeDatePickers(collectionModal);
                
                // If it's a new collection, we need special handling
                if (isNewCollection) {
                    initializeComponentSelector(null);
                    
                    if (pendingComponentData) {
                        setTimeout(() => {
                            setSelectedComponents(pendingComponentData);
                        }, 100);
                    }
                }
                
                // Set up component validation
                setupComponentValidation();
            });

            // Setup modal hidden event
            collectionModal.addEventListener('hidden.bs.modal', function() {
                // Reset flags
                isNewCollection = false;
                pendingComponentData = null;
                
                // Hide warning sections
                document.getElementById('mixed_status_warning').style.display = 'none';
            });
        }
        
        // Setup edit collection buttons
        document.querySelectorAll('.edit-collection-btn').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                isNewCollection = false;
                
                // Configure modal for editing
                document.getElementById('collectionModalLabel').textContent = 'Edit collection';
                document.getElementById('collection_form').action = '/update_collection';
                
                // Get data from the button
                const collectionId = this.dataset.collectionId;
                const collectionName = this.dataset.collectionName;
                const components = this.dataset.components ? JSON.parse(this.dataset.components) : [];
                const bikeId = this.dataset.bikeId || '';
                const comment = this.dataset.comment || '';
                const updatedDate = this.dataset.updatedDate || '';
                
                // Populate form fields
                document.getElementById('collection_id').value = collectionId;
                document.getElementById('collection_name').value = collectionName;
                document.getElementById('collection_bike_id').value = bikeId;
                document.getElementById('collection_comment').value = comment;
                document.getElementById('updated_date').value = updatedDate;
                
                // Update ID display
                document.getElementById('collection-id-display').textContent = collectionId;
                
                // Initialize component selector and set selected components
                initializeComponentSelector();
                setTimeout(() => {
                    if (components && components.length > 0) {
                        setSelectedComponents(components);
                    }
                    setupComponentValidation();
                }, 100);
                
                // Show the modal
                const modal = new bootstrap.Modal(document.getElementById('collectionModal'));
                modal.show();
            });
        });
        
        // Setup new collection button
        document.querySelectorAll('[data-bs-target="#collectionModal"]').forEach(button => {
            button.addEventListener('click', function() {
                // Flag as new collection
                isNewCollection = true;
                pendingComponentData = null;
                
                // Reset the form
                document.getElementById('collectionModalLabel').textContent = 'New collection';
                document.getElementById('collection_form').action = '/add_collection';
                document.getElementById('collection_form').reset();
                document.getElementById('collection_id').value = '';
                
                // Reset ID display to placeholder text
                document.getElementById('collection-id-display').textContent = 'Not created yet';
                
                // Clear TomSelect if it's already initialized
                const componentSelect = document.getElementById('collection_component_ids');
                if (componentSelect.tomSelect || componentSelect.tomselect) {
                    const ts = componentSelect.tomSelect || componentSelect.tomselect;
                    ts.clear();
                }
                
                // Hide warning sections
                document.getElementById('mixed_status_warning').style.display = 'none';
                
                // Show the modal
                const modal = new bootstrap.Modal(document.getElementById('collectionModal'));
                modal.show();
            });
        });
    });
    
    // Initialize the component selector with delayed data loading
    function initializeComponentSelector(pendingData) {
        const componentSelect = document.getElementById('collection_component_ids');
        if (!componentSelect) return;
        
        // Only initialize if not already done
        if (componentSelect.tomSelect || componentSelect.tomselect) {
            return;
        }
        
        new TomSelect(componentSelect, {
            plugins: ['remove_button'],
            placeholder: 'Search and select components...',
            searchField: ['text'],
            labelField: 'text',
            valueField: 'value',
            options: Array.from(componentSelect.options).map(option => ({
                value: option.value,
                text: option.textContent,
                status: option.dataset.status,
                bike: option.dataset.bike
            })),
            render: {
                option: function(data, escape) {
                    const statusBadge = data.status === 'Installed' ? 
                        '<span class="badge bg-success ms-2">Installed</span>' :
                        data.status === 'Retired' ?
                        '<span class="badge bg-secondary ms-2">Retired</span>' :
                        '<span class="badge bg-warning text-dark ms-2">Not installed</span>';
                    
                    return '<div>' + escape(data.text) + statusBadge + '</div>';
                },
                item: function(data, escape) {
                    return '<div>' + escape(data.text) + '</div>';
                }
            },
            onChange: function(values) {
                // Trigger validation when components change
                setTimeout(setupComponentValidation, 50);
            }
        });
    }
    
    // Set selected components in the TomSelect
    function setSelectedComponents(componentIds) {
        const componentSelect = document.getElementById('collection_component_ids');
        if (!componentSelect) return;
        
        const tomSelect = componentSelect.tomSelect || componentSelect.tomselect;
        if (tomSelect && componentIds) {
            tomSelect.setValue(componentIds);
        }
    }
    
    // Setup component validation and status checking
    function setupComponentValidation() {
        const componentSelect = document.getElementById('collection_component_ids');
        const bikeSelect = document.getElementById('collection_bike_id');
        const mixedStatusWarning = document.getElementById('mixed_status_warning');
        const bulkStatusSection = document.getElementById('bulk_status_section');
        
        if (!componentSelect) return;
        
        const tomSelect = componentSelect.tomSelect || componentSelect.tomselect;
        if (!tomSelect) return;
        
        const selectedValues = tomSelect.getValue();
        if (!selectedValues || selectedValues.length === 0) {
            mixedStatusWarning.style.display = 'none';
            bulkStatusSection.style.display = 'block';
            return;
        }
        
        // Get status information for selected components
        const selectedOptions = selectedValues.map(value => {
            const option = componentSelect.querySelector(`option[value="${value}"]`);
            return {
                id: value,
                status: option ? option.dataset.status : null,
                bike: option ? option.dataset.bike : null
            };
        });
        
        // Check for mixed statuses
        const statuses = [...new Set(selectedOptions.map(opt => opt.status))];
        const hasMixedStatuses = statuses.length > 1;
        
        // Check for installed components
        const hasInstalledComponents = selectedOptions.some(opt => opt.status === 'Installed');
        
        // Show/hide mixed status warning
        if (hasMixedStatuses) {
            mixedStatusWarning.style.display = 'block';
        } else {
            mixedStatusWarning.style.display = 'none';
        }
        
        // Always show bulk status section
        bulkStatusSection.style.display = 'block';
        
        // Validate bike assignment for installed components
        if (hasInstalledComponents && !bikeSelect.value) {
            bikeSelect.classList.add('is-invalid');
            if (!bikeSelect.nextElementSibling || !bikeSelect.nextElementSibling.classList.contains('invalid-feedback')) {
                const feedback = document.createElement('div');
                feedback.className = 'invalid-feedback';
                feedback.textContent = 'Required when collection contains installed components';
                bikeSelect.parentNode.appendChild(feedback);
            }
        } else {
            bikeSelect.classList.remove('is-invalid');
            const feedback = bikeSelect.parentNode.querySelector('.invalid-feedback');
            if (feedback) {
                feedback.remove();
            }
        }
    }
    
    // Setup bulk status change functionality
    document.addEventListener('DOMContentLoaded', function() {
        const applyStatusBtn = document.getElementById('apply_status_change');
        if (applyStatusBtn) {
            applyStatusBtn.addEventListener('click', function() {
                const newStatus = document.getElementById('new_status').value;
                const collectionId = document.getElementById('collection_id').value;
                const updatedDate = document.getElementById('updated_date').value;
                
                if (!newStatus || !collectionId) {
                    showToast('Please select a new status and ensure the collection is saved first.', 'warning');
                    return;
                }
                
                if (!updatedDate) {
                    showToast('Please select a status change date.', 'warning');
                    return;
                }
                
                // Show confirmation
                showConfirmModal(
                    'Change Component Status',
                    `Are you sure you want to change the status of all components in this collection to "${newStatus}"?`,
                    function() {
                        // Perform bulk status change
                        performBulkStatusChange(collectionId, newStatus, updatedDate);
                    }
                );
            });
        }
    });
    
    // Perform bulk status change via API
    function performBulkStatusChange(collectionId, newStatus, updatedDate) {
        showLoadingModal('Updating component statuses...');
        
        fetch('/change_collection_status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                collection_id: collectionId,
                new_status: newStatus,
                updated_date: updatedDate
            })
        })
        .then(response => response.json())
        .then(data => {
            hideLoadingModal();
            
            if (data.success) {
                showToast(data.message, 'success');
                
                // Close modal and refresh page
                const modal = bootstrap.Modal.getInstance(document.getElementById('collectionModal'));
                modal.hide();
                
                // Refresh page after short delay
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                showToast(data.message, 'danger');
            }
        })
        .catch(error => {
            hideLoadingModal();
            console.error('Error:', error);
            showToast('An error occurred while updating component statuses.', 'danger');
        });
    }
    
    // Setup bike select change handler
    document.addEventListener('DOMContentLoaded', function() {
        const bikeSelect = document.getElementById('collection_bike_id');
        if (bikeSelect) {
            bikeSelect.addEventListener('change', setupComponentValidation);
        }
    });
    
})();