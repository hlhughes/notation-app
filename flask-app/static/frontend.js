var midiBuffer;
var visualObj;


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
                    // Display the ABC content TEXT
                    const formattedString = abcContent.replace(/\n/g, "<br>");
                    document.getElementById('abcContent').innerHTML = formattedString;

                    var startAudioButton = document.querySelector(".activate-audio");
                    var stopAudioButton = document.querySelector(".stop-audio");

                    var recording = document.getElementById('stop_record_btn');
                    // make the activate-audio button visible if the content is not empty
                    if (abcContent.length > 0 && recording === null) {
                        startAudioButton.style.display = "inline";
                        stopAudioButton.style.display = "inline";
                    }
                    else {
                        startAudioButton.style.display = "none";
                        stopAudioButton.style.display = "none";
                    }
                    
                    // Use ABCJS to render the ABC content into sheet music
                    visualObj = ABCJS.renderAbc("paper", abcContent, {
                        responsive: "resize" })[0];

                    // This object is the class that will contain the buffer
                    
                    
                    
                    
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



// This will play the synthesized audio
//startAudioButton.addEventListener("click", function() {
$(".activate-audio").click(function() {

    if (ABCJS.synth.supportsAudio()) {
        //stopAudioButton.style.display = "inline";

        // An audio context is needed - this can be passed in for two reasons:
        // 1) So that you can share this audio context with other elements on your page.
        // 2) So that you can create it during a user interaction so that the browser doesn't block the sound.
        // Setting this is optional - if you don't set an audioContext, then abcjs will create one.
        window.AudioContext = window.AudioContext ||
            window.webkitAudioContext ||
            navigator.mozAudioContext ||
            navigator.msAudioContext;
        var audioContext = new window.AudioContext();
        audioContext.resume().then(function () {
            //statusDiv.innerHTML += "<div>AudioContext resumed</div>";
            // In theory the AC shouldn't start suspended because it is being initialized in a click handler, but iOS seems to anyway.

            // This does a bare minimum so this object could be created in advance, or whenever convenient.
            midiBuffer = new ABCJS.synth.CreateSynth();

            // midiBuffer.init preloads and caches all the notes needed. There may be significant network traffic here.
            return midiBuffer.init({
                visualObj: visualObj,
                audioContext: audioContext,
                millisecondsPerMeasure: visualObj.millisecondsPerMeasure()
            }).then(function (response) {
                console.log("Notes loaded: ", response)
                //statusDiv.innerHTML += "<div>Audio object has been initialized</div>";
                // console.log(response); // this contains the list of notes that were loaded.
                // midiBuffer.prime actually builds the output buffer.
                return midiBuffer.prime();
            }).then(function (response) {
                //statusDiv.innerHTML += "<div>Audio object has been primed (" + response.duration + " seconds).</div>";
                //statusDiv.innerHTML += "<div>status = " + response.status + "</div>"
                // At this point, everything slow has happened. midiBuffer.start will return very quickly and will start playing very quickly without lag.
                midiBuffer.start();
                //statusDiv.innerHTML += "<div>Audio started</div>";
                return Promise.resolve();
            }).catch(function (error) {
                if (error.status === "NotSupported") {
                    //stopAudioButton.setAttribute("style", "display:none;");
                    var audioError = document.querySelector(".audio-error");
                    audioError.style.display = "inline";
                } else
                    console.warn("synth error", error);
            });
        });
    } else {
        var audioError = document.querySelector(".audio-error");
        audioError.style.display = "inline";
    }
});

//stopAudioButton.addEventListener("click", function() {
$(".stop-audio").click(function() {
    //startAudioButton.setAttribute("style", "");
    //explanationDiv.setAttribute("style", "");
    //stopAudioButton.setAttribute("style", "display:none;");
    if (midiBuffer)
        midiBuffer.stop();
});

