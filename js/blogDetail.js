document.addEventListener('DOMContentLoaded', function () {
    // Get the post ID from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const postId = urlParams.get('id');

    if (postId) {
        fetchPostDetails(postId);
    } else {
        document.getElementById('postContent').innerText = 'No post ID provided.';
    }
});

function fetchPostDetails(postId) {
    const apiUrl = `http://localhost:8000/blog/posts/${postId}`;

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update the DOM with the fetched blog post details
            document.getElementById('postTitle').innerText = data.title;
            document.getElementById('postTitleBreadcrumb').innerText = data.title;
            document.getElementById('postDate').innerText = `Published on: ${formatDate(data.date)}`;
            document.getElementById('postImage').src = data.image_url;
            document.getElementById('postContent').innerText = data.content;
            document.getElementById('postAuthor').innerText = data.author || 'Unknown Author';
        })
        .catch(error => {
            document.getElementById('postContent').innerText = 'Error loading post details.';
            console.error('Error fetching post details:', error);
        });
}

// Utility function to format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}
