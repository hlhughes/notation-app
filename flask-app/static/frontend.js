function updateSheetMusic() {
const filePath = "./static/realTime.abc"; // Path to the specific ABC file
            

            fetch(filePath)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('File not found: ' + filePath);
                    }
                    return response.text();
                })
                .then(abcContent => {
                    const formattedString = abcContent.replace(/\n/g, "<br>");
                    document.getElementById('abcContent').innerHTML = formattedString;

                    // Use ABCJS to render the ABC content into sheet music
                    ABCJS.renderAbc("paper", abcContent);
                })
                .catch(error => {
                    console.error('Error fetching the file: ', error);
                    // Handle the error (e.g., display an error message)
                });
        }

        // Update the sheet music every 5 seconds
        setInterval(updateSheetMusic, 500);

        // Also update the sheet music when the page loads
        document.addEventListener('DOMContentLoaded', updateSheetMusic);

