$(document).ready(function () {
    // Voice Input Button Click Event
    $('#voice').on('click', function () {
        // Check if the browser supports speech recognition
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.lang = $('#language').val(); // Set the selected language

            // Start voice recognition
            recognition.start();

            // Handle recognized speech
            recognition.onresult = function (event) {
                const result = event.results[0][0].transcript;
                $('#text').val(result); // Fill the input field with recognized text
            };

            // Handle errors
            recognition.onerror = function (event) {
                console.error(event.error);
            };
        } else {
            alert('Voice input is not supported in your browser.');
        }
    });

    // Send Button Click Event
    $('#send').on('click', function () {
        const message = $('#text').val();
        if (message.trim() !== '') {
            sendMessage(message);
        }
    });

    // Handle sending a message and receiving a response
    function sendMessage(message) {
        // Add the user's message to the chatbox
        const userHtml = '<p class="userText"><span>' + message + '</span></p>';
        $('#text').val(''); // Clear the input field
        $('#chatbox').append(userHtml);

        // Scroll to the bottom of the chatbox
        document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;

        // Send the user's message to OpenAI for a response (replace 'YOUR_OPENAI_API_KEY' with your actual key)
        const openaiApiKey = 'YOUR_OPENAI_API_KEY';
        const apiUrl = 'https://api.openai.com/v1/engines/davinci-codex/completions';

        $.ajax({
            type: 'POST',
            url: apiUrl,
            headers: {
                'Authorization': 'Bearer ' + openaiApiKey,
                'Content-Type': 'application/json',
            },
            data: JSON.stringify({
                prompt: message,
                max_tokens: 50, // Adjust the response length as needed
            }),
            success: function (data) {
                const botResponse = data.choices[0].text;
                // Add the bot's response to the chatbox
                const botHtml = '<p class="botText"><span>' + botResponse + '</span></p>';
                $('#chatbox').append(botHtml);

                // Scroll to the bottom of the chatbox
                document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;
            },
            error: function (error) {
                console.error(error);
            },
        });
    }
});

function generateResponse(prompt) {
    // Create an OpenAI client
    const openai = new OpenAI(OPENAI_API_KEY);
  
    // Send a request to the OpenAI API to generate a response
    openai.Completion.create({
      prompt: prompt,
      model: "text-davinci-002",
      max_tokens: 1024,
    }).then(response => {
      // Get the generated response from the OpenAI API
      const generatedResponse = response.choices[0].text;
  
      // Display the generated response in the chat
      document.getElementById("chat-response").innerHTML = generatedResponse;
    });
  }
  