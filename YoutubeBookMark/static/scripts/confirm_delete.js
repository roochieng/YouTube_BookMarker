function confirmDelete(bookmarkId) {
    console.log("Delete button clicked for bookmark ID: " + bookmarkId);
    if (confirm("Are you sure you want to delete this bookmark?")) {
        console.log("User confirmed deletion.");
        // Use the fetch API to send a POST request
        fetch(`/delete/${bookmarkId}`, {
            method: 'POST',
        })
        .then(response => {
            if (response.status === 200) {
                // Bookmark deleted, reload the page
                window.location.reload();
            } else {
                console.error("Failed to delete bookmark.");
            }
        })
        .catch(error => {
            console.error("Error while sending the delete request: " + error);
        });
    } else {
        console.log("Deletion cancelled by user.");
    }
}