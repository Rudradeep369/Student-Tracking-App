const toggleDeleteButton = document.getElementById('toggleDelete');
    const deleteColumns = document.querySelectorAll('.delete-column');
    
    toggleDeleteButton.addEventListener('click', () => {
        deleteColumns.forEach(column => {
            column.classList.toggle('d-none');
        });
    });

    const unselectButton = document.getElementById('unselectButton');
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');

    unselectButton.addEventListener('click', () => {
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });
    });