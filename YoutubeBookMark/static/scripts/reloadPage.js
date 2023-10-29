document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('bookmark-form'); // Replace 'bookmark-form' with the actual form ID

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent the default form submission

            // Serialize the form data into JSON
            const formData = new FormData(form);
            const formDataJSON = {};
            formData.forEach((value, key) => {
                formDataJSON[key] = value;
            });

            // Send an AJAX request to save the bookmark
            fetch('/save-bookmark', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formDataJSON),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Bookmark saved successfully, reload the page
                    location.reload();
                } else {
                    // Handle the case where bookmark saving failed
                    console.error('Bookmark saving failed:', data.error);
                }
            })
            .catch(error => {
                // Handle AJAX request errors
                console.error('AJAX request error:', error);
            });
        });
    }
});
