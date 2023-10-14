(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();

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
            const openaiApiKey = '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';
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
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').css('top', '0px');
        } else {
            $('.sticky-top').css('top', '-100px');
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Header carousel
    $(".header-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        items: 1,
        dots: true,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ]
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        margin: 24,
        dots: true,
        loop: true,
        nav : false,
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });
    
})(jQuery);
document.addEventListener("DOMContentLoaded", function () {
    const chatContent = document.getElementById("chat-content");
    const chatInput = document.getElementById("chat-input");
    const voiceButton = document.getElementById("voice-button");
    const sendButton = document.getElementById("send-button");

    // Function to add a message to the chat content
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement("div");
        messageDiv.className = isUser ? "user-message" : "assistant-message";
        messageDiv.textContent = message;
        chatContent.appendChild(messageDiv);
        // Scroll to the bottom to see the latest message
        chatContent.scrollTop = chatContent.scrollHeight;
    }

    // Function to send a user message to the assistant and receive a response
    async function sendMessage() {
        const userMessage = chatInput.value;
        if (!userMessage) return; // Don't send an empty message

        addMessage(userMessage, true); // Add user message to chat content

        // Clear the input field
        chatInput.value = "";

        // Make an API call to OpenAI (replace 'YOUR_API_KEY' with your actual API key)
        const apiKey = 'YOUR_API_KEY';
        const response = await fetch("/api/openai", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${apiKey}`
            },
            body: JSON.stringify({ message: userMessage }),
        });

        if (response.ok) {
            const data = await response.json();
            const assistantMessage = data.message;
            addMessage(assistantMessage); // Add assistant's response to chat content
        } else {
            console.error("Error sending message:", response.statusText);
        }
    }

    // Function to handle voice input (simulate voice input)
    function handleVoiceInput() {
        // Simulate voice input by generating a random message
        const voiceMessage = "This is a voice message."; // Replace with actual voice input
        addMessage(voiceMessage, true); // Add voice message to chat content
    }

    // Add click event listener to the voice button
    voiceButton.addEventListener("click", handleVoiceInput);

    // Add click event listener to the send button
    sendButton.addEventListener("click", sendMessage);

    // Add key press event listener to the chat input field
    chatInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent the default Enter key behavior (form submission)
            sendMessage(); // Send the message
        }
    });
});
