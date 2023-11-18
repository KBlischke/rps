document.addEventListener('DOMContentLoaded', function() {
    let lecturer = document.querySelector('#lecturer');

    lecturer.addEventListener('change', async function() {
        try {
            let response = await fetch('/dozierenden_kurse?dozent=' + encodeURIComponent(lecturer.value));

            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }

            let courses = await response.text();
            document.querySelector('#course').innerHTML = courses;
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });
});
