// facts.js






//This code is responsible for fact scrolling on the main page, complete with some additional logic.


document.addEventListener('DOMContentLoaded', function() {
  const factsArray = [
    "● 95% of respondents said that presenting well has a wider impact on a person’s career.",
    "● 60% of people said a successful presentation can help build one’s personal reputation.",
    "● 45% of people said that a strong presentation had helped them win new business.",
    "● 50% of those surveyed believed impactful presenting skills could boost their organisation’s profile."
  ];

  const factsList = document.getElementById('did-you-know-facts');
  let currentFactIndex = 0; 

  // Create list items from the facts array
  factsArray.forEach(fact => {
    const li = document.createElement('li');
    li.textContent = fact;
    li.classList.add('inline-block', 'mx-4', 'hidden'); // Initially hide
    factsList.appendChild(li);
  });

  // Get all the dynamically created facts
  const facts = factsList.querySelectorAll('li'); 

  // Hide all facts initially (handled within the loop above)

  function showNextFact() {
    facts[currentFactIndex].classList.remove('show');
    facts[currentFactIndex].classList.add('hidden');

    currentFactIndex = (currentFactIndex + 1) % facts.length;

    facts[currentFactIndex].classList.add('show');
    facts[currentFactIndex].classList.remove('hidden');
  }

  function showPrevFact() {
    facts[currentFactIndex].classList.remove('show');
    facts[currentFactIndex].classList.add('hidden');

    currentFactIndex = (currentFactIndex - 1 + facts.length) % facts.length;

    facts[currentFactIndex].classList.add('show');
    facts[currentFactIndex].classList.remove('hidden');
  }

  document.querySelector('.prev-fact').addEventListener('click', showPrevFact);
  document.querySelector('.next-fact').addEventListener('click', showNextFact);

  // Immediately display the first fact on load  
  facts[0].classList.remove('hidden'); 
  facts[0].classList.add('show');  

  // Function to automatically cycle facts
  function cycleFacts() {
    showNextFact(); 
  }

  // Start cycling the facts 
  let factInterval = setInterval(cycleFacts, 5000); // 5 seconds

  // Add logic to stop cycling on button interaction
  document.querySelector('.prev-fact').addEventListener('click', function() {
      clearInterval(factInterval); 
  });

  document.querySelector('.next-fact').addEventListener('click', function() {
      clearInterval(factInterval); 
  });

  // **Optional: Restart cycling after button interaction**
  // You can uncomment the following lines to restart the cycling after interaction
  // document.querySelector('.prev-fact').addEventListener('click', function() {
  //     clearInterval(factInterval);
  //     factInterval = setInterval(cycleFacts, 5000); // Restart after 5 seconds
  // });
  // 
  // document.querySelector('.next-fact').addEventListener('click', function() {
  //     clearInterval(factInterval);
  //     factInterval = setInterval(cycleFacts, 5000); // Restart after 5 seconds
  // });
});
