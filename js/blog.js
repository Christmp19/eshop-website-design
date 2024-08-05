document.addEventListener('DOMContentLoaded', function () {
    // Fetch blog posts and update the DOM
    fetch('http://localhost:8000/blog/posts')
        .then(response => response.json())
        .then(data => {
            const postGrid = document.getElementById('postGrid');
            data.forEach(post => {
                const postItem = document.createElement('article');
                postItem.classList.add('post-item');

                postItem.innerHTML = `
                    <img src="${post.image_url}" class="post-img" alt="Post Image">
                    <div class="post-content">
                        <h3 class="post-title">${post.title}</h3>
                        <p class="post-excerpt">${post.excerpt}</p>
                        <a href="/postDetail.html?id=${post.id}" class="read-more">Read More</a>
                    </div>
                `;

                postGrid.appendChild(postItem);
            });
        })
        .catch(error => console.error('Error fetching blog posts:', error));
});
